from flask import Flask, request, jsonify, render_template
from sqlalchemy import create_engine, text, insert
from datetime import datetime

import uuid
import os

SCRIPT_PATH = os.path.dirname(__file__)
LOG_DIR = 'logs'
LOG_PATH = f"{SCRIPT_PATH}{LOG_DIR}"


dbEngine = create_engine("mysql+mysqlconnector://netadmin:12221222@192.168.0.30/dataphobe")

def logMessage(msgClass, logText):
    curDate = datetime.now().strftime("%Y-%m-%d")
    curDateTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logfilePath = f"{LOG_PATH}CreateBillingCSV.{curDate}.log"  
   
    if (msgClass == 'DEBUG' and DEBUG != 'Yes'):
        return

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
    
    selectQuery = text("SELECT * FROM endpoint WHERE uid = :uid")
    newEndpointResultSet = executeSQL(selectQuery, {'uid': uid})
    newEndpointResult = newEndpointResultSet.mappings().all()
    return newEndpointResult

def deleteEndpoint(endpointID):
    if len(getEndpointByID(endpointID)) == 0:
        logMessage('WARNING', f'Attempted to delete: {endpointID}, which does not exist')
        return False
    deleteQuery = text('DELETE FROM endpoint WHERE id = :id')
    executeSQL(deleteQuery, {'id':endpointID})
    logMessage('INFO', f'Deleting endpoint: {endpointID}')
    return True
    
def getEndpointByID(endpointID):
    selectQuery = text("SELECT display_name, uid FROM endpoint WHERE id = :id") 
    endpointResultSet = executeSQL(selectQuery, {'id':endpointID})
    endpointResult = endpointResultSet.mappings().all()
    return endpointResult
    
def getEndpoints():
    selectQuery = text("SELECT id, display_name, uid FROM endpoint") 
    endpoints = executeSQL(selectQuery)
    return endpoints

def getAlertsByEndpoint(endpointUID):
    selectQuery = text('SELECT * FROM alert a JOIN endpoint e on a.endpoint_id = e.id WHERE e.uid = :uid')
    alertResultSet = executeSQL(selectQuery, {endpointUID})
    
def getActiveAlerts():
    selectQuery = text("""SELECT CONCAT('AL', a.id) AS id, e.display_name, a.insert_date, a.category, rc.reference_code_label AS status, a.name, a.body, a.priority
                       FROM alert a  
                       JOIN endpoint e  ON a.endpoint_id = e.id 
                       JOIN (SELECT * FROM reference_code WHERE reference_type = 'alertStatus') rc ON a.status = rc.reference_code
                       WHERE a.status in (1,2)""") 
    endpoints = executeSQL(selectQuery)
    return endpoints

def getAlertByID(alertID):
    selectQuery  = text(f""" SELECT CONCAT('AL', a.id) AS id, e.display_name, a.insert_date, a.category, rc.reference_code_label AS status, a.name, a.body, a.priority
                        FROM alert a  
                        JOIN endpoint e  ON a.endpoint_id = e.id 
                        JOIN (SELECT * FROM reference_code WHERE reference_type = 'alertStatus') rc ON a.status = rc.reference_code
                        WHERE CONCAT('AL', a.id) = {alertID}
                        """)

def getEndpointByUID(endpointUID):
    selectQuery = text("SELECT * FROM endpoint WHERE uid = :uid")
    endpointResultSet = executeSQL(selectQuery, {'uid': endpointUID})
    if endpointResultSet.rowcount == 0:
        return False
    endpointResult = endpointResultSet.mappings().all()
    return endpointResult

def createAlertHistoryRecord(alertID, historyType, historyUser, historySummary) -> bool:
    insertQuery = text("""INSERT INTO alert_history (alert_id, effective_date, type, user, summary)
                       VALUES (:alertID, NOW(), :historyType, :historyUser, :historySummary)""")
    alertHistoryResult = executeSQL(insertQuery, {'alertID': alertID, 'historyType': historyType, 'historyUser': historyUser, 'historySummary': historySummary})
    print(f'alertHistoryResult Value: {alertHistoryResult.rowcount}')
    return True

def updateAlertStatus(alertID, userID, newAlertStatus) -> bool:
    updateQuery = text("""UPDATE alert SET status = :status
                       WHERE id = :alertID""")
    alertResult = executeSQL(updateQuery, {'status': newAlertStatus, 'alertID': alertID})
    createAlertHistoryRecord(alertID, 'alertStatusUpdate', 'admin', f'User admin updated the status to {newAlertStatus}')
    return True

def createAlert(alertEndpoint, alertName, alertBody, alertOrigin=None, alertCategory=None, alertPriority=None):
    endpointDetails = getEndpointByUID(alertEndpoint)
    if endpointDetails == False:
        logMessage('ERROR', f'createAlert: Failed to create alert because endpoint {alertEndpoint} does not exist')
        return False
    alertEndpointID = endpointDetails[0]['id']
    if alertCategory is None:
        #derive from endpoint default category
        alertCategory = 'default'
    
    insertQuery = text(""" 
                   INSERT INTO alert (endpoint_id, insert_date, effective_date, status, body, name, priority, category)
                   VALUES(:endpointID, NOW(), NOW(), :status, :body, :name, :priority, :category)
                   """)
    result = executeSQL(insertQuery, {'endpointID': alertEndpointID, 'status': 1, 'body': alertBody, 'name': alertName, 'priority': alertPriority, 'category': alertCategory})
    print(result.rowcount)
    return result
    

app = Flask(__name__)
from routes.MainRoutes import main_bp
# Register the blueprint
app.register_blueprint(main_bp)
    
    
    
    
        
    
    