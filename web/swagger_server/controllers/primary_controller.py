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



def get_primary():
    global vrs
    """
    primary
    Returns most updated primary 

    :rtype: Problem
    """

    print("\n-----------------------GET PRIMARY----------------------\n")
    print("vrs here is: {0}".format(vrs))

    # Checks vrs number and sees if it is 0
    if vrs == 0:
        print("\nDatabase is Empty")
        return jsonify({"version": vrs, "body": 0})
    #Else it will look into the database and find the content using the version number
    else:
        ret_object = db.posts.find_one({"version": vrs-1})
        if ret_object is None:
            return get_status(404, "COULD NOT FIND"), status.HTTP_404_NOT_FOUND
        #Returns actual data to the server
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
        print("\n-----------------------POST PRIMARY----------------------\n")
        str_body = str(problem.decode("utf-8")).replace('\'', '\"')
        json.loads(str_body)
        #pprint(str_body)
        print("vrs is: {0} | In Version is: {1}\n".format(vrs, version))

        #Gets JSON from connection and store in problem
        problem = Body.from_dict(connexion.request.get_json())
        json.dumps(problem, sort_keys = True, indent = 4, ensure_ascii = False)
        print("\nproblem\n")
        pprint(problem)

        #If the Version is 9000 and the JSON has "delete" = 1, then reset server database
        if (version == 9000) and ("delete" in problem):
            if problem["delete"] == 1:   
                print("Deleting data in db")
                #Resets server database
                db.posts.delete_many({})
                #Sets vrs variable to 0 so it will get deleted
                vrs = 0
                return jsonify({"version": version})
            else:
                print("Version was 9000 but 'delete' = 1 not in body. Database still intact")
        else:
            #Does a check. Happens when server restarts anew
            if vrs == 0:
                print("Deleting data in db")
                #Deletes database
                db.posts.delete_many({})
                vrs = 0

            #Run actual POST of message into database
            if vrs == version:
                print("Versions Equal")

                db_size = db.posts.count()+1
                print("\ndb_size is: {0}".format(db_size))
                #Inserts the content into the body and adds version number as well
                db.posts.insert_one({"version": version, "body": problem})
                #Increments vrs variable
                vrs = vrs + 1
                print("\nvrs incremented to {0}".format(vrs))
                print("\n\tSUCCESS")
                
                #Return to server, the version # just as a check
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
