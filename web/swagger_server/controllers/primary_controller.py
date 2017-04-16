import connexion
import json
import os
import flask
from pprint import pprint

from swagger_server.models.body import Body
from swagger_server.models.problem import Problem
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

from flask import jsonify
from flask.ext.api import status
from pymongo import MongoClient

#____FOR LOCAL_______
client = MongoClient()
#_____________________

db = client.path_db

def insert_json(uid, version, body):
    #print("inside func")
    db.posts.insert_one({"problem_id": str(uid), "version": version, "body":body})

def get_primary():
    """
    primary
    Returns most updated primary 

    :rtype: Problem
    """
    array = []
    for post in db.posts.distinct("problem_id"):
        print(post)
        array.append(int(post))
    #run a check to see if the uid exists
    if len(array) == 0:
        return get_status(404, "No problems found"), status.HTTP_404_NOT_FOUND
    #if the uid doesn't exist then just go ahead return error status
    return jsonify({"problem_id": array})


def post_primary(version, problem):
    """
    Update the existing primary
    
    :param version: The version of the problem being manipulated
    :type version: int
    :param problem: Problem object that needs to be updated.
    :type problem: dict | bytes

    :rtype: int
    if connexion.request.is_json:
        problem = Body.from_dict(connexion.request.get_json())
    return 'do some magic!'
    """
    try:
        pprint(problem)
        #tprob = problem
        json.dumps(problem, ensure_ascii = False)
        print("\n\nproblem\n")
        pprint(problem)
        print("\n\n")


        str_body = str(problem.decode("utf-8")).replace('\'', '\"')
        json.loads(str_body)
        db_size = db.posts.count()+1
        print(str_body)
        problem = Body.from_dict(connexion.request.get_json())
        for i in range(1, db_size):
            print(i)
        insert_json(db_size, 0, problem)
        #print("out of func")
        return jsonify({"problem_id": db_size})
    except ValueError:
        print("error Post Primary")
        return get_status(500, "Invalid JSON"), status.HTTP_500_INTERNAL_SERVER_ERROR
