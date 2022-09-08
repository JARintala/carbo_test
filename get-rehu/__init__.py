# https://stackoverflow.com/questions/67014113/how-to-use-req-get-body-in-azure-function-in-python-and-what-is-purpose
# https://stackoverflow.com/questions/67919944/not-getting-json-input-in-req-get-json-in-azure-function-app-in-python
# https://stackoverflow.com/questions/69676969/how-to-post-json-with-postman-to-azure-functions
import logging

import json

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")
    try:
        req_body = req.get_body().decode(encoding="utf-8")

        return func.HttpResponse(f"{req_body}")
    except Exception as e:
        return func.HttpResponse(f"This HTTP triggered function failed: {e}.")
