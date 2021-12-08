import pytest
import json
import logging
import os
import joblib
from prediction_service.prediction import form_response, api_response
import prediction_service

input_data = {'incorrect_range':{"fixed_acidity":12332451,
"volatile_acidity":421,
"citric_acid":0.5,
"residual_sugar":2,
"chlorides":0.5,
"free_sulfur_dioxide":2,
"total_sulfur_dioxide":7,
"density":1,
"pH":3,
"sulphates":1.5,
"alcohol":12
},

'correct_range':
{"fixed_acidity":5,
"volatile_acidity":1,
"citric_acid":0.5,
"residual_sugar":2,
"chlorides":0.5,
"free_sulfur_dioxide":2,
"total_sulfur_dioxide":7,
"density":1,
"pH":3,
"sulphates":1.5,
"alcohol":12
}
}

TARGET_range={
    'min':3.0,
    'max':8.0
}

def test_form_response_correct_range(data=input_data['correct_range']):
    res = form_response(data)
    assert TARGET_range['min'] <= res <= TARGET_range['max']

def test_api_response_correct_range(data=input_data['correct_range']):
    res = api_response(data)
    assert TARGET_range['min'] <= res <= TARGET_range['max']


def test_form_response_incorrect_range(data=input_data['incorrect_range']):
    with pytest.raises(prediction_service.prediction.NotInRange):
        res = form_response(data)

def test_api_response_incorrect_range(data=input_data['incorrect_range']):
    res = api_response(data)
    assert res['response'] == prediction_service.prediction.NotInRange().message




