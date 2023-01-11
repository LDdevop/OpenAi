def test_get_answer_not_allowed_method_status_code(client):
    assert client.post('/get_answer/<question>', data={'question': 'hello'}).status_code == 200
    assert client.put('/get_answer/<question>', data={'question': 'hello'}).status_code == 200
    assert client.delete('/get_answer/<question>', data={'question': 'hello'}).status_code == 200
    assert client.patch('/get_answer/<question>', data={'question': 'hello'}).status_code == 200


def test_get_answer_not_allowed_method_response(client):
    expected_response = {"success": False,
                         "message": "405 Method Not Allowed: The method is not allowed for the requested URL."}

    assert client.post('/get_answer/<question>', data={'question': 'hello'}).json == expected_response
    assert client.put('/get_answer/<question>', data={'question': 'hello'}).json == expected_response
    assert client.delete('/get_answer/<question>', data={'question': 'hello'}).json == expected_response
    assert client.patch('/get_answer/<question>', data={'question': 'hello'}).json == expected_response
