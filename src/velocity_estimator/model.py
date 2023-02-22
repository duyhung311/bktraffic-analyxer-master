import torch
from torch import nn


class Net(nn.Module):
    def __init__(self, lstm_hidden_layers=256, device='cpu'):
        super().__init__()

        self.lstm_hidden_layers = lstm_hidden_layers

        self.street_level_embed = nn.Linear(4, 2)
        self.street_type_embed = nn.Linear(12, 8)
        self.segment_id_embed = nn.Linear(1276, 512)

        self.linear1 = nn.Linear(527, 256)
        self.linear2 = nn.Linear(256, 128)

        self.lstm1 = nn.LSTMCell(56, self.lstm_hidden_layers)

        self.linear4 = nn.Linear(self.lstm_hidden_layers + 128, 256)
        self.linear5 = nn.Linear(256, 128)
        self.linear6 = nn.Linear(128, 128)
        self.linear7 = nn.Linear(128, 1)

        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

    def forward(self, spatial_feature, temporal_feature, future_preds=0):
        outputs, batch_size = [], temporal_feature.size(0)
        
        # Spatial forwarding
        street_level, street_type, segment_id, rest = spatial_feature[:,0:4], spatial_feature[:,4:16], spatial_feature[:,16:1292], spatial_feature[:,1292:]
        out_1 = self.street_level_embed(street_level)
        out_2 = self.street_type_embed(street_type)
        out_3 = self.segment_id_embed(segment_id)

        out_4 = self.linear1(torch.cat((out_1, out_2, out_3, rest), axis=1))
        out_5 = self.linear2(out_4)

        # Temporal forwarding
        h_t = torch.zeros(batch_size, self.lstm_hidden_layers, dtype=torch.float32, device=self.device)
        c_t = torch.zeros(batch_size, self.lstm_hidden_layers, dtype=torch.float32, device=self.device)
        
        for input_t in temporal_feature.split(1, dim=1):
            h_t, c_t = self.lstm1(input_t.squeeze(dim=1), (h_t, c_t))
            linear_out = self.linear4(torch.cat((out_5, h_t), axis=1))
            linear_out2 = self.linear5(linear_out)
            linear_out3 = self.linear6(linear_out2)
            output = self.linear7(linear_out3) # output from the last FC layer
        outputs.append(output)

        if future_preds > 0:
            period_emb = temporal_feature[:, 47:, 1:]
            for i in range(future_preds):
                output = torch.concat((output, period_emb[:, i]), dim=1)
                h_t, c_t = self.lstm1(output, (h_t, c_t))
                linear_out = self.linear4(torch.cat((out_5, h_t), axis=1))
                linear_out2 = self.linear5(linear_out)
                linear_out3 = self.linear6(linear_out2)
                output = self.linear7(linear_out3) # output from the last FC layer
                outputs.append(output)

        # transform list to tensor    
        outputs = torch.cat(outputs, dim=1)

        return outputs
