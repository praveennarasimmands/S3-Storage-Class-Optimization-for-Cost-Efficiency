import boto3
import logging
from config.s3_config import BUCKET_NAME

# Setup logging
logging.basicConfig(filename='logs/lifecycle_logs.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

def enable_intelligent_tiering(bucket_name):
    s3 = boto3.client('s3')

    storage_class_configuration = {
        'Rules': [
            {
                'ID': 'EnableIntelligentTiering',
                'Status': 'Enabled',
                'Filter': {},
                'Transitions': [],
                'NoncurrentVersionTransitions': [],
                'StorageClassAnalysis': {
                    'DataExport': {
                        'OutputSchemaVersion': 'V_1',
                        'Destination': {
                            'S3BucketDestination': {
                                'Format': 'CSV',
                                'Bucket': f'arn:aws:s3:::{bucket_name}',
                                'Prefix': 'intelligent-tiering-logs/'
                            }
                        }
                    }
                }
            },
        ]
    }

    try:
        # Enable Intelligent-Tiering storage class
        response = s3.put_bucket_storage_class_analysis(
            Bucket=bucket_name,
            StorageClassAnalysis=storage_class_configuration
        )
        logging.info(f"Successfully enabled S3 Intelligent-Tiering for {bucket_name}")
        return response
    except Exception as e:
        logging.error(f"Error enabling Intelligent-Tiering: {e}")
        return None

if __name__ == "__main__":
    enable_intelligent_tiering(BUCKET_NAME)
