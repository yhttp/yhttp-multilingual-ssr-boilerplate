"""Mock and test the Google OAuth2.0

References:
- https://developers.google.com/identity/protocols/oauth2/web-server
"""
import json
from unittest import mock
from urllib.parse import parse_qsl, unquote

from bddrest import status, response, when

from boilerplate.auth.models import Member


class RespMock:

    def __init__(self, status, json=None):
        self.status_code = status
        self.json = lambda: json

    @property
    def text(self):
        return json.dumps(self.json())


def test_google(httpreq, app):
    # Try without refresh token
    with httpreq('/tokens/google/oauth2'):
        assert status == 302
        cookie = response.headers['Set-Cookie'].split(';')[0]
        assert cookie.startswith('yhttp-csrf-token=')

        location = response.headers['location']
        path, query = location.split('?')
        assert path == 'https://accounts.google.com/o/oauth2/v2/auth'

        params = dict(parse_qsl(query))
        assert 'client_id' in params
        assert 'response_type' in params
        assert 'scope' in params
        assert 'redirect_uri' in params
        assert 'state' in params
        assert 'access_type' in params
        assert 'login_hint' not in params

        # Try with refresh token
        when(
            title='Obtain OAuth2.0 token with refresh token',
            headers=dict(cookie=f'yhttp-refresh-token={refreshtoken}')
        )
        assert status == 302
        cookie = response.headers['Set-Cookie'].split(';')[0]
        assert cookie.startswith('yhttp-csrf-token=')
        location = response.headers['location']
        path, query = location.split('?')
        assert path == 'https://accounts.google.com/o/oauth2/v2/auth'

        params = dict(parse_qsl(query))
        assert 'client_id' in params
        assert 'response_type' in params
        assert 'scope' in params
        assert 'redirect_uri' in params
        assert 'state' in params
        assert 'access_type' in params
        assert params['login_hint'] == 'god@example.com'

        when(
            title='`redurl` has invalid format',
            query=dict(redurl='maformed')
        )
        assert status == '400 redurl: Invalid Format'

        when(
            title='`redurl` is empty',
            query=dict(redurl='')
        )
        assert status == '400 redurl: Length must be between 7 and 2048 ' \
            'characters'

    cbquery = dict(
        code='4/0AX4XfWitAl4eZ2U7eJ7CYbFgl0HrKjUxrAuD5TiXfOV1ZHfcSWjxM1u6z'
             '_w8IZMXlLuJLg',
        scope='email+profile+https://www.googleapis.com/auth/userinfo.email'
              '+https://www.googleapis.com/auth/userinfo.profile+openid',
        state=params['state'],
    )

    tokenresp = RespMock(200, json=dict(
        id_token=idtoken,
        access_token='accesstoken-fake',
        refresh_token='refreshtoken-fake',
    ))

    with mock.patch('httpx.post', return_value=tokenresp) as tokenmock, \
            httpreq('/tokens/callbacks/google', query=cbquery,
                    headers={'Cookie': cookie}):
        assert status == 302
        location = response.headers['location']
        assert unquote(location) == app.settings.root

        cookie = response.headers['Set-Cookie'].split(';')[0]
        assert cookie.startswith('yhttp-refresh-token=')

        with app.db.session() as session:
            member = session.query(Member) \
                .filter_by(email='god@example.com').one()

            assert member.name == 'god'
            assert member.nickname == 'god'
            assert member.locale == 'en-US'
            assert member.oauth2_avatar == 'https://awesome.avatar'
            assert member.oauth2_refreshtoken == 'refreshtoken-fake'
            assert member.oauth2_accesstoken == 'accesstoken-fake'

        tokenmock.assert_called_with(
            'https://oauth2.googleapis.com/token',
            data={
                'code': '4/0AX4XfWitAl4eZ2U7eJ7CYbFgl0HrKjUxrAuD5TiXfOV1ZHf'
                        'cSWjxM1u6z_w8IZMXlLuJLg',
                'client_id': 'foobarbaz',
                'client_secret': '12345678901234567890123456789012',
                'redirect_uri': 'http://localhost:8080/tokens/google/cb',
                'grant_type': 'authorization_code'
            }
        )

        # Login again
        when(title='Login again')
        assert status == 302

        tokenmock.return_value = RespMock(403)
        when(title='Google say 403 during key exchange')
        assert status == 401

        tokenmock.return_value = RespMock(400)
        when(title='Google say 400 during key exchange')
        assert status == 401

        # Malformed id_token
        tokenmock.return_value = RespMock(200, json=dict(
            id_token='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.e30.Xu_sWESYaAuv0'
                     'WOxMPW53WA8nNsmPEylF__ce_NE3L4'
        ))
        when(title='Token received from google is malformed')
        assert status == 401

    with httpreq('/tokens', verb='CREATE', headers={'Cookie': cookie}):
        assert status == 200
        assert response.json['token'] is not None


# created using:
"""
boilerplate auth c 1 '{"refresh": true, "email": "god@example.com"}'
"""
refreshtoken = \
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEiLCJleHAiOjE3NzM2NjIwM' \
    'TMsInJlZnJlc2giOnRydWUsImVtYWlsIjoiZ29kQGV4YW1wbGUuY29tIn0.LW2NRnA55hG' \
    '9POJZbmKkRQP1QXiivCB5KMoqvAUz858'


# created using:
"""
boilerplate auth c 1 '{"email": "god@example.com", \
    "picture": "https://awesome.avatar", "locale": "en-US", "name": "god"}'
"""
idtoken = \
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEiLCJleHAiOjE3NzM2NjIwN' \
    'TYsImVtYWlsIjoiZ29kQGV4YW1wbGUuY29tIiwicGljdHVyZSI6Imh0dHBzOi8vYXdlc29' \
    'tZS5hdmF0YXIiLCJsb2NhbGUiOiJlbi1VUyIsIm5hbWUiOiJnb2QifQ.B2-QanKlhuqhNw' \
    '17qh5rxoBeq52xl6aLA_vWfe1rr5U'
