# Copyright 2022 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from kfp.v2.dsl import component


@component(
    base_image="python:3.7",
    packages_to_install=["google-cloud-bigquery==2.30.0"],
)
def bq_query_to_table(
    query: str,
    bq_client_project_id: str,
    dataset_location: str = "EU",
) -> None:
    """
    Run query & create a new BigQuery table
    Args:
        query (str): SQL query to execute, results are saved in a BigQuery table
        bq_client_project_id (str): project id that will be used by the bq client
        dataset_location (str): bq dataset location
        required by the bq query operation. No need to specify destination param
    Returns:
        None
    """
    from google.cloud.exceptions import GoogleCloudError
    from google.cloud import bigquery
    import logging

    logging.getLogger().setLevel(logging.INFO)

    job_config = bigquery.QueryJobConfig()

    bq_client = bigquery.client.Client(
        project=bq_client_project_id, location=dataset_location
    )
    query_job = bq_client.query(query, job_config=job_config)

    try:
        result = query_job.result()
        logging.info(f"BQ Job finished")
    except GoogleCloudError as e:
        logging.error(e)
        logging.error(query_job.error_result)
        logging.error(query_job.errors)
        raise e
