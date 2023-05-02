from pdf2image import convert_from_path


def pdf_to_image_convertor(pdf_path, output_path):
    pages = convert_from_path(pdf_path, 500)
    for page in pages:
        page.save(output_path, 'JPEG')


if __name__ == '__main__':
    pdf_to_image_convertor('Files/facture1.pdf', 'img1.jpg')
