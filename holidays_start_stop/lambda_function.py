import json
import urllib3
import boto3
from botocore.exceptions import ClientError
from datetime import date, timedelta

# Variables
URL = "https://api.calendario.com.br/?ano=2020&estado=MG&cidade=BELO_HORIZONTE&token=bGVvbmFyZG9iaWZmaUBteWxpbnV4LmNvbS5iciZoYXNoPTEzMDE2MjU2NQ&json=true"

INSTANCES_TYPES = [
{'instance_id': 'i-07d820f98b96114b2', 'holiday': 't3a.micro', 'default': 't3a.small'},
{'instance_id': 'i-01a3029daf317a386', 'holiday': 't3a.micro', 'default': 't3a.small'}
]

# Type Code
#	1 - Feriado Nacional
#	4 - Facultativo
#
TYPE_CODE = ['1']

def lambda_handler(event, context):

	# Get the holidays
	http = urllib3.PoolManager()
	response = http.request('GET', URL)

	if response.status == 200:
		data = json.loads(response.data.decode('utf-8'))

	# Filter python objects with date
	output_dict = [x for x in data if x['type_code'] in TYPE_CODE ]

	# Get today date BR Format
	date_today = date.today()
	date_yesterday = date_today - timedelta(days=1)
	
	date_today = date_today.strftime('%d/%m/%Y')
	date_yesterday = date_yesterday.strftime('%d/%m/%Y')

	today = [x for x in output_dict if x['date'] == date_today]
	yesterday = [x for x in output_dict if x['date'] == date_yesterday]

	# If today is holiday execute function
	if today:

		# Execute changes to holiday
		change_instance_type("holiday")

	else:
		print('Date {0} is not Holiday'.format(date_today))

		if yesterday:
			print('Ajusting to Default Instances types')

			# Execute changes to dafault
			change_instance_type("default")


def change_instance_type(day_type):
	
	# Let's use Amazon EC2
	ec2 = boto3.client('ec2')

	for instance in INSTANCES_TYPES:

		print("Changing instance {0} to {1}".format(instance["instance_id"], instance[day_type]))

		ec2.stop_instances(InstanceIds=[instance["instance_id"]])

		waiter = ec2.get_waiter('instance_stopped')
		waiter.wait(InstanceIds=[instance["instance_id"]])

		# Change the instance type
		ec2.modify_instance_attribute(InstanceId=instance["instance_id"], Attribute='instanceType', Value=instance[day_type])

		# Start the instance
		ec2.start_instances(InstanceIds=[instance["instance_id"]])

	print("Finalized")