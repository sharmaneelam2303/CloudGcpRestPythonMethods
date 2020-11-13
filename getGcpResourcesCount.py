from google.oauth2 import service_account
import googleapiclient.discovery
from google.cloud import resource_manager
import json


# TODO : Lines 8 to 16 will be required for setup when running test cases from ROBOT
cwd = __file__
text = cwd.split('\\')[-1]
filename = 'some-project.json'
path = cwd[:-(len(text))] + filename
service_account_info = json.load(open(path))
client = resource_manager.Client.from_service_account_json(path)
credentials = service_account.Credentials.from_service_account_info(service_account_info)
compute_service = googleapiclient.discovery.build('compute', 'v1', credentials=credentials, cache_discovery=False)
cloudfunction_service = googleapiclient.discovery.build('cloudfunctions', 'v1', credentials=credentials, cache_discovery=False)


# TODO : Lines 20 to 23 can be used to check results of functions without using test cases from PYTHON
# client = resource_manager.Client.from_service_account_json('some-project.json')
# credentials = service_account.Credentials.from_service_account_file(filename='some-project.json')
# compute_service = googleapiclient.discovery.build('compute', 'v1', credentials=credentials, cache_discovery=False)
# cloudfunction_service = googleapiclient.discovery.build('cloudfunctions', 'v1', credentials=credentials, cache_discovery=False)


project = ''
for proj in client.list_projects():
    project = proj.project_id


def __getTotalCountForGcpVmInstances():
    total = 0
    zoneList = __list_zones()
    for zone in zoneList:
        result = compute_service.instances().list(project=project, zone=zone).execute()
        if 'items' in result:
            instances = result['items']
            for instance in instances:
                total = total + 1
    return total


def __getTotalCountForGcpFirewallRules():
    total = 0
    result = compute_service.firewalls().list(project=project).execute()
    if 'items' in result:
        firewalls = result['items']
        for firewall in firewalls:
            total = total + 1
    return total


def __getTotalCountForGcpNetworks():
    total = 0
    result = compute_service.networks().list(project=project).execute()
    if 'items' in result:
        networks = result['items']
        for network in networks:
            total = total + 1
    return total


def __getTotalCountForGcpSubNetworks():
    total = 0
    allRegions = __list_regions()
    for region in allRegions:
        result = compute_service.subnetworks().list(project=project, region=region).execute()
        if 'items' in result:
            subs = result['items']
            for sub in subs:
                total = total + 1
    return total


def __getTotalCountForGcpCloudFunctions():
    total = 0
    name = 'projects/' + project
    locations = cloudfunction_service.projects().locations().list(name=name).execute()
    for location in locations['locations']:
        result = cloudfunction_service.projects().locations().functions().list(parent=location['name']).execute()
        if 'functions' in result:
            functions = result['functions']
            for function in functions:
                total = total + 1
    return total


def __list_regions():
    allRegions = []
    request = compute_service.regions().list(project=project)
    while request is not None:
        response = request.execute()
        for region in response['items']:
            allRegions.append(region['name'])
        request = compute_service.regions().list_next(previous_request=request, previous_response=response)
    return allRegions


def __list_zones():
    allZones = []
    request = compute_service.regions().list(project=project)
    while request is not None:
        response = request.execute()
        for reg in response['items']:
            for zone in reg['zones']:
                allZones.append(zone.split('/')[-1])
        request = compute_service.regions().list_next(previous_request=request, previous_response=response)
    return allZones


def getGcpTotalCountOfResources(resourceName):
    if resourceName == 'VM Instances':
        total = __getTotalCountForGcpVmInstances()
    elif resourceName == 'Networks':
        total = __getTotalCountForGcpNetworks()
    elif resourceName == 'Firewall Rules':
        total = __getTotalCountForGcpFirewallRules()
    elif resourceName == 'Subnetworks':
        total = __getTotalCountForGcpSubNetworks()
    elif resourceName == 'Cloud Function':
        total = __getTotalCountForGcpCloudFunctions()
    else:
        total = 0
    return total
