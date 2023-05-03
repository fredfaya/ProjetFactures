from GPT.gpt import get_info_from_file
from PDF_preprocessors.pdf_to_txt_convertor import convert_pdf_to_txt
from Texts.rib_extractor import extract_rib
from Texts.info_extracted_verification import verify_infos_extracted


def pipeline_for_no_ocr_pdf(file_path):
    """
    Pipeline for processing pdf files that are not OCR-ed.
    :param file_path: path to pdf file
    :return: dictionary with extracted information
    """
    # convert pdf to txt
    txt_text = convert_pdf_to_txt(file_path)
    # extract information from txt
    infos = get_info_from_file(file_path)
    # extract RIB
    infos['RIB'] = extract_rib(txt_text)
    # verify that all the information extracted are present in the file
    infos = verify_infos_extracted(infos, file_path)

    return infos


if __name__ == '__main__':
    file_path = r'../Files/facture6.pdf'
    info = pipeline_for_no_ocr_pdf(file_path)
    print(info)