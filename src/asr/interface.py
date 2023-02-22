import string
import pickle
from src.utils.path import ASRPath

class ASR:
    def __init__(self):
        self.path_helper = ASRPath()
        self.model = pickle.load(open(self.path_helper.file_path, 'rb'))

    def to_text(self, speech):
        return self.model(speech)

    def text_normalizer(self, text):
        text = text.upper()
        return text.translate(str.maketrans('', '', string.punctuation))
