import json
from bson import ObjectId
from agents.base.model_handler import AIModelHandler
from interviews.models.interview import Interview
from .prompts import ANALYSIS_PROMPT, ZAP_TEMPLATE_SCRIPT
from .kafka_producer import send_to_testing
from tickets.models import Ticket
from loguru import logger
import re


class AnalysisAgent:
    def __init__(self):
        self.model_handler = AIModelHandler()

    def analyze_interview(self, interview_id):
        interview = Interview.objects.get(id=interview_id)
        answers_qs = interview.answers.all()

        interview_answers = ""
        for answer in answers_qs:
            question_text = getattr(answer.question, "text", str(answer.question))
            interview_answers += f"Question: {question_text}\nAnswer: {answer.body}\n\n"

        prompt = ANALYSIS_PROMPT.format(
            template_script=ZAP_TEMPLATE_SCRIPT, interview_answers=interview_answers
        )

        print("Prompt being sent to model:", prompt)
        raw_output = self.model_handler.query_model(prompt)
        print("Raw model output:", raw_output)

        parsed_output = self._parse_output(raw_output)
        num_test_cases = self._get_num_test_cases(parsed_output)

        ticket = interview.ticket
        ticket.status = "testing"
        ticket.save()

        interview.save()

        send_to_testing(
            {
                "interview_id": interview.id,
                "analysis_result": parsed_output,
                "num_test_cases": num_test_cases,
            }
        )

        return interview

    def _parse_output(self, raw_output):
        try:
            match = re.search(
                r"```(?:python)?\s*(.*?)\s*```", raw_output, flags=re.DOTALL
            )
            if match:
                code = match.group(1)
            else:
                code = raw_output
            return code.strip()
        except Exception as e:
            logger.warning("Failed to parse raw data from model: {}", e)
            return "Error: Failed to parse model output"

    def _get_num_test_cases(self, code):
        test_functions = re.findall(r"^\s*def\s+(test_\w+)\s*\(", code, re.MULTILINE)
        return len(test_functions)
