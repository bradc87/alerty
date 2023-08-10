from flask import Blueprint, render_template, request, jsonify
from Alerty import getActiveAlerts, getEndpoints, deleteEndpoint, getEndpointByID, createEndpoint, createAlert, getAlertByID

main_bp = Blueprint('main', __name__)

@main_bp.route('/endpoints')
def render_endpoints():
    endpoints = getEndpoints()
    return render_template('endpoints.html', endpoints=endpoints)

@main_bp.route('/alerts')
def render_alerts():
    alerts = getActiveAlerts()
    return render_template('alertSummary.html', alerts=alerts)

@main_bp.route('/')
def render_home(): 
    return render_template('main.html')

@main_bp.route('/alertDetail/<alertID>')
def render_alertDetail(alertID):
    alertDetail = getAlertByID(alertID)
    return render_template('alertDetail.html', alertDetail)

@main_bp.route('/endpoint/modify', methods=['POST'])
def modifyEndpoint():
    # JSON Schema:
    # { 
    #   "endpointID": 123,
    #   "modifyAction": "delete, update"
    # }
    #print(request.get_data())
    requestDict = request.get_json()
    
    if requestDict['modifyAction'].lower() == 'delete':
        endpointID = requestDict['endpointID']
        deleteEndpoint(endpointID)
        deletedEndpoint = getEndpointByID(endpointID)
        if len(deletedEndpoint) == 0:
            response = {"status":"success", "statusMessage": f"Endpoint id {endpointID} deleted"}
            return jsonify(response), 200
    response = {"status":"fail", "statusMessage": f"Problem encountered while deleting endpoint id {endpointID}"}
    return jsonify(response), 501

@main_bp.route('/endpoint/create', methods=['POST'])
def endpoint_create():
    # JSON Schema:
    # { 
    #   "endpointDisplayName": 'testEndpoint'
    # }
    print(request.get_data())
    #print(request.data)
    requestDict = request.get_json()
    endpointDisplayName = requestDict['endpointDisplayName']
    
    newEndpoint = createEndpoint(endpointDisplayName)
    newEndpointUID = newEndpoint[0]['uid']
    if len(newEndpoint) == 1: 
        response = {"status":"success", "statusMessage": f"Endpoint with uid {newEndpointUID} created", "uid": newEndpointUID}
        return jsonify(response), 200
    response = {"status":"fail", "statusMessage": f"Problem encountered while creating endpoint"}
    return jsonify(response), 500

@main_bp.route('/alert/<endpoint>', methods=['POST'])
def alert_create(endpoint):
    requestDict = request.get_json()
    alertName = requestDict['alertName']
    alertBody = requestDict['alertBody']
    alertCategory = requestDict.get('alertCategory', None)
    alertPriority = requestDict.get('alertPriority', None)
    alertOrigin = requestDict.get('alertOrigin', None)
    
    newAlert = createAlert(endpoint, alertName, alertBody, alertOrigin, alertCategory, alertPriority)
    if newAlert == False:
        response = {"status":"fail", "statusMessage": f"Problem encountered while creating alert"}
        return jsonify(response), 500
    
    response = {"status":"success", "statusMessage": f"Alert created successfully"}
    return jsonify(response), 201

