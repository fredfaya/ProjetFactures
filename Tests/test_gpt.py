from GPT.gpt import is_valid_amount, response_to_dict


def test_is_valid_amount():
    assert is_valid_amount("123.45 KGS") is False
    assert is_valid_amount("123 KGS") is False
    assert is_valid_amount("123") is True
    assert is_valid_amount("123.45") is True
    assert is_valid_amount("123.45 USD") is True
    assert is_valid_amount("EUR 123.45") is True


def test_response_to_dict():
    response = "expeditor_name: John\nexpeditor_address: 123 Main St\nreceiver_name: Jane\nreceiver_address: 456 Elm St\ntotal_amount: 100.00 USD\ngoods_origin: Kyrgyzstan\n"
    expected_output = {
        "expeditor_name": "John",
        "expeditor_address": "123 Main St",
        "receiver_name": "Jane",
        "receiver_address": "456 Elm St",
        "total_amount": "100.00 USD",
        "goods_origin": "Kyrgyzstan",
    }
    assert response_to_dict(response) == expected_output


def test_response_to_dict_invalid_amount():
    response = "expeditor_name: John\nexpeditor_address: 123 Main St\nreceiver_name: Jane\nreceiver_address: 456 Elm St\ntotal_amount: 100.00 KGS\ngoods_origin: Kyrgyzstan\n"
    expected_output = {
        "expeditor_name": "John",
        "expeditor_address": "123 Main St",
        "receiver_name": "Jane",
        "receiver_address": "456 Elm St",
        "total_amount": "unknown",
        "goods_origin": "Kyrgyzstan",
    }
    assert response_to_dict(response) == expected_output
