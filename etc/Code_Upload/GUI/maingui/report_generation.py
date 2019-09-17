from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from maingui.settings import Report
from enum import Enum
from abc import ABC, abstractmethod
import datetime

REPORT_GENERATOR_VERSION = 0.1


class ReportFormats(Enum):
    PDF = 1
    Markdown = 2
    Text = 3


def get_generation_date():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M")


class ReportGenerator(ABC):

    def __init__(self, report: Report, filename: str):
        self.report = report
        self.filename = filename
        self._c = canvas.Canvas(self.filename, pagesize=A4)

        # Set detault
        self.lmargin = 0.3 * inch
        self._c.setStrokeColorRGB(0, 0, 0)
        self._c.setFillColorRGB(0, 0, 0)
        self._c.setFont("Helvetica", 18)

        super().__init__()

    def generate_report(self):
        """"
        Generate and save the report to disk
        """
        self.report_title()
        self.report_header()  # Abstract, must be defined by subclass
        self.report_results()  # Abstract, must be defined by subclass
        self.report_footer()  # Abstract, must be defined by subclass
        self.save_report()

    def report_title(self):
        """
        Add the title used on all reports
        :return:
        """
        self._c.setStrokeColorRGB(0, 0, 0)
        self._c.setFillColorRGB(0, 0, 0)
        self._c.setFont("Helvetica", 20)
        self._c.drawString(self.lmargin, 11 * inch, "EM Toolkit Report")
        self._c.setFont("Helvetica", 12)
        self._c.drawString(self.lmargin, 10.7 * inch, f"Date: {get_generation_date()}")

    @abstractmethod
    def report_header(self):
        pass

    @abstractmethod
    def report_results(self):
        pass

    @abstractmethod
    def report_footer(self):
        pass

    def save_report(self):
        self._c.showPage()
        self._c.save()


class TechnicanReport(ReportGenerator):

    def __init__(self, report: Report, filename: str):
        super().__init__(report, filename)

    def report_header(self):
        self._c.setStrokeColorRGB(0, 0, 0)
        self._c.setFillColorRGB(0, 0, 0)
        self._c.setFont("Helvetica", 24)
        self._c.drawString(self.lmargin + (2.7 * inch), 10 * inch, "Technician Report")

        self._c.setFont("Helvetica", 16)
        self._c.drawString(self.lmargin, 9 * inch, f"Technician: {self.report.technician}")
        self._c.drawString(self.lmargin, 8.5 * inch, f"Date: {self.report.date}")

    def report_results(self):
        self._c.setFont("Helvetica", 16)
        self._c.drawString(self.lmargin, 7 * inch, "Details:")
        self._c.line(self.lmargin, (6.95 * inch), self.lmargin + (1 * inch), 6.95 * inch)
        details = self.report.details.split("\n")
        self._c.setFont("Helvetica", 14)
        for i, line in enumerate(details):
            self._c.drawString(self.lmargin, (6.5 - (i * 0.3)) * inch, line)

    def report_footer(self):
        pass


class ForensicsReport(TechnicanReport):

    def __init__(self, report: Report, filename: str):
        super().__init__(report, filename)

    # Replace entirely
    def report_header(self):
        self._c.setStrokeColorRGB(0, 0, 0)
        self._c.setFillColorRGB(0, 0, 0)
        self._c.setFont("Helvetica", 24)
        self._c.drawString(self.lmargin, 10 * inch, f"Forenics Report: #{self.report.report_id}")
        self._c.setFont("Helvetica", 16)
        self._c.drawString(self.lmargin, 9 * inch, f"Technician: {self.report.technician}")
        self._c.drawString(self.lmargin, 8.5 * inch, f"Date: {self.report.date}")
        self._c.setFont("Helvetica", 14)
        self._c.drawString(self.lmargin, 8 * inch, f"Generator Version: v{REPORT_GENERATOR_VERSION}")

    def report_signoff(self):
        self._c.drawString(self.lmargin, 2 * inch, f"Sign-off: {self.report.signoff}")
        self._c.line(self.lmargin, (1.6 * inch), self.lmargin + (7 * inch), 1.6 * inch)

    # Specialise
    def generate_report(self):
        self.report_signoff()
        super().generate_report()


ReportTypes = {"Technican Report": TechnicanReport, "Forensics Report": ForensicsReport}

if __name__ == "__main__":
    new_file = "test.pdf"
    r = Report()
    r.technician = "John Smith"
    r.date = "1 April 2019"
    r.location = "RF Lab 1, Cork, Ireland"
    r.details = "ECC Classification for Arduino based IoT devices\nSignal UUID: 2792c9c5-7d77-444d-87da-30df5c3b3446\nScore: 0.9987\nResult: Detected ECC"
    r.signoff = "Dr. Jane Doe"
    r.report_id = "66709"
    rg = ForensicsReport(r, new_file)
    rg.generate_report()
