import boto3

# List WorkspaceIds not to be in the script rule
WORKSPACES_EXCEPTION = []

def execute_workspaces(command):
	"""
	This function execute start and stop workspaces where not in WORKSPACES_EXCEPTION
	"""
	client = boto3.client('workspaces')
	response = client.describe_workspaces()['Workspaces']

	# get WorkspacesIds
	workspaceIds = [ {'WorkspaceId': workspace['WorkspaceId']} for workspace in response if workspace['WorkspaceId'] not in WORKSPACES_EXCEPTION ]

	if command == 'start':
		response = client.start_workspaces(StartWorkspaceRequests=workspaceIds)
	
	elif command == 'stop':
		response = client.stop_workspaces(StopWorkspaceRequests=workspaceIds)	


def lambda_handler(event, context):
	"""
	execute function execute_workspaces
	@command (start, stop)
	"""
	execute_workspaces(command='stop')