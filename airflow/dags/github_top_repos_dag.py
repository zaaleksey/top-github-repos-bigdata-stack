import json
from datetime import datetime

import requests
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from airflow.operators.sqlite_operator import SqliteOperator
from airflow.providers.sqlite.hooks.sqlite import SqliteHook

from config import token

headers = {'Authorization': f'token {token}'}


def get_orgs(num_of_orgs):
    orgas_with_repos_urls: dict[int, str] = {}
    since = 0
    num_of_requests = _get_number_of_requests(num_of_orgs)

    url = "https://api.github.com/organizations"
    params = {'per_page': 100}

    for _ in range(num_of_requests):
        params['since'] = since
        response = requests.get(url, headers=headers, params=params).json()
        data = {org['id']: org['repos_url'] for org in response}
        orgas_with_repos_urls.update(data)
        since = response[-1]['id']

    return json.dumps(orgas_with_repos_urls)


def _get_number_of_requests(number_of_organizations):
    if number_of_organizations < 100:
        return 1
    elif number_of_organizations % 100 == 0:
        return number_of_organizations // 100
    else:
        return number_of_organizations // 100 + 1


def get_repos(orgas_with_repos_urls):
    urls = json.loads(orgas_with_repos_urls).values()
    repos_data = []
    for url in urls:
        params = {'page': 1}
        data = []
        response = requests.get(url, headers=headers, params=params).json()
        while response:
            params["page"] += 1
            data.extend(map(_mapping_repo, response))
            response = requests.get(url, headers=headers, params=params).json()
        repos_data.extend(data)

    return json.dumps(repos_data)


def _mapping_repo(repo):
    return {
        'id': repo['id'],
        'org_name': repo['owner']['login'],
        'repo_name': repo['name'],
        'stars_count': repo['stargazers_count'],
    }


def get_top_repos(repos_data, top_num):
    repos_data = json.loads(repos_data)
    top_repos = sorted(repos_data, key=lambda repo: repo['stars_count'], reverse=True)[:top_num]
    return json.dumps(top_repos)


def insert_top_repos_in_db(repos_data):
    repos_data = json.loads(repos_data)
    sqlite_hook = SqliteHook()

    for repo in repos_data:
        parameters = [repo['id'], repo['org_name'], repo['repo_name'], repo['stars_count']]
        sqlite_hook.run("""
        INSERT INTO top_repos (id, org_name, repo_name, stars_count) VALUES (?, ?, ?, ?)
        """, parameters=parameters, autocommit=True)


with DAG(
        dag_id='github_top_repos',
        start_date=datetime(2021, 1, 1),
        schedule_interval="@hourly",
        catchup=False
) as dag:
    drop_table = SqliteOperator(
        task_id='drop_table',
        sql="""
        DROP TABLE IF EXISTS top_repos;
        """
    )

    pull_orgs = PythonOperator(
        task_id='pull_orgs',
        python_callable=get_orgs,
        op_kwargs={
            'num_of_orgs': int(Variable.get("number_of_organizations"))
        }
    )

    pull_repos = PythonOperator(
        task_id='pull_repos',
        python_callable=get_repos,
        op_kwargs={
            'orgas_with_repos_urls': "{{ ti.xcom_pull(task_ids='pull_orgs') }}"
        }
    )

    top_repos = PythonOperator(
        task_id='top_repos',
        python_callable=get_top_repos,
        op_kwargs={
            'repos_data': "{{ ti.xcom_pull(task_ids='pull_repos') }}",
            'top_num': int(Variable.get("top_repositories"))
        }
    )

    create_top_table = SqliteOperator(
        task_id='create_top_table',
        sql="""
        CREATE TABLE top_repos (
            id INT PRIMARY KEY,
            org_name TEXT,
            repo_name TEXT,
            stars_count INT
        );
        """
    )

    insert_data_in_db = PythonOperator(
        task_id='insert_data_in_db',
        python_callable=insert_top_repos_in_db,
        op_kwargs={
            'repos_data': "{{ ti.xcom_pull(task_ids='top_repos') }}"
        }
    )

    drop_table >> create_top_table
    pull_orgs >> pull_repos >> top_repos >> create_top_table
    create_top_table >> insert_data_in_db
