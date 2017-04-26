# -*- coding: utf-8 -*-


import boto3
import MySQLdb

# GLOBAL VARIABLES
REGION_NAME = 'us-east-1'


def download_bd():
    s3 = boto3.resource('s3',
                        region_name=REGION_NAME,)
    s3.meta.client.download_file('fluidserves', '', '/tmp/')


def dump_bd(route, username, passw, bdname):

    db = MySQLdb.connect(host=route,    # your host, usually localhost
                         user=username,         # your username
                         passwd=passw,  # your password
                         db=bdname)        # name of the data base

    # you must create a Cursor object. It will let
    #  you execute all the queries you need
    cur = db.cursor()

    # Use all the SQL you like
    cur.execute("SELECT * FROM YOUR_TABLE_NAME")

    # print all the first cell of all the rows
    for row in cur.fetchall():
        print row[0]

    db.close()
