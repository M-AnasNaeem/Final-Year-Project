# translation_config.py

import os
from google.cloud import translate_v2 as translate
from config import GOOGLE_CLOUD_CONFIG

def configure_google_cloud():
    # Configure Google Cloud credentials and return a translation client
    
    # Set environment variable with absolute path
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GOOGLE_CLOUD_CONFIG['credentials_path']
    os.environ['GOOGLE_CLOUD_PROJECT'] = GOOGLE_CLOUD_CONFIG['project_id']
    
    # Initialize and return translation client
    try:
        client = translate.Client()
        # Test the client with a simple translation to verify it's working
        test_result = client.translate('test', target_language='es')
        return client
    except Exception as e:
        raise Exception(f"Failed to initialize translation client: {str(e)}")