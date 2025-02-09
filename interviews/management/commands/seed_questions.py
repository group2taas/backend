from django.core.management.base import BaseCommand
from interviews.models.question import Question 

class Command(BaseCommand):
    help = "Seed the database with default questions."
    def handle(self, *args, **kwargs):
        questions = [
            {"text": "Sensitive Data Handled", "type": Question.SELECT_MULTIPLE, "choices":"Personal Information, Financial Data, Healthcare Information, Government Data, Intellectual Property", "is_required": True},
            {"text": "Data Storage", "type": Question.SELECT_MULTIPLE, "choices":"Local Database, Cloud Storage, Third-party Services, Distributed Systems", "is_required": True},
            {"text": "Number of Endpoints", "type": Question.INTEGER, "is_required": True},
            {"text": "Authentication Required", "type": Question.RADIO, "choices": "Yes, No", "is_required": True},
            {"text": "Rate Limiting", "type": Question.RADIO, "choices": "Yes, No", "is_required": True},
            {"text": "Documentation Available", "type": Question.RADIO, "choices": "Yes, No", "is_required": True},
            {"text": "API Methods Used", "type": Question.SELECT_MULTIPLE, "choices": "GET, POST, PUT, DELETE, PATCH, Other", "is_required": True},
            {"text": "Security Controls Present", "type": Question.SELECT_MULTIPLE, "choices": "WAF, IPS/IDS, Load Balancer, Anti-DDoS, API Gateway", "is_required": True},
            {"text": "Hosting", "type": Question.RADIO, "choices": "Cloud, On-premises, Hybrid", "is_required": True},
            {"text": "Critical Functions", "type": Question.SELECT_MULTIPLE, "choices": "Financial Transactions, User Data Management, Administrative Operations, System Configuration, Report Generation", "is_required": True},
            {"text": "Compliance Requirements", "type": Question.SELECT_MULTIPLE, "choices": "PCI DSS, HIPAA, GDPR, ISO 27001, SOC2, Other", "is_required": True},
            {"text": "Last Security Assessment Date", "type": Question.DATE, "is_required": True},
            {"text": "Known Vulnerabilities", "type": Question.TEXT, "is_required": False},
            {"text": "Time Restrictions", "type": Question.SELECT_MULTIPLE, "choices": "Business Hours Only, 24/7 Allowed, Specific Time Window", "is_required": True},
            {"text": "Testing Limitations", "type": Question.SELECT_MULTIPLE, "choices": "No Destructive Testing, No Automated Scanning, No Performance Testing, Other", "is_required": True},
            {"text": "Required Reports", "type": Question.SELECT_MULTIPLE, "choices": "Executive Summary, Technical Details, Remediation Plan, Compliance Mapping, Risk Rating", "is_required": True},
            {"text": "Project Start Date", "type": Question.DATE, "is_required": True},
            {"text": "Draft Report Due", "type": Question.DATE, "is_required": True},
            {"text": "Final Report Due", "type": Question.DATE, "is_required": True},
            {"text": "Additional Information", "type": Question.TEXT, "is_required": True},
            {"text": "Client Representative", "type": Question.TEXT, "is_required": True},
            {"text": "Date", "type": Question.DATE, "is_required": True},
            {"text": "Security Assessor", "type": Question.TEXT, "is_required": True},
            {"text": "Assessor Date", "type": Question.DATE, "is_required": True},
        ]

        for question_data in questions:
            question, created = Question.objects.get_or_create(
                text=question_data["text"], 
                defaults={
                    "type": question_data["type"],
                    "choices": question_data.get("choices", None),
                    "is_required": question_data["is_required"],
                },
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added question: {question.text}"))
            else:
                self.stdout.write(f"Question already exists: {question.text}")
