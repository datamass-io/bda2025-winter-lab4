import os
import json
import uuid

import psutil
import time

from azure.identity import DefaultAzureCredential
from azure.cosmos import CosmosClient
from dotenv import load_dotenv

load_dotenv()

# for database management use azure-mgmt-cosmosdb
database_name = "iot"
container_name = "monitoring"
database_endpoint = "https://mdtest4321.documents.azure.com:443/"
try:
    print("Hello, Azure CosmosDB!")
    # credential = DefaultAzureCredential()
    # client = CosmosClient(url=database_endpoint, credential=credential)

    # or use connection string
    cosmos_key = os.getenv('COSMOS_KEY')
    client = CosmosClient(url=database_endpoint, credential=cosmos_key)

    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)
    ID = str(uuid.uuid4())
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    data = {
        "id": ID,
        "system": "work",   # try to create data for other system, e.g. "work"
        "timestamp": timestamp,
        "cpu_usage": cpu,
        "mem_usage": mem,
    }

    print("Creating item...")
    container.create_item(data)

    print("Querying item...")
    QUERY = "SELECT * FROM monitoring m WHERE m.id = @id"
    params = [dict(name="@id", value=ID)]
    results = container.query_items(
        query=QUERY, parameters=params, enable_cross_partition_query=False
    )
    items = [item for item in results]
    output = json.dumps(items, indent=True)
    print("Result list\t", output)
    
    # Query by system property instead of id
    print("Querying item by system property...")
    QUERY = "SELECT * FROM monitoring m WHERE m.system = @system"
    params = [dict(name="@system", value="work")]
    results = container.query_items(
        query=QUERY, 
        parameters=params, 
        enable_cross_partition_query=True 
    )
    items = [item for item in results]
    output = json.dumps(items, indent=True)
    print("Result list\t", output)

except Exception as ex:
    print("Exception: ")
    print(ex)
