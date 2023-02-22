import os


RESOURCES = 'resources'
STREETS_FILE = os.path.join(RESOURCES, 'streets.txt')

class ModelPath:
    def __init__(self, url, folder_name, filename):
        self._url = url
        self._folder_name = folder_name
        self._filename = filename
    
    @property
    def folder_path(self):
        return os.path.join(RESOURCES, self._folder_name)
    
    @property
    def file_path(self):
        return os.path.join(RESOURCES, self._folder_name, self._filename)
    
    @property
    def url(self):
        return f"{self._url}/{self._filename}"
    
    @property
    def folder_name(self):
        return self._folder_name
    
    @property
    def filename(self):
        return self._filename
    
    def exists(self):
        return os.path.exists(self.file_path)

class ASRPath(ModelPath):
    def __init__(self):
        super().__init__(
            os.getenv('ASR_S3_URL'),
            os.getenv('ASR_FOLDER_NAME'),
            os.getenv('ASR_S3_FILENAME'),
        )

class SlotFillingPath(ModelPath):
    def __init__(self):
        super().__init__(
            os.getenv('SF_S3_URL'),
            os.getenv('SF_FOLDER_NAME'),
            os.getenv('SF_S3_FILENAME'),
        )
        self.bert = os.getenv('SF_BERT')
        self.crf = os.getenv('SF_CRF')
    
    @property
    def sf_bert_path(self):
        return os.path.join(self.folder_path, self.bert)
    
    @property
    def sf_crf_path(self):
        return os.path.join(self.folder_path, self.crf)
    
    def exists(self):
        return os.path.exists(self.sf_bert_path) and os.path.exists(self.sf_crf_path)
    
    def downloaded_zip(self):
        return os.path.exists(self.filename)
    
    def sl_model_path(self):
        # resources/slot_filling/JointIDSF_PhoBERTencoder/4e-5/0.15/100'
        return os.path.join(self.sf_bert_path, '4e-5', '0.15', '100')

class VelocityEstimatorPath(ModelPath):
    def __init__(self):
        super().__init__(
            os.getenv('VELOCITY_ESTIMATOR_URL'),
            os.getenv('VELOCITY_ESTIMATOR_FOLDER_NAME'),
            os.getenv('VELOCITY_ESTIMATOR_FILENAME'),
        )
    
    @property
    def data_path(self):
        return os.path.join(self.folder_path, 'data')
    
    @property
    def encoder_path(self):
        return os.path.join(self.folder_path, 'encoders')

    @property
    def model_path(self):
        return os.path.join(self.folder_path, 'model')
    
    def exists(self):
        return os.path.exists(self.data_path) and os.path.exists(self.encoder_path) and os.path.exists(self.model_path)
    
    def downloaded_zip(self):
        return os.path.exists(self.filename)
    
    def model_filename(self):
        return os.path.join(self.model_path, 'model.pt')

    def segment_csv_filename(self):
        return os.path.join(self.data_path, 'segments.csv')
    
    def segment_status_folder_path(self):
        return os.path.join(self.data_path, 'segment_status')
    
    def segment_id_encoder_path(self):
        return os.path.join(self.encoder_path, 'segment_id_encoder.pkl')
    
    def street_level_encoder_path(self):
        return os.path.join(self.encoder_path, 'street_level_encoder.pkl')
    
    def street_type_encoder_path(self):
        return os.path.join(self.encoder_path, 'street_type_encoder.pkl')
