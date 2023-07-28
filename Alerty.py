from flask import Flask, request, jsonify, render_template
from sqlalchemy import create_engine, text, insert
import uuid

app = Flask(__name__)
dbEngine = create_engine("mysql+mysqlconnector://netadmin:12221222@192.168.0.30/dataphobe")

def executeSQL(sql_query, *params):
    with dbEngine.connect() as connection:
        result = connection.execute(sql_query, *params)
        connection.commit()
        return result

def getUUID(charCount):
    uniqueID = uuid.uuid4().hex
    return uniqueID[:charCount]

def createEndpoint(displayName):
    uid = getUUID(6)
    insertQuery = text("INSERT INTO endpoint (uid, display_name) VALUES (:uid, :displayName);") 
    executeSQL(insertQuery,{"uid":uid, "displayName":displayName})

def getEndpoints():
    selectQuery = text("SELECT display_name, uid FROM endpoint") 
    endpoints = executeSQL(selectQuery)
    return endpoints

@app.route('/endpoints')
def render_endpoints():
    endpoints = getEndpoints()
    return render_template('endpoints.html', endpoints=endpoints)

@app.route('/')
def render_home(): 
    return render_template('main.html')
