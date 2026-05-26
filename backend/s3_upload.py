import boto3

AWS_ACCESS_KEY = "AKIAT3H7RDDM4XW4IREH"
AWS_SECRET_KEY = "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"

BUCKET_NAME = "ai-resume-analyzer-project"

s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)


def upload_to_s3(file, filename):

    s3.upload_fileobj(
        file,
        BUCKET_NAME,
        filename
    )

    file_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{filename}"

    return file_url