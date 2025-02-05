import json
from bson import ObjectId
from agents.base.model_handler import AIModelHandler
from agents.analysis_agent.models import ClientScopingData
from loguru import logger

#TBD
class TestingAgent:
    def __init__(self):
        
        pass
    #     self.model_handler = AIModelHandler()

    # def generate_vulnerability_report(self, scoping_data_id):
    #     if isinstance(scoping_data_id, ObjectId):
    #         scoping_data_id = str(scoping_data_id)

    #     scoping_data = ClientScopingData.objects.get(id=scoping_data_id)

    #     prompt = VULNERABILITY_REPORT_PROMPT.format(
    #         analysis = scoping_data.analysis_result["analysis"],
    #         recommendations = scoping_data.analysis_result["recommendations"]
    #     )

    #     logger.info(f"Generating vulnerability report for {scoping_data_id}...")
    #     raw_output = self.model_handler.query_model(prompt, max_new_tokens=256)
    #     logger.debug(f"Raw output for {scoping_data_id}: {raw_output}")

    #     report_result = self._parse_output(raw_output)

    #     vulnerability_report = VulnerabilityReport(
    #         id=scoping_data_id,
    #         client_id = scoping_data.client_id,
    #         report_result = report_result
    #     )
    #     vulnerability_report.save()

    #     send_to_product_manager({
    #         "scoping_data_id": scoping_data_id
    #     })
    #     return
