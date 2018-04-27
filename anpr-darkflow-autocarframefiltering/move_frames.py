import boto3
import datetime
import os
import common
from botocore.exceptions import ClientError
from os import listdir
from os.path import isfile, join

# In order for this script to work make sure of the following:
# 1. This script is located in the directory one level above the directory containing the car frames.
# 2. AWS CLI is configured with the right credentials.
s3 = boto3.client('s3')
BUCKET_NAME = "tapway-vint-courtyard"
#PATH_WITHIN_BUCKET = "kirthi_frames_test/" #boto3-testfolder/" # This path must exist within the bucket. (e.g tapway-vint-courtyard/path/)
PATH_WITHIN_BUCKET = "kirthi_frames_test/"
DEFAULT_PATH_WITHIN_BUCKET = "frames-test/"

def todayDate():
    now = datetime.datetime.now()
    return now.strftime("%H-%d-%m-%Y")
    #return now.strftime("%Y-%m-%d")

def todayBucketPath():
    return PATH_WITHIN_BUCKET + todayDate() + "/"

def check_bucket_exists(s3, bucket, key):
    try:
        s3.head_object(Bucket=bucket, Key=key)
    except ClientError as e:
        return False
    return True

def moveFrames():
    bucket_path = DEFAULT_PATH_WITHIN_BUCKET # default bucket path and must be created beforehand.
    s3_daily_path = todayBucketPath() #
    if check_bucket_exists(s3, BUCKET_NAME, s3_daily_path):
        bucket_path = s3_daily_path
    else:
        # Create daily bucket.
        try:
            s3.put_object(Bucket=BUCKET_NAME,Body='',Key=s3_daily_path)
            bucket_path = s3_daily_path
        except Exception as e:
            print(e)
            print("{0} Daily bucket could not be created".format(str(datetime.datetime.now())))
    os.system("aws s3 mv {} s3://{} --recursive".format(common.CARS_PATH, BUCKET_NAME+'/'+bucket_path))

def main():
    moveFrames()

main()
