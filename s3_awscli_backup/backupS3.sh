#!/bin/bash
# 
# Example in cron
#	00 22 * * * /directory/backupS3.sh > /var/log/backupS3.log 2>&1
#

BUCKET_NAME="leonardobiffi"
DIRECTORY_REMOTE=""
DIRECTORY_LOCAL="/home/leonardo/mytec"
AWS_CLI="/usr/local/bin/aws"
TIMESTAMP=$(date +"%F %T")
LOGFILE="/home/leonardo/mytec/aws-utils/s3_awscli_backup/s3.log"
UPLOAD_LOG="/home/leonardo/mytec/aws-utils/s3_awscli_backup/upload.log"
S3_DIRECTORY="s3://$BUCKET_NAME/$DIRECTORY_REMOTE"

# command execute
$AWS_CLI s3 sync $DIRECTORY_LOCAL $S3_DIRECTORY > $UPLOAD_LOG

if [ $? -eq 0 ];then
   echo "Backup Completed Successfully at $TIMESTAMP"  >> "$LOGFILE"
else
   echo "Backup Failed at $TIMESTAMP"  >> "$LOGFILE"
fi