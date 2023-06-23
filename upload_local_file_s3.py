import boto3
import sys
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def connect_get_credentials(role_arn: str, role_session_name: str = "AssumedRoleSession"):
    """Connect to AWS STS and get credentials from assumed role.
    
    Arguments:
        role_arn {str} -- ARN of the role to assume.
        role_session_name {str} -- Name of the role session.
    
    Returns:
        boto3.client -- S3 client with assumed role credentials.
    """
    # Connect to STS
    sts_client = boto3.client('sts')
    
    # Assume role
    response = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName=role_session_name
    )
    
    # Get credentials from assumed role
    credentials = response['Credentials']
    access_key = credentials['AccessKeyId']
    secret_key = credentials['SecretAccessKey']
    session_token = credentials['SessionToken']
    
    # Create S3 client with assumed role credentials
    s3_client = boto3.client(
        's3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        aws_session_token=session_token
    )
    
    return s3_client


def upload_file_to_s3(s3_client, bucket_name: str, file_name: str):
    """Upload a file to S3.
    
    Arguments:
        s3_client {boto3.client} -- S3 client with assumed role credentials.
        bucket_name {str} -- Name of the bucket.
        file_name {str} -- Name of the file to upload.
    """
    try:
        # Upload file to S3
        s3_client.upload_file(file_name, bucket_name, file_name)
        logger.info(f"Successfully uploaded {file_name} to {bucket_name}")
        
        return "Success"
    except Exception as e:
        logger.error(f"Failed to upload {file_name} to {bucket_name}")
        logger.error(e)
        sys.exit(1)


def main(role_arn: str, role_session_name: str, bucket_name: str, file_name: str):
    """Main function."""
    # Connect to S3 and get credentials from assumed role
    s3_client = connect_get_credentials(role_arn, role_session_name)
    
    # Upload file to S3
    upload_file_to_s3(s3_client, bucket_name, file_name)


if __name__ == "__main__":
    # Set up boto3 client
    role_arn = 'arn:aws:iam::123456789012:role/role-name'
    role_session_name = 'role-session-name'
    
    # Set up S3 bucket and file name
    bucket_name = 'bucket-name'
    file_name = 'file-name'
    
    # Call the main function
    main(role_arn, role_session_name, bucket_name, file_name)
