from bddrest import status, response, when
from freezegun import freeze_time

from boilerplate.auth import basedata
from boilerplate.auth.models import Member


@freeze_time('2024-08-22')
def test_profile_update(httpreq, app):
    basedata.insert(app.db)

    # Create a token.
    with app.db.session() as session:
        god = session.query(Member).filter_by(email='god@example.com').one()
        token = god.create_token(app)

    with httpreq(
            path='/profiles/me',
            verb='UPDATE',
            headers={
                'Authorization': f'Bearer {token}'
            },
            form=dict(name='Bob', phone='+98 (912) 111 1111')):
        assert status == 200
        assert response.json == {
            'id': 1,
            'email': 'god@example.com',
            'nickname': 'god',
            'nickname_isdirty': True,
            'name': 'Bob',
            'locale': 'en-US',
            'phone': '+98 (912) 111 1111',
            'avatar': None,
            'timezone': '00:00',
            'roles': ['god'],
            'created_at': '2024-08-22T03:30:00',
            'modified_at': '2024-08-22T03:30:00',
        }

        when(title='Short nickname', form=dict(nickname=''))
        assert status == '400 nickname: Length must be between 3 and 20 ' \
            'characters'

        when(title='Long nickname', form=dict(nickname='x' * 21))
        assert status == '400 nickname: Length must be between 3 and 20 ' \
            'characters'

        when(title='Update nickname', form=dict(nickname='Bob'))
        assert status == 200
        assert response.json['nickname'] == 'Bob'
        assert not response.json['nickname_isdirty']

        when(title='Update locale', form=dict(locale='en-US'))
        assert status == 200
        assert response.json.get('locale') == 'en-US'

        when(title='Update timezone', form=dict(timezone='+03:30'))
        assert status == 200
        assert response.json.get('timezone') == '+03:30'

        # Delete god
        with app.db.session() as session, session.begin():
            god = session.query(Member).filter_by(id=1).one()
            session.delete(god)

        when(title='Member deleted')
        assert status == 404
