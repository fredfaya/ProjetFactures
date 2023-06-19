from typing import Optional

from Files_preprocessors.pdf_to_txt_convertor import convert_pdf_to_txt
from GPT.gpt import get_info_from_file
from Logs.my_logger import logger
from Texts.rib_extractor import extract_rib


def pipeline(file_path: str) -> Optional[dict]:
    """
    Pipeline for processing pdf files that are not OCR-ed.
    :param file_path: path to pdf file
    :return: dictionary with extracted information
    """
    logger.warning(
        "Starting the informations extraction for file : {}".format(file_path)
    )
    try:
        # convert pdf to txt
        txt_text = convert_pdf_to_txt(file_path)
        # extract information from txt
        infos = get_info_from_file(file_path)
        # extract RIB
        infos["RIB"] = extract_rib(txt_text)
        # add the name of the file
        infos["File name"] = file_path.split("/")[-1]

        logger.success(
            "Information extraction finished for file : {}".format(file_path)
        )
        return infos
    except Exception as e:
        logger.critical("Information extraction failed for file : {}".format(file_path))
        logger.critical("Error : {}".format(e))
    return None


if __name__ == "__main__":
    file_path = r"../Files/facture8.pdf"
    pipeline(file_path)
