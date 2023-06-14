from tika import parser
from Logs.my_logger import logger


def convert_pdf_to_txt(path_to_file: str) -> str:
    """
    Function that take a file name and convert the correspnding file to a txt version
    :param path_to_file:
    :return: txt version
    """
    logger.info("Reading and converting the pdf file to txt")
    try:
        parsed_pdf = parser.from_file(path_to_file)
        text = parsed_pdf['content']
        return text.strip()
    except FileNotFoundError as f:
        logger.error("Could not find the file to convert to txt : {}".format(path_to_file))
        raise f


if __name__ == '__main__':
    print(convert_pdf_to_txt('../Files/facture1.pdf'))
