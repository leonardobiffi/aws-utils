#!/bin/bash
# 
# Example in cron
#	00 22 * * * /directory/backupS3.sh > /var/log/backupS3.log 2>&1
#

BUCKET_NAME="leonardobiffi"
DIRECTORY_REMOTE=""
DIRECTORY_LOCAL="/home/leonardo/mytec"
LOG_FILE="/home/leonardo/mytec/aws-utils/s3_awscli_backup/s3.log"
LOG_UPLOAD="/home/leonardo/mytec/aws-utils/s3_awscli_backup/upload.log"
AWS_CLI="/usr/local/bin/aws"
TIMESTAMP=$(date +"%F %T")

S3_DIRECTORY="s3://$BUCKET_NAME/$DIRECTORY_REMOTE"

# command execute
$AWS_CLI s3 sync $DIRECTORY_LOCAL $S3_DIRECTORY > $LOG_UPLOAD

if [ $? -eq 0 ];then
   echo "Backup Completed Successfully at $TIMESTAMP"  >> "$LOG_FILE"
else
   echo "Backup Failed at $TIMESTAMP"  >> "$LOG_FILE"
fi