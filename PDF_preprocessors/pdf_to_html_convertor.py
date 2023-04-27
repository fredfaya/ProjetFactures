import os

from pdfminer.converter import HTMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from io import StringIO

from pdfminer.pdfpage import PDFPage


class PdfToHtmlConvertor:
    def __init__(self, pdf_file_path: str = "") -> None:
        self.pdf_file_path = pdf_file_path
        self.html_text = ""

    def convert_pdf_to_html(self) -> str:
        if not os.path.exists(self.pdf_file_path):
            return "invalid_path"
        output_string = StringIO()

        try:
            with open(self.pdf_file_path, "rb") as in_file:
                resource_manager = PDFResourceManager()
                la_params = LAParams()
                converter = HTMLConverter(
                    resource_manager, output_string, laparams=la_params
                )
                page_interpreter = PDFPageInterpreter(resource_manager, converter)

                for page in PDFPage.get_pages(in_file):
                    page_interpreter.process_page(page)

                converter.close()
                self.html_text = output_string.getvalue()

            return self.html_text

        except PDFTextExtractionNotAllowed as e:
            print(e)

    def write_into_file(self, path: str) -> None:
        with open(path, "wb") as out_file:
            out_file.write(self.html_text.encode("utf-8"))
