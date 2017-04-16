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

vrs = 0


def insert_json(uid, version, body):
    #print("inside func")
    print(" -- Inserting Data into DB -- \nproblem_id: {0} \nversion: {1} \n".format(uid, version))
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
    global vrs
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
        str_body = str(problem.decode("utf-8")).replace('\'', '\"')
        json.loads(str_body)
        #pprint(str_body)
        print("vrs is: {0} | In Version is: {1}".format(vrs, version))

        if vrs == version:
            print("\nVersions Equal")

            problem = Body.from_dict(connexion.request.get_json())
            json.dumps(problem, sort_keys = True, indent = 4, ensure_ascii = False)
            print("\n\nproblem\n")
            pprint(problem)
            print("\n\n")

            db_size = db.posts.count()+1
            print("db_size is: {0}".format(db_size))


            for i in range(1, db_size):
                if(db.posts.find_one({"problem_id":str(i)}) == None):
                    insert_json(i, 0, problem)
                    return jsonify({"problem_id": i})
                print(i)
            db.posts.insert_one({"version": version, "body": problem})
            
            vrs = vrs + 1
            if version == 9000:
                print("Deleting data in db")
                db.posts.delete_many({})

            return jsonify({"db_size": db_size})
        else:
            print("\nVersions NOT EQUAL")
            return get_status(412, "Invalid Version Number"), status.HTTP_412_INTERNAL_SERVER_ERROR



        #return 'Magic happened2'
    except ValueError:
        print("error Post Primary")
        return get_status(500, "Invalid JSON"), status.HTTP_500_INTERNAL_SERVER_ERROR
