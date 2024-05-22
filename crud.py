from models import *


def add_object(object_, session):
    session.add(object_)
    session.commit()


def get_objects(object_, session):
    objects_data = session.query(object_).all()
    return objects_data


def get_object(object_, id_, session):
    requested_object = session.query(object_).filter(object_.id_ == id_).first()
    return requested_object


def get_comments_by_theme_id(theme_id, session):
    requested_comments = session.query(Comment).filter(Comment.theme_id == theme_id).all()
    return requested_comments


def edit_comment_by_id(comment_id, new_comment, session):
    requested_comment = session.query(Comment).filter(Comment.id_ == comment_id).first()
    requested_comment.author_name = new_comment.author_name
    requested_comment.text = new_comment.text
    requested_comment.quote_id = new_comment.quote_id
    session.commit()
    return requested_comment


def delete_theme_by_id(theme_id, session):
    requested_theme = session.query(Theme).filter(Theme.id_ == theme_id).first()
    session.delete(requested_theme)
    session.commit()
    return requested_theme


def get_themes_lst(session):
    themes_lst = [dict(list(theme.__dict__.items())[1:]) for theme in get_objects(Theme, session)]
    themes_lst = [{'id_': d['id_'], 'name': d['name'], 'description': d['text']} for d in themes_lst]
    themes_lst = [{'id': int(theme['id_']), 'name': theme['name'], 'description': theme['description']} for theme in
                  themes_lst]
    return themes_lst


def get_theme_dict(id_: int, session):
    data_get_theme = [dict(list(get_object(Theme, id_, session).__dict__.items())[1:])]
    data_get_theme = [{'id_': d['id_'], 'name': d['name'], 'description': d['text']} for d in data_get_theme]
    data_get_theme = [{'id': int(theme['id_']), 'name': theme['name'], 'description': theme['description']} for theme in
                      data_get_theme]
    return data_get_theme


def get_comment_by_theme_dict(id_: int, session):
    data_get_comment_by_theme_id = [{"id": d.id_,
                                     "theme_id": d.theme_id,
                                     "author_name": d.author_name,
                                     "text": d.text,
                                     "quote_id": d.quote_id
                                     } for d in get_comments_by_theme_id(id_, session)]
    return data_get_comment_by_theme_id


def get_comment_info_by_id(id_: int, session):
    data_get_comment_by_id = dict(list(get_object(Comment, id_, session).__dict__.items())[1:])
    expected_keys = {'author_name', 'id_', 'quote_id', 'text', 'theme_id'}
    data_get_comment_by_id = dict(item for item in list(data_get_comment_by_id.items()) if item[0] in expected_keys)
    data_get_comment_by_id["id"] = data_get_comment_by_id.pop("id_")
    return data_get_comment_by_id


def edit_comment_test(id_, new_comment, session):
    new_comment_dict = {
        "author_name": new_comment.author_name,
        "text": new_comment.text,
        "quote_id": new_comment.quote_id
    }

    data_test_edit_comment_by_id = edit_comment_by_id(id_, new_comment, session)

    result = {
        "id": data_test_edit_comment_by_id.id_,
        "theme_id": data_test_edit_comment_by_id.theme_id,
        "author_name": data_test_edit_comment_by_id.author_name,
        "text": data_test_edit_comment_by_id.text,
        "quote_id": data_test_edit_comment_by_id.quote_id
    }
    return new_comment_dict, result
