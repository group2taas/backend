import json
from bson import ObjectId
from agents.base.model_handler import AIModelHandler
from .models import ClientScopingData
from .prompts import TECHNICAL_ANALYSIS_PROMPT
from .kafka_producer import send_to_sales

class TechnicalPreSalesAgent:
    def __init__(self):
        self.model_handler = AIModelHandler()
    
    def analyze_client_data(self, scoping_data_id):
        if isinstance(scoping_data_id, ObjectId):
            scoping_data_id = str(scoping_data_id)

        scoping_data = ClientScopingData.objects.get(id=scoping_data_id)
        
        prompt = TECHNICAL_ANALYSIS_PROMPT.format(
            tech_stack=json.dumps(scoping_data.tech_stack),
            security_concerns=scoping_data.security_concerns,
            client_type=scoping_data.get_client_type_display()
        )

        print("Prompt being sent to model:", prompt)
        raw_output = self.model_handler.query_model(prompt, max_new_tokens=256)
        print("Raw model output:", raw_output)

        send_to_sales({
            "client_id": str(scoping_data.client_id),
            "analysis_result": scoping_data.analysis_result,
            "scoping_data_id": scoping_data.id
        })

        scoping_data.analysis_result = self._parse_output(raw_output)
        scoping_data.save()
        return scoping_data

    def _parse_output(self, raw_output):
        try:
            return json.loads(raw_output.strip().replace('```json', '').replace('```', ''))
        except json.JSONDecodeError:
            return {"error": "Failed to parse model output"}