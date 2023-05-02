import openai
import chardet
import configparser


def get_api_key() -> str:
    # Créer le parser de configuration
    config = configparser.ConfigParser()

    # Lire la configuration depuis un fichier
    config.read("D:\Documents\Stage PFE\Projet Factrures\ProjetFacture\Config\gpt_api_connection_config.ini")

    return config.get('gpt', 'api_key')


def get_text_from_txt(path_to_file: str) -> str:
    with open(path_to_file, 'rb') as f:
        result = chardet.detect(f.read())

    with open(path_to_file, 'r', encoding=result['encoding']) as f:
        text = f.read()

    return text


def create_prompt(path_to_file: str) -> str:
    prompt = "give me the issuer or sender or bill to name, issuer or sender or bill to address , " \
             "delivery or receiver or ship to name, delivery or receiver or ship to address, total amount," \
             " goods origin or country of origin, rib if they exist in this text : \n"

    prompt += get_text_from_txt(path_to_file=path_to_file) + "The output should be like this : \n" + \
              "issuer or sender or bill to name : \n" + \
              "issuer or sender or bill to address : \n" + \
              "delivery or receiver or ship to name : \n" + \
              "delivery or receiver or ship to address : \n" + \
              "total amount : \n" + \
              "goods origin or country of origin : \n" + \
              "rib if they exist in this text : \n"

    return prompt


def get_info_from_file(path_to_file: str) -> dict:
    # recuperer l'api key du fichier de configuration
    openai.api_key = get_api_key()

    prompt = create_prompt(path_to_file=path_to_file)

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.3,
        max_tokens=2000,
    )

    return response.choices[0].text


#print(get_info_from_file(path_to_file='../Files/facture2.txt'))
