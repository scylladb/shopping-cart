# Ecommerce API - ScyllaDB & FastAPI sample application
This is a sample ecommerce application built with ScyllaDB and FastAPI.


## Prerequisites
* Python 3

## Get started
Create a new virtual environment:
```
virtualenv env
source env/bin/activate
```

Install Python requirements:
```
pip install fastapi "uvicorn[standard]" scylla-driver
```

Run the server:
```
uvicorn main:app --reload
```

Visit API docs: http://127.0.0.1/docs

![fast api docs](images/apidocs.png)