from .Datetime import Datetime


class SegmentReportSerializer():
    @staticmethod
    def serialize(segment_report):
        return {
            'segment_id': segment_report.segment.id,    # Reference
            'source': segment_report.source.value,      # Enum
            'velocity': segment_report.velocity,
            'causes': segment_report.causes,
            'description': segment_report.description,
            'createdAt': datetime_to_epoch(segment_report.createdAt),
            'updatedAt': datetime_to_epoch(segment_report.updatedAt),
        }

def datetime_to_epoch(datetime):
    if datetime and Datetime.is_datetime(datetime):
        return datetime.timestamp()
