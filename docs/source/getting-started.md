# Getting started

## Prerequisites
* [CQLSH](https://cassandra.apache.org/doc/stable/cassandra/tools/cqlsh.html)
* Python 3
* [ScyllaDB Cloud account](https://cloud.scylladb.com)

## Get started

Clone the repository:

```
git clone https://github.com/zseta/shopping-cart
cd shopping-cart
```

## Create database schema

Connect to your ScyllaDB Cloud cluster using CQLSH and create the schema:

```
cqlsh -u scylla -p <YOUR_PASSWORD> -f schema.cql xxxx.xxxx.xxxx.clusters.scylla.cloud
```

## Set up API server

Create a new virtual environment:
```
virtualenv env
source env/bin/activate
```

Install Python requirements (FastAPI with Uvicorn server and ScyllaDB driver):
```
pip install fastapi "uvicorn[standard]" scylla-driver
```

Modify `config.py` to match your database credentials:

```python
HOST="node-0.aws-us-east-1.xxxx.clusters.scylla.cloud"
USER="scylla"
PASSWORD="xxxxxx"
DATACENTER="AWS_US_EAST_1"
KEYSPACE="ecommerce"
```

Run the server:
```
uvicorn main:app --reload
```

Visit API docs: http://127.0.0.1:8000/docs

![fast api docs](../../images/apidocs.png)