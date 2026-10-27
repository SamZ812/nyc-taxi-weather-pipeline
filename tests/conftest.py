import boto3
import pytest
from moto import mock_aws

@pytest.fixture
def s3_client(monkeypatch):
    monkeypatch.delenv("AWS_ENDPOINT_URL", raising=False)
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "testing")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "testing")
    monkeypatch.setenv("AWS_DEFAULT_REGION", "us-east-1")

    with mock_aws():
        client = boto3.client("s3")
        client.create_bucket(Bucket="raw")
        yield client