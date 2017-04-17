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

def get_status(status, message):
    return jsonify({"Status": status, "Message": message})

def insert_json(uid, version, body):
    #print("inside func")
    print(" -- Inserting Data into DB -- \nproblem_id: {0} \nversion: {1} \n".format(uid, version))
    db.posts.insert_one({"problem_id": str(uid), "version": version, "body":body})


def get_primary():
    global vrs
    """
    primary
    Returns most updated primary 

    :rtype: Problem
    """

    print("\n-----------------------GET----------------------\n")
    print("vrs here is: {0}".format(vrs))

    if vrs == 0:
        print("\nDatabase is Empty")
        return jsonify({"version": vrs, "body": })
    else:
        ret_object = db.posts.find_one({"version": vrs-1})
        if ret_object is None:
            return get_status(404, "COULD NOT FIND"), status.HTTP_404_NOT_FOUND
        return jsonify({"version": ret_object['version'], "body": ret_object['body']})




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
        print("\n-----------------------POST----------------------\n")
        str_body = str(problem.decode("utf-8")).replace('\'', '\"')
        json.loads(str_body)
        #pprint(str_body)
        print("vrs is: {0} | In Version is: {1}\n".format(vrs, version))

        if vrs == 0:
            print("Deleting data in db")
            db.posts.delete_many({})
            vrs = 0

        if vrs == version:
            print("Versions Equal")

            problem = Body.from_dict(connexion.request.get_json())
            json.dumps(problem, sort_keys = True, indent = 4, ensure_ascii = False)
            print("\nproblem\n")
            pprint(problem)
            

            db_size = db.posts.count()+1
            print("\ndb_size is: {0}".format(db_size))
            """
            for i in range(1, db_size):
                if(db.posts.find_one({"problem_id":str(i)}) == None):
                    insert_json(i, 0, problem)
                    return jsonify({"problem_id": i})
                print(i)
            """
            db.posts.insert_one({"version": version, "body": problem})
            
            vrs = vrs + 1
            print("\nvrs incremented to {0}".format(vrs))
            print("\n\tSUCCESS")
            


            return jsonify({"version": version})
        else:
            print("\n\tError Versions NOT EQUAL")
            print("\n\tFAILURE")
            #return 'Versions not equal'
            return get_status(412, "Incorrect Version Number"), status.HTTP_412_PRECONDITION_FAILED

        print("\n-------------------------------------------------\n")



        #return 'Magic happened2'
    except ValueError:
        print("\n\tError Post_Primary")
        print("\n\tFAILURE")
        return get_status(500, "Invalid JSON"), status.HTTP_500_INTERNAL_SERVER_ERROR
