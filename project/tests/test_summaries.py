import json


def test_create_summary(test_app_with_db):
    response = test_app_with_db.post('/summaries/', data=json.dumps({'url': 'https://foo.bar'}))
    assert response.status_code == 201
    assert response.json()['url'] == 'https://foo.bar'


def test_create_summary_invalid_json(test_app_with_db):
    response = test_app_with_db.post('/summaries/', data=json.dumps({}))
    assert response.status_code == 422
    assert response.json() == {
        'detail': [
            {
                'loc': ['body', 'url'],
                'msg': 'field required',
                'type': 'value_error.missing'
            }
        ]
    }


def test_read_summary(test_app_with_db):
    response = test_app_with_db.post('/summaries/', data=json.dumps({'url': 'https://foo.bar'}))
    summary_id = response.json()['id']
    assert response.status_code == 201

    response = test_app_with_db.get(f'/summaries/{summary_id}')
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict['id'] == summary_id
    assert response_dict['url'] == 'https://foo.bar'
    assert response_dict['summary']
    assert response_dict['created_at']


def test_read_summary_incorrect_id(test_app_with_db):
    response = test_app_with_db.get('/summaries/999/')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Summary not found'


def test_read_all_summaries(test_app_with_db):
    added_summaries = []
    response = test_app_with_db.post('/summaries/', data=json.dumps({'url': 'https://foo1.bar'}))
    assert response.status_code == 201
    added_summaries.append(response.json()['id'])
    response = test_app_with_db.post('/summaries/', data=json.dumps({'url': 'https://foo2.bar'}))
    assert response.status_code == 201
    added_summaries.append(response.json()['id'])

    response = test_app_with_db.get('/summaries/')
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda x: x['id'] in added_summaries, response_list))) == 2
