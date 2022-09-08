import asyncio
import logging
import uuid
import azure.functions as func
import json
from types import SimpleNamespace
from CarbonRepository import CarbonRepository

# from CarbonRepositoryAsynch import CarbonRepositoryAsynch
from dataClasses.CarbonData import CarbonData
from services.CalculatorService import CalculatorService

# see e.g. https://github.com/kmt112/A2Ztutorial
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    try:
        req_body = req.get_json()
        req_as_str = json.dumps(req_body)

        # carbonDataInstance = CarbonData()
        # carbonDataInstance = json.loads(
        #    req_as_str, object_hook=lambda d: SimpleNamespace(**d)
        # )
        carbonDataInstance: CarbonData = json.loads(
            req_as_str, object_hook=lambda d: SimpleNamespace(**d)
        )

        if carbonDataInstance.id == "":
            carbonDataInstance.id = str(uuid.uuid4())

        carbonRepositoryInstance = CarbonRepository()

        carbonRepositoryInstance.save_carbonData(carbonDataInstance)

        carbonServiceInstance = CalculatorService()
        carbonResult = carbonServiceInstance.SaveCarbondata(carbonDataInstance)
        return carbonResult

    except Exception as e:
        func.HttpResponse(f"Error message: {e}")
