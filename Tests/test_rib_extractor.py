import pytest

from Texts.rib_extractor import extract_rib


@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        ("RIB : FR76 3000 3000 3000 3000 3000 300", ['FR76 3000 3000 3000 3000 3000 300']),

        ("DH76 3000 3000 4567 3000 3000", ['DH76 3000 3000 4567 3000 3000']),

        ("Only the products that are identified as such on this document are\nFSC® or PEFC certified FSC: "
         "BV−COC−117918, PEFC: BV/CdC/03−00031\n\nPayment to:BNP Paribas France\nBNP Paribas France\n16, "
         "bd des Italiens, 75009 Paris, FR\nFR76 3000 4015 2900 0200 1160 548\nBNPAFRPPXXX", ['FR76 3000 4015 2900 '
                                                                                              '0200 1160 548']),

        ("Geschäftsführer/CEO: Alexander Pirc, Tom Testa\nProkurist: Yener Agdag\nHandelsregister: Freiburg i.Br. HRB "
         "621154\nSitz der Gesellschaft: 79798 Jestetten\nUSt-IdNr/VAT-ID: DE 177 661 851\n\nBank details : "
         "Commerzbank AG, D-78224 Singen\nUSD account IBAN: DE05 6928 0035 0841 0148 00 BIC : DRESDEFF692\nEUR "
         "account IBAN: DE05 6928 0035 0841 0148 00 BIC : DRESDEFF692\nEUR UBS AG  IBAN: CH20 0028 7287 8141 6960 T "
         "BIC:UBSWCHZH80A\n\nPage of1 1\n\nTEL. +49(0)7745-92799-0\nFAX +49(0)7745-92799-99\ne-mail "
         "info@fssb.de\nwww.fssb.de", ['DE05 6928 0035 0841 0148 00','DE05 6928 0035 0841 0148 00','CH20 0028 7287 '
                                                                                                   '8141 6960 T']),

        ("ACCOUNT NAME : KURLAR DALGIC POMPA SAN.TIC.LTD.STI.\nBANK NAME : ALBARAKA TURK KATILIM BANKASI A.S. / "
         "BRANCH : 085 KOZYATAGI\nIBAN NO : TR80 0020 3000 0184 9572 0000 03\nSWIFT CODE : BTFHTRISXXX ACCOUNT NO : "
         "1849572-3", ['TR80 0020 3000 0184 9572 0000 03'])
    ]
)
def test_extract_rib_should_return_a_rib_when_given_a_text_with_a_rib(input_text, expected_output):
    assert extract_rib(input_text) == expected_output
