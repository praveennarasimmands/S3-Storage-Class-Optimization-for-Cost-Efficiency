import boto3
import logging
from config.s3_config import BUCKET_NAME

# Setup logging
logging.basicConfig(filename='logs/lifecycle_logs.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

def create_lifecycle_policy(bucket_name):
    s3 = boto3.client('s3')

    lifecycle_configuration = {
        'Rules': [
            {
                'ID': 'MoveDataToGlacier',
                'Status': 'Enabled',
                'Prefix': '',  # Apply to all objects
                'Transitions': [
                    {
                        'Days': 30,  # Move to Glacier after 30 days
                        'StorageClass': 'GLACIER'
                    },
                    {
                        'Days': 365,  # Move to Glacier Deep Archive after 1 year
                        'StorageClass': 'GLACIER_DEEP_ARCHIVE'
                    }
                ],
                'Expiration': {
                    'Days': 3650  # Delete objects after 10 years
                },
            },
        ]
    }

    try:
        # Apply lifecycle policy to the bucket
        response = s3.put_bucket_lifecycle_configuration(
            Bucket=bucket_name,
            LifecycleConfiguration=lifecycle_configuration
        )
        logging.info(f"Successfully applied lifecycle policy to {bucket_name}")
        return response
    except Exception as e:
        logging.error(f"Error applying lifecycle policy: {e}")
        return None

if __name__ == "__main__":
    create_lifecycle_policy(BUCKET_NAME)
