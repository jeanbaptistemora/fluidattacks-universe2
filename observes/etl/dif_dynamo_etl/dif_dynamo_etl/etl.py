# Standard libraries
from multiprocessing.context import Process
from typing import Any, Dict, Optional
# Third party libraries
import boto3
import botocore
# Local libraries
from dif_dynamo_etl.wrappers import loader
from dif_dynamo_etl.wrappers import transformer
from streamer_dynamodb import extractor
from streamer_dynamodb.extractor import TableSegment


def boto_resource(auth: Dict[str, Any]):
    resource_options: Dict[str, Optional[str]] = {
        'service_name': 'dynamodb',
        'aws_access_key_id': auth['aws_access_key_id'],
        'aws_secret_access_key': auth['aws_secret_access_key'],
        'region_name': auth['region_name'],
        'config': botocore.config.Config(max_pool_connections=50),
    }
    return boto3.resource(**resource_options)


def start_etl(db_client, table_segment: TableSegment, auth: Dict[str, Any]):
    d_pages = extractor.extract_segment(db_client, table_segment)
    t_pages = transformer.transform_pages(d_pages)
    loader.upload_pages(t_pages, 'dynamodb_forces', auth)


def parallel_start_etl(auth: Dict[str, Any], table: str, workers: int = 4):
    db_client = boto_resource(auth)
    processes = []
    for segment in range(workers):
        table_segment = TableSegment(
            table,
            segment,
            workers
        )
        etl_process = Process(
            target=start_etl(db_client, table_segment, auth)
        )
        processes.append(etl_process)
        etl_process.start()
    for process in processes:
        process.join()


def start_new_data_etl(auth: Dict[str, Any]):
    parallel_start_etl(auth, 'FI_forces')


def start_old_data_etl(auth: Dict[str, Any]):
    parallel_start_etl(auth, 'bb_executions')
