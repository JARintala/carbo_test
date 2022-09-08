# Install:
# https://docs.microsoft.com/en-us/azure/cosmos-db/local-emulator?tabs=ssl-netstd21

# python -m pip install --upgrade pip
# python -m pip install azure-cosmos
# python -m pip install aio-cosmos

import json
from dataClasses.CarbonData import CarbonData
from azure.cosmos.aio import CosmosClient as cosmos_client
from azure.cosmos import PartitionKey, CosmosClient, exceptions


class CarbonRepository:
    # <add_uri_and_key>
    endpoint = "https://localhost:8081"
    key = "C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw=="
    # </add_uri_and_key>

    # <define_database_and_container_name>
    database_name = "CarbonDatabase"
    container_name = "CarbonContainer"
    # </define_database_and_container_name>

    # <create_database_if_not_exists>
    def get_or_create_db(self, client, database_name):
        try:
            database_obj = client.get_database_client(database_name)
            database_obj.read()
            return database_obj
        except exceptions.CosmosResourceNotFoundError:
            print("Creating database")
            return client.create_database(database_name)

    # </create_database_if_not_exists>

    # Create a container
    # Using a good partition key improves the performance of database operations.
    # <create_container_if_not_exists>
    def get_or_create_container(self, database_obj, container_name):
        try:
            todo_items_container = database_obj.get_container_client(container_name)
            todo_items_container.read()
            return todo_items_container
        except exceptions.CosmosResourceNotFoundError:
            print("Creating container with id as partition key")
            return database_obj.create_container(
                id=container_name,
                partition_key=PartitionKey(path="/id"),
                offer_throughput=400,
            )
        except exceptions.CosmosHttpResponseError:
            raise

    # </create_container_if_not_exists>

    # <method_populate_container_items>
    def populate_container_items(self, container_obj, carbonData: CarbonData):
        # <create_item>
        try:
            data = json.dumps(carbonData, default=vars)
            data_ad_dict = json.loads(data)
            inserted_item = container_obj.create_item(data_ad_dict)
            print("Inserted item for carbonData. Item Id: " + inserted_item["id"])
        except exceptions.CosmosHttpResponseError as e:
            print("\npopulate_container_items caught an error. {0}".format(e.message))
        except Exception as e:
            print(
                "\npopulate_container_items has caught an error. {0}".format(e.message)
            )
        # </create_item>

    # </method_populate_container_items>

    # <method_read_items>
    def read_items(self, container_obj, carbonData: CarbonData):
        # <read_item>
        try:
            item_response = container_obj.read_item(
                item=carbonData.id, partition_key=carbonData.id
            )
            request_charge = container_obj.client_connection.last_response_headers[
                "x-ms-request-charge"
            ]
            print(
                "Read item with id {0}. Operation consumed {1} request units".format(
                    item_response["id"], (request_charge)
                )
            )
        except Exception as e:
            print(
                "\npopulate_container_items has caught an error. {0}".format(e.message)
            )
        # </read_item>

    # </method_read_items>

    # <method_query_items>
    def query_items(self, container_obj, query_text):
        # enable_cross_partition_query should be set to True as the container is partitioned
        # In this case, we do have to await the asynchronous iterator object since logic
        # within the query_items() method makes network calls to verify the partition key
        # definition in the container
        # <query_items>
        query_items_response = container_obj.query_items(
            query=query_text, enable_cross_partition_query=True
        )
        request_charge = container_obj.client_connection.last_response_headers[
            "x-ms-request-charge"
        ]
        items = [item for item in query_items_response]
        print(
            "Query returned {0} items. Operation consumed {1} request units".format(
                len(items), request_charge
            )
        )
        # </query_items>

    # </method_query_items>

    # <save_carbonData>
    def save_carbonData(self, carbonData: CarbonData):
        # <create_cosmos_client>
        client = CosmosClient(self.endpoint, credential=self.key)
        # </create_cosmos_client>
        try:
            # create a database
            database_obj = self.get_or_create_db(client, self.database_name)
            # create a container
            container_obj = self.get_or_create_container(
                database_obj, self.container_name
            )
            # populate the carbonData item in container
            self.populate_container_items(container_obj, carbonData)
            # read the just populated item using their id and partition key
            self.read_items(container_obj, carbonData)
            # Query these item using the SQL query syntax.
            query = "SELECT * FROM c WHERE c.id = '" + carbonData.id + "'"
            self.query_items(container_obj, query)
        except Exception as e:
            print("\nrun_sample has caught an error. {0}".format(e.message))
        finally:
            print("\nQuickstart complete")

    # </run_sample>

    # <python_main>
    # if __name__=="__main__":
    #    loop = asyncio.get_event_loop()
    #    loop.run_until_complete(run_sample())
    # <python_main>
