import pytest

from ingest.taxi import build_s3_key, build_source_url, file_exists_in_s3, download_file, upload_file_to_s3

@pytest.mark.parametrize(
    ("year", "month", "expected"),
    [
        (2024, 1, "taxi/yellow/year=2024/month=01/yellow_tripdata_2024-01.parquet"),
        (2024, 12, "taxi/yellow/year=2024/month=12/yellow_tripdata_2024-12.parquet"),
    ],
)
def test_build_s3_key(year, month, expected):
    """
    Verify that key gets created with correct format
    """
    assert build_s3_key(year, month) == expected

@pytest.mark.parametrize(
        ("year", "month", "expected"),
        [
            (2024, 1, "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet"),
            (2024, 12, "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-12.parquet")
        ]
)
def test_build_source_url(year, month, expected):
    """
    Verify that url gets created with correct source format
    """
    assert build_source_url(year, month) == expected

def test_file_exists_in_s3_returns_true_when_file_is_present(s3_client):
    bucket_name = "raw"
    s3_key = "my_file.txt"

    s3_client.put_object(Bucket=bucket_name, Key=s3_key, Body=b"hello")

    assert file_exists_in_s3(s3_client, bucket_name, s3_key) is True

def test_file_exists_in_s3_returns_false_when_file_is_missing(s3_client):
    bucket_name = "raw"
    s3_key = "my_file.txt"

    s3_client.create_bucket(Bucket=bucket_name)
    assert file_exists_in_s3(s3_client, bucket_name, s3_key) is False