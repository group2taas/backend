import unittest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from zapv2 import ZAPv2
import os
from dotenv import load_dotenv

load_dotenv()
ZAP_API_KEY = os.getenv("ZAP_API_KEY")
ZAP_PROXY_SERVER = os.getenv("ZAP_PROXY_SERVER")
CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH")

class OWASP_SecurityTests(unittest.TestCase):

    def setUp(self):
        self.target_url = "<target_url>"  
        self.zap_proxy = ZAP_PROXY_SERVER
        self.results = {}  

        service = Service(executable_path=CHROMEDRIVER_PATH)
        options = webdriver.ChromeOptions()
        options.add_argument(f"--proxy-server={self.zap_proxy}")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--disable-gpu")
        options.add_argument('--disable-webrtc')
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.delete_all_cookies()
        self.zap = ZAPv2(apikey=ZAP_API_KEY, proxies={"http": self.zap_proxy, "https": self.zap_proxy})
        self.zap.core.delete_all_alerts()
        self.run_zap_scans()
        self.alert_count_before = len(self.zap.core.alerts(baseurl=self.target_url))


    def run_zap_scans(self):
        self.zap.spider.scan(self.target_url)
        
        while int(self.zap.spider.status()) < 100:
            time.sleep(2)

        while int(self.zap.pscan.records_to_scan) > 0:
            time.sleep(2)

        self.zap.ascan.scan(self.target_url)
        
        while int(self.zap.ascan.status()) < 100:
            time.sleep(2)

    def tearDown(self):
        self.driver.quit()
        for test in self.results.keys():
            self.generate_summary_report(test)

    def generate_summary_report(self, test_name):
        all_alerts = self.zap.core.alerts(baseurl=self.target_url)
        new_alerts = all_alerts[self.alert_count_before:]           
        severity_counts = {
            "High": 0,
            "Medium": 0,
            "Low": 0,
            "Informational": 0
        }

        for alert in new_alerts:
            severity = alert.get("risk", "Informational")
            if severity in severity_counts:
                severity_counts[severity] += 1
        
        summary_data = {
            "target_url": self.target_url,
            "security_alerts": severity_counts,
            "test_case": test_name,
            "result": self.results[test_name]
        }

        print(summary_data)

if __name__ == "__main__":
    unittest.main()
