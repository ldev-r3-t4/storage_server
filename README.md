# Storage API
This is the storage server implementation

## Accessing the Website/Server ui

**To access Existing EC2 Servers Go to this link** [**Main Website**](<http://ec2-54-69-164-246.us-west-2.compute.amazonaws.com:8000/v1/ui/#/primary/>)

## POSTMAN Automated Test Links ##

The public Postman URL to see and run the tests (independently) are found here:
https://documenter.getpostman.com/view/1745639/collection/6Ywyb8T

The shared Collections link to my tests are here:
https://www.getpostman.com/collections/993667a29a4d02bd5e23

## How to Run Test Framework on Docker ##

Run the following command in your Docker to run these tests on the server:
* $ docker run -t postman/newman_ubuntu1404 --url="https://www.getpostman.com/collections/993667a29a4d02bd5e23"


## Docker Repo ##
The storage server was dockerized as a stand-alone and is available below
https://github.com/bowei437/final_docker_storage

### What is this for? ###

This is the storage server for our final project. It will take in blobs (granted version number provided is correct) and store them. This repository contains the API definition, Mongodb DataBase Code, and Server host.

## Prerequisites to Run ##
* Docker is installed
* Your device is connected to the internet (to clone the repository and download required libraries)


## Videos of Tests ##
This repository also contains videos to be viewed showing the tests being run. Please see:

* Internal_Testing_Video.mp4
* POSTMAN_Automated_Tests.mp4


### Authors ###

* Bowei zhao
