from mongoengine import connect, Document
from mongoengine.fields import *
from enum import Enum
from .PPrinter import PPrinter
from .Datetime import Datetime


Printer = PPrinter()
DEFAULT_CONNECTION_NAME = 'default'

def init(db_uri, alias=None):
    alias_name = alias or DEFAULT_CONNECTION_NAME
    Printer.success(f"[DATABASE] Start connecting to {db_uri} ({alias_name}) at", Datetime.now())
    connect(host=db_uri, alias=alias_name)
    Printer.success('[DATABASE] Connect database successfully')

class Source(Enum):
    AD = 'AD'
    USER = 'user'
    SYSTEM = 'system'
    OTHER = 'other'

class ProcessStatus(Enum):
    SUCCESS = 'success'
    FAIL = 'fail'

class BaseDocument(Document):
    createdAt = DateTimeField(default=Datetime.utcnow())
    updatedAt = DateTimeField(default=Datetime.utcnow())

    meta = {
        'abstract': True,
        'strict': False,
    }

class Node(BaseDocument):
    id = LongField(primary_key=True)
    location = PointField(required=True)

    meta = {
        'collection': 'Nodes',
    }

class Street(BaseDocument):
    id = LongField(primary_key=True)
    name = StringField()
    type = StringField()
    max_velocity = DecimalField(default=40)
    level = IntField()

    meta = {
        'collection': 'Streets',
        'indexes': ['type', 'level'],
    }

class Segment(BaseDocument):
    id = LongField(primary_key=True)
    polyline = PolygonField(required=True)
    length = IntField()
    start_node = LazyReferenceField(Node)
    end_node = LazyReferenceField(Node)
    street = LazyReferenceField(Street, required=True)
    street_name = StringField()
    street_level = IntField()

    meta = {
        'collection': 'Segments',
        'indexes': ['street_level'],
    }

class SpeechRecord(BaseDocument):
    script = IntField()
    data = BinaryField(required=True)
    length = IntField()
    contentType = StringField()
    encoding = StringField()
    dataEnhanced = BinaryField()

    meta = {'collection': 'SpeechRecords'}

class SpeechReport(BaseDocument):
    user = ObjectIdField()
    segments = ListField(LongField(min_value=1))
    speech_record = ReferenceField(SpeechRecord, required=True)
    period_id = ObjectIdField(required=True)
    source = EnumField(Source, default=Source.OTHER)
    processed_date = DateTimeField()
    processed_status = EnumField(ProcessStatus)

    meta = {'collection': 'SpeechReports'}

class SegmentReport(BaseDocument):
    user = ObjectIdField()
    segment = LazyReferenceField(Segment, required=True)
    center_point = PointField(Required=True)
    velocity = IntField(required=True, min_value=0, max_value=200)
    description = StringField()
    images = ListField(URLField())
    period_id = ObjectIdField(required=True)
    causes = ListField(StringField())
    source = EnumField(Source, default=Source.USER, choices=[Source.AD, Source.USER, Source.SYSTEM])

    meta = {'collection': 'SegmentReports'}

    @classmethod
    def from_dict(cls, data):
        return cls(
            user=data.get('user'),
            segment=data.get('segment'),
            center_point = data.get('center_point'),
            velocity=data.get('velocity'),
            description=data.get('description'),
            images=data.get('images'),
            period_id=data.get('period_id'),
            causes=data.get('causes'),
            source=data.get('source'),
            createdAt=data.get('createdAt'),
            updatedAt=data.get('updatedAt')
        )
    
    def __repr__(self):
        return f"SegmentReport(_id: {self.id}, segment: {self.segment}, center_point: {self.center_point}, velocity: {self.velocity}, period_id: {self.period_id}, user: {self.user})"
