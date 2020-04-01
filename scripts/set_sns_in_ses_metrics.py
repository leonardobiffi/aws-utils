#!/usr/bin/env python3
import boto3
import time

client = boto3.client('ses')

SNS_TOPIC = 'arn:aws:sns:us-east-1:544440274962:ses_notifications'

response = client.list_identities(
    IdentityType='Domain'
)

for domain in response['Identities']:
	print('Config domain: {}'.format(domain))

	# Enable Fowarding
	response = client.set_identity_feedback_forwarding_enabled(ForwardingEnabled=True, Identity=str(domain))
	
	# Set SNS in Bounce, Complaint, Delivery
	response = client.set_identity_notification_topic(Identity=str(domain), NotificationType='Bounce', SnsTopic=SNS_TOPIC)
	response = client.set_identity_notification_topic(Identity=str(domain), NotificationType='Complaint', SnsTopic=SNS_TOPIC)
	response = client.set_identity_notification_topic(Identity=str(domain), NotificationType='Delivery', SnsTopic=SNS_TOPIC)

	# Enable Headers
	response = client.set_identity_headers_in_notifications_enabled(Identity=str(domain), NotificationType='Bounce', Enabled=True)
	response = client.set_identity_headers_in_notifications_enabled(Identity=str(domain), NotificationType='Complaint', Enabled=True)
	response = client.set_identity_headers_in_notifications_enabled(Identity=str(domain), NotificationType='Delivery', Enabled=True)

	time.sleep(0.5)
