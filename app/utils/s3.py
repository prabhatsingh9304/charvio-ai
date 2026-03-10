import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import logging
from typing import Optional, BinaryIO
from app.core.config import settings

logger = logging.getLogger(__name__)

def get_s3_client():
    """Create and return an S3 client."""
    if not settings.AWS_ACCESS_KEY_ID or not settings.AWS_SECRET_ACCESS_KEY:
        logger.warning("AWS credentials not configured")
        return None
        
    return boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION
    )

def upload_file_to_s3(file_obj: BinaryIO, filename: str, content_type: Optional[str] = None) -> Optional[str]:
    """
    Upload a file-like object to S3.
    
    Args:
        file_obj: Binary file-like object (must support read())
        filename: Destination filename in S3
        content_type: MIME type of the file
        
    Returns:
        str: Public URL of the uploaded file, or None if failed
    """
    s3_client = get_s3_client()
    if not s3_client:
        return None
        
    if not settings.AWS_BUCKET_NAME:
        logger.error("AWS_BUCKET_NAME not configured")
        return None

    try:
        extra_args = {}
        if content_type:
            extra_args['ContentType'] = content_type

        # Upload the file
        s3_client.upload_fileobj(
            file_obj,
            settings.AWS_BUCKET_NAME,
            filename,
            ExtraArgs=extra_args
        )

        # Generate the URL
        url = f"https://{settings.AWS_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{filename}"
        return url

    except NoCredentialsError:
        logger.error("Credentials not available")
        return None
    except ClientError as e:
        logger.error(f"S3 upload error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error uploading to S3: {e}")
        return None
