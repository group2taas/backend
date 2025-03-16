from django.db import models, transaction
from tickets.models import Ticket
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.core.files.base import File, ContentFile
import os
import pypandoc
import tempfile
from loguru import logger
from collections import defaultdict
from gdstorage.storage import GoogleDriveStorage

gd_storage = GoogleDriveStorage()


def upload_to(instance, filename):
    return os.path.join(
        "results",
        str(instance.user.pk),
        str(instance.ticket.pk),
        str(instance.pk),
        filename,
    )


class Result(models.Model):
    title = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="results")
    num_tests = models.PositiveIntegerField(default=0)
    logs = models.JSONField(default=list)
    progress = models.PositiveIntegerField(default=0)
    security_alerts = models.JSONField(default=dict)
    alerts_detail = models.JSONField(default=list)
    markdown = models.FileField(
        upload_to=upload_to,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=["md"])],
        storage=gd_storage,
    )
    pdf = models.FileField(
        upload_to=upload_to,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
        storage=gd_storage,
    )

    def add_log(self, test_log):
        with transaction.atomic():
            result = Result.objects.select_for_update().get(id=self.id)
            result.logs.append(test_log)
            result.progress = len(result.logs)
            result.save(update_fields=["logs", "progress"])

    def update_test_results(self, result_data):
        with transaction.atomic():
            result = Result.objects.select_for_update().get(id=self.id)

            if "security_alerts" in result_data:
                result.security_alerts = result_data["security_alerts"]

            if "alert_details" in result_data:
                result.alerts_detail = result_data["alert_details"]

            result.save(update_fields=["security_alerts", "alerts_detail"])

    def generate_markdown(self):

        md = f"# OWASP Security Test Summary\n\n"

        for idx, log in enumerate(self.logs, start=1):
            log_type = log.get("type", "")

            if log_type == "error":
                test_case = log.get("test_case", "Unknown Test")
                message = log.get("message", "")
                md += f"## {idx}. {test_case} \n"
                md += f"{message}"

            elif log_type == "result":
                target_url = log.get("target_url", "Unknown URL")
                severity_counts = log.get("security_alerts", defaultdict(int))
                alert_details = log.get("alert_details", [])
                test_case = log.get("test_case", "Unknown Test")
                result = log.get("result", "No result")

                md += f"## {idx}. {test_case} \n"
                md += f"**Target URL:** `{target_url}`\n\n"

                md += "### Security Alert Summary\n"
                md += f"- **High Alerts:** {severity_counts['High']}\n"
                md += f"- **Medium Alerts:** {severity_counts['Medium']}\n"
                md += f"- **Low Alerts:** {severity_counts['Low']}\n"
                md += f"- **Informational Alerts:** {severity_counts['Informational']}\n\n"

                md += "### Alert Details\n"
                if alert_details:
                    for alert in alert_details:
                        md += f"- {alert}\n"
                md += "\n"

                md += "### Other Result\n"
                md += f"{result}\n\n"

            else:
                logger.info(f"Skipping this log: {log}")
                continue

            # page break
            md += "\f\n\n"

        return md

    def md2pdf(self, markdown_content):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_file:
            tmp_filepath = tmp_file.name
            pypandoc.convert_text(
                markdown_content, "pdf", format="md", outputfile=tmp_filepath
            )
        return tmp_filepath

    def save_overall_test_results(self):
        if self.logs:
            try:
                markdown_content = self.generate_markdown()
            except Exception as e:
                logger.info(f"Failed to generate markdown. {e}")
                return

            try:
                pdf_tmppath = self.md2pdf(markdown_content)
            except Exception as e:
                logger.info("Failed to generate PDF. {e}")
                return

            try:
                md_filename = f"{self.title}_results.md"
                md_file = ContentFile(markdown_content.encode("utf-8"))
                self.markdown.save(md_filename, md_file, save=False)

                pdf_filename = f"{self.title}_results.pdf"
                with open(pdf_tmppath, "rb") as f:
                    pdf_file = File(f)
                    self.pdf.save(pdf_filename, pdf_file, save=False)

                os.remove(pdf_tmppath)

                self.save(update_fields=["markdown", "pdf"])
                logger.info("Markdown and PDF files saved successfully.")

            except Exception as e:
                logger.info(f"Failed to save markdown/pdf files. {e}")
                return

    def get_alert_counts(self):
        """Returns alert counts by severity"""
        return self.security_alerts or {
            "High": 0,
            "Medium": 0,
            "Low": 0,
            "Informational": 0,
        }

    def __str__(self):
        return self.title
