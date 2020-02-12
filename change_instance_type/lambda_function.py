import json
import urllib3
import boto3
from botocore.exceptions import ClientError
from datetime import date, timedelta, datetime

# Variables of api.calendario.com.br
CITY = 'BELO_HORIZONTE'
STATE = 'MG'
TOKEN = 'bGVvbmFyZG9iaWZmaUBteWxpbnV4LmNvbS5iciZoYXNoPTEzMDE2MjU2NQ'

# Type Code of Holidays
#	1 - Feriado Nacional
#	4 - Facultativo
TYPE_CODE = ['1']

# Number Days of the Week
# 0 - Monday, 1 - Tuesday, 2 - Wednesday, 3 - Thursday, 4 - Friday, 5 - Saturday, 6 - Sunday
WEEK_DAY = ['5', '6']

# List of Instances with types
INSTANCES_TYPES = [

{'instance_id': 'i-07d820f98b96114b2', 'holiday_weekday': 't3a.micro', 'default': 't3a.small'},
{'instance_id': 'i-0f9bf9ddb218f9822', 'holiday_weekday': 't3a.micro', 'default': 't3a.small'},

]


def verify_weekday(today):

	weekno = str(today.weekday())
	
	if weekno in WEEK_DAY:
		return True
	else:
		return False


def verify_holiday(today):

	YEAR = today.year
	URL_HOLIDAYS = "https://api.calendario.com.br/?ano={0}&estado={1}&cidade={2}&token={3}&json=true".format(YEAR,STATE,CITY,TOKEN)
	
	# Get the holidays
	http = urllib3.PoolManager()
	response = http.request('GET', URL_HOLIDAYS)

	if response.status == 200:
		data = json.loads(response.data.decode('utf-8'))

	# Filter python objects with date
	holidays = [x for x in data if x['type_code'] in TYPE_CODE ]

	# Get today date BR Format
	date_today = today.strftime('%d/%m/%Y')
	today = [x for x in holidays if x['date'] == date_today]

	if today:
		return True
	else:
		return False


def verify_not_default(today):

	client = boto3.client('ec2')

	response = client.describe_instances(
		Filters=[
			{
				'Name': 'tag-key',
				'Values': ['NOT_DEFAULT']
			}
		]
	)

	instancelist = []
	
	for reservation in (response["Reservations"]):
		for instance in reservation["Instances"]:
			instancelist.append(instance["InstanceId"])

	if len(instancelist) > 0:
		return True
	else:
		return False


def change_instance_type(day_type, tag):
	
	# Let's use Amazon EC2
	ec2 = boto3.client('ec2')

	# Stop all instances
	instanceIds = [instance["instance_id"] for instance in INSTANCES_TYPES]
	ec2.stop_instances(InstanceIds=instanceIds)

	waiter = ec2.get_waiter('instance_stopped')
	waiter.wait(InstanceIds=instanceIds)

	for instance in INSTANCES_TYPES:

		print("Changing instance {0} to {1}".format(instance["instance_id"], instance[day_type]))

		# Change the instance type
		ec2.modify_instance_attribute(InstanceId=instance["instance_id"], Attribute='instanceType', Value=instance[day_type])

		# Remove tag
		ec2.delete_tags(Resources=[instance["instance_id"]],Tags=[{"Key": "NOT_DEFAULT"}])
		ec2.delete_tags(Resources=[instance["instance_id"]],Tags=[{"Key": "DEFAULT"}])

		# Define tag
		ec2.create_tags(Resources=[instance["instance_id"]],Tags=[{'Key': tag, 'Value': 'True'}])

		# Start the instance
		ec2.start_instances(InstanceIds=[instance["instance_id"]])

	print("Finalized")


def lambda_handler(event, context):

	today = datetime.today()
	# Test in specific day
	#today = datetime.strptime('01/01/20', '%d/%m/%y')

	if verify_weekday(today):
		print("Day into Weekday")
		change_instance_type(day_type="holiday_weekday", tag="NOT_DEFAULT")
	
	elif verify_holiday(today):
		print("Day into Holiday")
		change_instance_type(day_type="holiday_weekday", tag="NOT_DEFAULT")

	elif verify_not_default(today):
		change_instance_type(day_type="default", tag="DEFAULT")

	else:
		print('Default Day')
		

lambda_handler(None, None)