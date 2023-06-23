# write a class to download s3 bucket

class:

    def __init__():
    
    def download_s3_bucket(access_key, secret_key, bucket_name, file_name):
        s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
        s3.download_file(bucket_name, file_name, file_name):
        """
        Download a file from S3.
        Arguments:
            s3_client {boto3.client} -- S3 client with assumed role credentials.
            bucket_name {str} -- Name of the bucket.
            file_name {str} -- Name of the file to download.

        """
        try:
            # Download file from S3
            s3.download_file(bucket_name, file_name, file_name)
            logger.info(f"Successfully downloaded {file_name} from {bucket_name}")
            return "Success"
        except Exception as e:
            logger.error(f"Failed to download {file_name} from {bucket_name}")
            logger.error(e)
            sys.exit(1)
            
