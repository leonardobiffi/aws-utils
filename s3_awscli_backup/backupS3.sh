#!/bin/bash

BUCKET_NAME="leonardobiffi"
DIRECTORY_REMOTE=""
DIRECTORY_LOCAL="/home/leonardo/mytec"

timestamp=$(date +"%F %T")
logfile="/home/leonardo/mytec/aws-utils/s3_awscli_backup/s3.log"
UPLOAD_LOG="/home/leonardo/mytec/aws-utils/s3_awscli_backup/upload.log"

S3_DIRECTORY="s3://$BUCKET_NAME/$DIRECTORY_REMOTE"

# command execute
aws s3 sync $DIRECTORY_LOCAL $S3_DIRECTORY > $UPLOAD_LOG

if [ $? -eq 0 ];then
   echo "Backup Completed Successfully at $timestamp"  >> "$logfile"
else
   echo "Backup Failed at $timestamp"  >> "$logfile"
fi