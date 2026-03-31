import jwt
from bddrest import status, response, when
from freezegun import freeze_time

from boilerplate.auth.models import Member


@freeze_time('2024-08-22')
def test_create_token(httpreq, app):
    refreshtoken = \
        'yhttp-refresh-token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ij' \
        'EiLCJleHAiOjE3NzA5Mzc5NDIsInJlZnJlc2giOnRydWUsImVtYWlsIjoiZ29kQGtvb' \
        'WF4Z2NjLmNvbSJ9.eNWuC0NxRKb5MH8zo9VeBX3DzTHAVO-eqUXOXG4-iYI'

    with httpreq('/tokens', verb='CREATE', headers={'Cookie': refreshtoken}):
        assert status == 401

        with app.db.session.begin():
            member = Member(
                email='god@example.com',
                nickname='god',
                roles=['god', 'admin', 'user'],
            )
            app.db.session.add(member)

        when()
        assert status == 200
        assert response.json['token'] is not None
        token = jwt.decode(
            response.json['token'],
            options={"verify_signature": False}
        )

        assert token['id'] == member.id
        assert member.roles is not None
        assert token['roles'] is not None
        assert token['roles'] == member.roles
