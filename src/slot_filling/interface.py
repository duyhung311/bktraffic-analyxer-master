import src.slot_filling.model.config as sl_cfg
from src.slot_filling.model import inference
from src.slot_filling import utils


class SlotFilling:
    def __init__(self):
        self.model = inference.SlotFillingInference(sl_cfg.SL_MODEL_PATH, sl_cfg.DEVICE)

    def predict(self, sentence):
        sentence = sentence.strip()
        words = sentence.split()
        words = [words]
        preds = self.model.predict(words)
        return preds

    def test(self):
        sentence = 'từ trường đại học bách khoa thành phố hồ chí minh đến ngã tư bảy hiền bị kẹt xe do có quá nhiều xe vận tốc đạt được khoảng bốn mươi ki lô mét trên giờ'
        print(self.predict(sentence))
        print(utils.sf2json(self.predict(sentence), sentence))

if __name__ == '__main__':
    sf_test = SlotFilling()
    sf_test.test()
