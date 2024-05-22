from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
import pytest

from route import app
from crud import *
from models import *

client = TestClient(app)

session = sessionmaker(bind=engine)()

data_create_theme = {
    "name": "Hi everyone",
    "description": "My name is Boba"
}


def test_create_theme():
    response = client.post("/theme/", json=data_create_theme)
    assert response is not None
    assert response.status_code == 200
    response = response.json()
    assert response["id"] > 0
    assert response["name"] == data_create_theme["name"]
    assert response["description"] == data_create_theme["description"]


data_create_comment = {
    "author_name": "Bobik",
    "text": "This topic makes me cry",
    "quote_id": -1
}


def test_create_comment():
    response = client.post(f'/comment/{447}', json=data_create_comment)
    assert response is not None
    assert response.status_code == 200
    response = response.json()
    assert response[0]["author_name"] == data_create_comment["author_name"]
    assert response[0]["text"] == data_create_comment["text"]
    assert response[0]["quote_id"] == data_create_comment["quote_id"]


def test_get_themes():
    themes_lst = get_themes_lst(session)
    response = client.get("/themes/")
    assert response is not None
    assert response.status_code == 200
    response = response.json()
    assert response == themes_lst


def test_get_theme():
    data_get_theme = get_theme_dict(447, session)
    response = client.get(f'/theme/{447}')
    assert response is not None
    assert response.status_code == 200
    response = response.json()
    assert response == data_get_theme


def test_get_comments_by_theme_id():
    data_get_comment_by_theme_id = get_comment_by_theme_dict(6, session)
    response = client.get(f'/comment/{6}/comments')
    assert response is not None
    assert response.status_code == 200
    response = response.json()
    assert response == data_get_comment_by_theme_id


def test_get_comment_by_id():
    data_get_comment_by_id = get_comment_info_by_id(95681, session)
    response = client.get(f"/comment/{95681}/details")
    assert response is not None
    assert response.status_code == 200
    response = response.json()
    assert response == data_get_comment_by_id


def test_edit_comment_by_id():
    new_comment = Comment(author_name="Lolik", text="hello im a new member of this forum", quote_id=-1)
    data_test_edit_comment_by_id = edit_comment_test(78956, new_comment, session)
    new_comment = data_test_edit_comment_by_id[0]
    req_response = data_test_edit_comment_by_id[1]
    response = client.put(f"/comment/{78956}/edit", json=new_comment)
    assert response is not None
    assert response.status_code == 200
    response = response.json()
    assert response == req_response


def test_delete_theme_by_id():
    response = client.delete(f"/theme/{830}")
    assert response is not None
    assert response.status_code == 200
    response = response.json()
    assert response['id'] == 830
