from tika import parser


def convert_pdf_to_txt(path_to_file: str) -> str:
    parsed_pdf = parser.from_file(path_to_file)
    text = parsed_pdf['content']
    return text.strip()


if __name__ == '__main__':
    print(convert_pdf_to_txt('Files/facture1.pdf'))
