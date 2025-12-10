import azure.functions as func
import datetime
import json
import logging
import hmac 
import hashlib
import base64
from io import BytesIO
from graph_requests import Graph 
import asyncio

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="declination_form")
def declination_form(req: func.HttpRequest) -> func.HttpResponse:
    
    try:
        msg = json.loads(req.get_body())
        if "data" in msg:
            data = msg["data"]
            if "envelopeSummary" in data:
                envelope_summary = data["envelopeSummary"]
                if "envelopeDocuments" in envelope_summary:
                    envelope_documents = envelope_summary["envelopeDocuments"]
                    for doc in envelope_documents:
                        if "Flu Declination 2025-2026.pdf" == doc["name"]:
                            pdf_bytes = doc["PDFBytes"].encode("ascii")
                            content = base64.decodebytes(pdf_bytes)
                            file_obj = BytesIO(content)
                            file_name = "FluDeclination.pdf"
                            for recipient in envelope_summary["recipients"]["signers"]:
                                if recipient["recipientId"] == "1":
                                    file_name = f"{recipient["name"]}_{file_name}"

                            with open("config.json", "r") as config_file:
                                ms = Graph(config_file.read())
                                config_file.seek(0)
                                settings = json.loads(config_file.read())
                                shared_lib = settings["sharedLibrary"]

                            vol_flu_decl_folder = "01DMUEVTQ7Z4SMS7FY4NHLAFKZMSHVSYWS"
                            file_obj.seek(0)
                            result = asyncio.run(ms.upload_single_file(parent_id=vol_flu_decl_folder,drive_id=shared_lib,file_name=file_name, file=file_obj))
                            logging.info(f"File Upload Result: {result}")
                            break 

        logging.info(json.dumps(msg, indent=4))

    except (Exception, RuntimeError, TypeError, NameError) as e:
        logging.info(f"Error: {e}")
        return func.HttpResponse("Bad request", status_code=400)

    return func.HttpResponse("Hello", status_code=200)