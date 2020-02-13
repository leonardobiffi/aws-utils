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
WEEKDAY = ['5', '6']

# List of Instances with types
INSTANCES_TYPES = [

{'instance_id': 'i-07d820f98b96114b2', 'holiday_weekday': 't3a.micro', 'default': 't3a.small'},
{'instance_id': 'i-0f9bf9ddb218f9822', 'holiday_weekday': 't3a.micro', 'default': 't3a.small'},

]


def verify_weekday(today):

	weekno = str(today.weekday())
	
	if weekno in WEEKDAY:
		if filter_instance_tag(tag='WEEKDAY'):
			# Caso já esteja com a tag WEEKDAY não altera novamente
			return "WEEKDAY"
		else:
			# Retorna True para alterar o tipo da instancia
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
		if filter_instance_tag(tag='HOLIDAY'):
			# Caso já esteja com a tag HOLIDAY não altera novamente
			return "HOLIDAY"
		else:
			# Retorna True para alterar o tipo da instancia
			return True
	else:
		return False

def verify_default(today):

	if filter_instance_tag(tag='DEFAULT'):
		# Caso já esteja com a tag DEFAULT não altera novamente
		return "DEFAULT"
	else:
		# Retorna True para alterar o tipo da instancia
		return True

def filter_instance_tag(tag):

	client = boto3.client('ec2')

	response = client.describe_instances(
		Filters=[
			{
				'Name': 'tag-key',
				'Values': [tag]
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
		ec2.delete_tags(Resources=[instance["instance_id"]],Tags=[{"Key": "DEFAULT"}])
		ec2.delete_tags(Resources=[instance["instance_id"]],Tags=[{"Key": "WEEKDAY"}])
		ec2.delete_tags(Resources=[instance["instance_id"]],Tags=[{"Key": "HOLIDAY"}])

		# Define tag
		ec2.create_tags(Resources=[instance["instance_id"]],Tags=[{'Key': tag, 'Value': 'True'}])

		# Start the instance
		ec2.start_instances(InstanceIds=[instance["instance_id"]])

	print("Finalized")


def lambda_handler(event, context):

	today = datetime.today()
	# Test in specific day
	#today = datetime.strptime('17/02/20', '%d/%m/%y')

	while True:
		
		####### Weekday #######
		verify = verify_weekday(today)
		
		if verify == True:
			print("Day into Weekday")
			change_instance_type(day_type="holiday_weekday", tag="WEEKDAY")
			break
		
		elif verify == 'WEEKDAY':
			print("Not change aplly, still a Weekday")
			break
		
		####### Holiday #######
		verify = verify_holiday(today)
		
		if verify == True:
			print("Day into Holiday")
			change_instance_type(day_type="holiday_weekday", tag="HOLIDAY")
			break

		elif verify == 'HOLIDAY':
			print("Not change aplly, still a Holiday")
			break

		####### Default day #######
		verify = verify_default(today)

		if verify == True:
			print("Day is default day")
			change_instance_type(day_type="default", tag="DEFAULT")
			break

		elif verify == 'DEFAULT':
			print("Not change aplly, still a Default day")
			break
