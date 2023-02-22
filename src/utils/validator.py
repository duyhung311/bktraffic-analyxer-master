from pydantic import BaseModel, ValidationError
from typing import Union, List
import json


class InferenceValidator(BaseModel):
    segment_id: List[int]
    timestamp: Union[int, float, List]

class SeqInferenceValidator(BaseModel):
    segment_id: List[int]
    timestamp: Union[int, float]

def validate_input(req, model):
    errors = []

    try:
        model = model(**req)
    except ValidationError as error:
        error_fields = []
        for e in json.loads(error.json()):
            if e['loc'][0] not in error_fields:
                error_fields.append(e['loc'][0])

        errors = []
        for e in error_fields:
            e = {
                'domain': f"field_{e}",
                'reason': 'wrong data type',
                'message': f"Field '{e}' is not in the right data type: {type(e)}"
            }
            errors.append(e)
    else:
        return errors, model.dict()

    return errors, {}
