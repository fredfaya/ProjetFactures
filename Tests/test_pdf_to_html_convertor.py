import os

import pytest
from pdfminer.pdfdocument import PDFTextExtractionNotAllowed

from PDF_preprocessors.pdf_to_html_convertor import PdfToHtmlConvertor


def test_convert_pdf_to_html_should_return_empty_string_when_given_empty_path():
    pdf_to_html_convertor = PdfToHtmlConvertor()

    result = pdf_to_html_convertor.convert_pdf_to_html()

    assert result == "invalid_path"


def test_convert_pdf_to_html_should_return_empty_string_when_given_invalid_path():
    pdf_to_html_convertor = PdfToHtmlConvertor("invalid_path")

    result = pdf_to_html_convertor.convert_pdf_to_html()

    assert result == "invalid_path"


def test_convert_pdf_to_html_should_raise_exception_when_text_extraction_not_allowed():
    # test not work
    pdf_to_html_convertor = PdfToHtmlConvertor("Files/facture6.pdf")

    with pytest.raises(PDFTextExtractionNotAllowed):
        pdf_to_html_convertor.convert_pdf_to_html()


def test_convert_pdf_to_html_should_not_raise_exception_when_text_extraction_allowed():
    pdf_to_html_convertor = PdfToHtmlConvertor("Files/facture1.pdf")

    try:
        pdf_to_html_convertor.convert_pdf_to_html()
    except PDFTextExtractionNotAllowed:
        pytest.fail("An exception was raised when text extraction was allowed")


def test_write_into_file_should_write_html_text_into_file():
    pdf_to_html_convertor = PdfToHtmlConvertor("Files/sample.pdf")
    html_text = "<html><head></head><body><p>Test</p></body></html>"
    pdf_to_html_convertor.html_text = html_text
    path = "test.html"
    pdf_to_html_convertor.write_into_file(path)
    with open(path, "r") as f:
        assert f.read() == html_text
    os.remove(path)
