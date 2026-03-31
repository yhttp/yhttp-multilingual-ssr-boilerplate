from bddrest import status, response, when

from boilerplate.auth import basedata
from boilerplate.auth.models import Member


def test_logout(httpreq, app):
    basedata.insert(app.db)

    with httpreq('/tokens', verb='DELETE'):
        assert status == 401

        # Create a token to test successful login
        with app.db.session() as session:
            god = session.query(Member).filter_by(email='god@example.com') \
                .one()

        token = god.create_token(app)
        when(
            headers={
                'Authorization': f'Bearer {token}'
            },
        )
        assert status == 200
        cookie = response.headers['Set-Cookie']
        assert cookie == \
            'yhttp-refresh-token=""; Domain=example.com; ' \
            'expires=Thu, 01 Jan 1970 00:00:00 GMT; ' \
            'HttpOnly; Path=/tokens; SameSite=Strict; Secure'
