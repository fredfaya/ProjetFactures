import re

from Files_preprocessors.pdf_to_txt_convertor import convert_pdf_to_txt


def verify_infos_extracted(infos: dict, path_to_file: str) -> dict:
    """
    Verify that all the information extracted are present in the file.
    :param path_to_file:
    :param infos: dictionary with extracted information
    :return: dictionary with verified information
    """

    text = convert_pdf_to_txt(path_to_file)
    for key, value in infos.items():
        if not isinstance(value, list):
            values = re.split(r"\s|,|\.", value)
            for item in values:
                if item not in text:
                    infos[key] = 'unknown'
                    break
        else:
            for item in value:
                if item not in text:
                    infos[key] = 'unknown'
                    break

    return infos
