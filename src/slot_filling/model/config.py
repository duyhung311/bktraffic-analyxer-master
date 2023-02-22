import torch
from src.utils.path import SlotFillingPath

INTENT_LABEL = ['UNK', 'report']
SLOT_LABEL = ['UNK', 'O', 'B-location', 'I-location', 'B-velocity', 'I-velocity', 'B-reason', 'I-reason']

DEVICE = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

path_helper = SlotFillingPath()
SL_MODEL_PATH = path_helper.sl_model_path()
