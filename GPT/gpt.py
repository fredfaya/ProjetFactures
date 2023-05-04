import re
import openai
import configparser
from typing import Optional

from openai import error

from Files_preprocessors.pdf_to_txt_convertor import convert_pdf_to_txt
from Logs.my_logger import logger


def get_api_key() -> str:
    logger.info("Getting the gpt api key")
    # Créer le parser de configuration
    config = configparser.ConfigParser()

    try:
        # Lire la configuration depuis un fichier
        config.read(
            "D:\Documents\Stage PFE\Projet Factrures\ProjetFacture\Config\gpt_api_connection_config.ini"
        )

        return config.get("gpt", "api_key")
    except configparser.NoSectionError:
        logger.error("An error occurred while reading the configuration file")


def create_prompt(path_to_file: str) -> str:
    logger.info("Creating the prompt")
    prompt = (
        "give me the issuer or sender or bill to name, issuer or sender or bill to address , "
        "delivery or receiver or ship to name, delivery or receiver or ship to address, total amount,"
        " goods origin or country of origin, if they exist in this text : \n"
    )

    prompt += (
            convert_pdf_to_txt(path_to_file=path_to_file)
            + "The output should be like this : \n"
            + "issuer or sender or bill to name : \n"
            + "issuer or sender or bill to address : \n"
            + "delivery or receiver or ship to name : \n"
            + "delivery or receiver or ship to address : \n"
            + "total amount : \n"
            + "goods origin or country of origin : \n"
    )

    return prompt


def is_valid_amount(amount: str) -> bool:
    amount_regex = r"^\d+(?:\.\d+)?\s*KGS*$"
    return False if re.match(amount_regex, amount) else True


def response_to_dict(response: str) -> dict:
    logger.info("Getting responses from the gpt api")
    dict_fields = [
        "expeditor_name",
        "expeditor_address",
        "receiver_name",
        "receiver_address",
        "total_amount",
        "goods_origin",
    ]
    lines = response.strip().split("\n")
    result = {}
    for i, line in enumerate(lines):
        parts = line.split(":")
        key = dict_fields[i]
        if key == "total_amount":
            if is_valid_amount(parts[1].strip()):
                result[key] = parts[1].strip()
            else:
                result[key] = "unknown"
            continue
        value = ":".join(parts[1:]).strip()
        result[key] = value
    return result


def get_info_from_file(path_to_file: str) -> Optional[dict]:
    # recuperer l'api key du fichier de configuration
    openai.api_key = get_api_key()

    prompt = create_prompt(path_to_file=path_to_file)

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.3,
            max_tokens=2000,
        )
        return response_to_dict(response=response.choices[0].text)

    except error.APIConnectionError as e:
        logger.error("An error occurred while connecting to the gpt API")
        raise e
    except error.AuthenticationError as e:
        logger.error("An error occurred while authenticating to the gpt API")
        raise e


if __name__ == "__main__":
    print(get_info_from_file(path_to_file="../Files/facture1.pdf"))
