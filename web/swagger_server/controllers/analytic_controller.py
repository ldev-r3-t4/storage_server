import connexion
from swagger_server.models.body import Body
from swagger_server.models.problem import Problem
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime


def get_analytic():
    """
    analytic
    Returns most updated analytic 

    :rtype: Problem
    """
    return 'do some magic!'


def post_analytic(version, problem):
    """
    Update the existing analytic
    
    :param version: The version of the problem being manipulated
    :type version: int
    :param problem: Problem object that needs to be updated.
    :type problem: dict | bytes

    :rtype: int
    """
    if connexion.request.is_json:
        problem = Body.from_dict(connexion.request.get_json())
    return 'do some magic!'