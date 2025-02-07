import json
from bson import ObjectId
from agents.base.model_handler import AIModelHandler
from .models import ClientScopingData
from .prompts import ANALYSIS_PROMPT
from .kafka_producer import send_to_testing
from loguru import logger

class AnalysisAgent:
    def __init__(self):
        self.model_handler = AIModelHandler()
    
    def analyze_client_data(self, scoping_data_id):
        if isinstance(scoping_data_id, ObjectId):
            scoping_data_id = str(scoping_data_id)

        scoping_data = ClientScopingData.objects.get(id=scoping_data_id)
        
        prompt = ANALYSIS_PROMPT.format(
            tech_stack=json.dumps(scoping_data.tech_stack),
            security_concerns=scoping_data.security_concerns,
            client_type=scoping_data.get_client_type_display()
        )

        print("Prompt being sent to model:", prompt)
        raw_output = self.model_handler.query_model(prompt, max_new_tokens=256)
        print("Raw model output:", raw_output)

        scoping_data.analysis_result = self._parse_output(raw_output)
        scoping_data.save()

        send_to_testing({
            "scoping_data_id": scoping_data.id
        })
        
        return scoping_data

    def _parse_output(self, raw_output):
        try:
            return json.loads(raw_output.strip().replace('```json', '').replace('```', ''))
        except json.JSONDecodeError:
            logger.warning("Failed to parse raw data from model.")
            return {"error": "Failed to parse model output"}