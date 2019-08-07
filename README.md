# Insight DevOps Engineering Systems Puzzle Challenge

## Table of Contents
1. [Introduction](README.md#introduction)
2. [Puzzle details](README.md#puzzle-details)
3. [Postmortem](README.md#postmortem)

# Introduction

Imagine you're on an engineering team that is building an eCommerce site where users can buy and sell items (similar to Etsy or eBay). One of the developers on your team has put together a very simple prototype for a system that writes and reads to a database. The developer is using Postgres for the backend database, the Python Flask framework as an application server, and nginx as a web server. All of this is developed with the Docker Engine, and put together with Docker Compose.

Unfortunately, the developer is new to many of these tools, and is having a number of issues. The developer needs your help debugging the system and getting it to work properly.

# Puzzle details

The codebase included in this repo is nearly functional, but has a few bugs that are preventing it from working properly. The goal of this puzzle is to find these bugs and fix them. To do this, you'll have to familiarize yourself with the various technologies (Docker, nginx, Flask, and Postgres). You definitely don't have to be an expert on these, but you should know them well enough to understand what the problem is.

Assuming you have the Docker Engine and Docker Compose already installed, the developer said that the steps for running the system is to open a terminal, `cd` into this repo, and then enter these two commands:

    docker-compose up -d db
    docker-compose run --rm flaskapp /bin/bash -c "cd /opt/services/flaskapp/src && python -c  'import database; database.init_db()'"

This "bootstraps" the PostgreSQL database with the correct tables. After that you can run the whole system with:

    docker-compose up -d

At that point, the web application should be visible by going to `localhost:8080` in a web browser. 

***

# Postmortem 

![](https://i.imgur.com/e16qOEj.gif)

## Issue Summary & (Fictional) Timeline
* 08:00 PDT - The on call engineer attempts to set up the app but cannot access it at localhost:8080.
* 08:30 PDT - Not knowing much about docker-compose, they go and research about it and do some tutorials.
* 11:30 PDT - After learning more about docker-compose, the engineer notices that there is an error in the docker-compose.yml file for the Nginx port. They change the incorrect 80:8080 port to 8080:80.
* 12:00 PDT - The engineer has trouble setting up the environment using vagrant so they decide to spin up an Ubuntu VM.
* 13:00 PDT - After switching to the Ubuntu VM, the engineer manages to get a 502 gateway error. 
* 14:30 PDT - They run the command docker-compose up without the detach option to see the log details.
* 15:00 PDT - The logs show that flaskapp_1 was trying to run on port 5000. 
* 15:15 PDT - The engineer finds the flaskapp.conf file and changed the proxy_pass http://flaskapp:5001 to 5000. They reran the docker-compose up command and get a 200 status code.
* 16:00 PDT - They noticed that after entering the items nothing seem to happen so they manually got to localhost:8080/sucess and see [,,,,] and the app incorrectly redirects you to "localhost,localhost:8080".
* 19:00 PDT - The engineer realizes that the CRUD functions aren't working and that the entering items is only adding empty values to a list because there is not representation of the item in the models.
* 21:00 PDT - They add basic CRUD functionality to the app.
* 2:00  PDT - The enginer resolves the incorrect redirects by investigating routing issues. After researching more about Nginx and reverseproxying they are able to fix the problem by modifiying the proxy set header for Host and server inside of the flaskapp.conf file.
* 3:00  PDT - Problem resolved

## Root Causes
Main issues:
* Incorrect configuration of docker-compose.yml, Nginx port
* Flask routing in flaskapp.conf, changed from 5001 to 5000 to match the port flaskapp_1 runs on when executing docker-compose up.
* Improper redirects, was being redirected to "localhost,localhost:8080". Fix by modifiying proxy set header for Host and server inside of the flaskapp.conf file.
* CRUD actions weren't working properly, adding an item was just adding empty values to a list because there is no representation of the item in the models.py or forms.py file.     

## Corrective and preventative measures
* Don't set up the environment in a vagrant machine, there were issues with getting the ports to work.
* In the future, pair programming with another engineer could prevent typos in the configurations.
* A code review process or setting up a CI/CD pipeline with automated test would have caught the errors.
* Need to migrate to a production WSGI server soon!
