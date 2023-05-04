from Files_preprocessors.result_saver import dict_to_excel
from GPT.gpt import get_info_from_file
from Files_preprocessors.pdf_to_txt_convertor import convert_pdf_to_txt
from Texts.rib_extractor import extract_rib
from Logs.my_logger import logger


def pipeline(file_path: str) -> None:
    """
    Pipeline for processing pdf files that are not OCR-ed.
    :param file_path: path to pdf file
    :return: dictionary with extracted information
    """
    logger.info("Starting the informations extraction for file : {}".format(file_path))
    try:
        # convert pdf to txt
        txt_text = convert_pdf_to_txt(file_path)
        # extract information from txt
        infos = get_info_from_file(file_path)
        # extract RIB
        infos['RIB'] = extract_rib(txt_text)
        # add the name of the file
        infos['File name'] = file_path.split('/')[-1]
        # save the information in a csv file
        dict_to_excel(infos, r'../results.xlsx')

        logger.info("Information extraction finished for file : {}".format(file_path))
    except Exception as e:
        logger.critical("Information extraction failed for file : {}".format(file_path))


if __name__ == '__main__':
    file_path = r'../Files/facture1.pdf'
    pipeline(file_path)