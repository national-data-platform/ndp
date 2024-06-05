from typing import Union
import os
from fastapi import FastAPI

app = FastAPI()
datasets = os.getenv('DATASETS', 'uniform-ensemble')

# Split the string into a list
if datasets is not None:
    datasets_list = datasets.split(',')
else:
    datasets_list = []

print(datasets_list)

@app.get("/")
def read_root():
    return {"datasets": datasets_list}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}