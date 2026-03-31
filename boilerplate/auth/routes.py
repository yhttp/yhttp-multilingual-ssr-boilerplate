import jwt
import httpx
from yhttp.core import json, statuscode, statuses
import functools
from urllib.parse import quote, urlencode

from ..common import guard
from ..rollup import app
from .models import Member


urlquote = functools.partial(quote, safe='/:?=')


@app.route(r'/tokens/google/oauth2')
@app.queryguard((
    guard.Url('redurl', optional=True),
))
def get(req, *, redurl=None):
    oauthconf = app.settings.oauth
    redurl = urlquote(redurl or app.settings.root)

    query = dict(
        client_id=oauthconf.google.clientid,
        response_type='code',
        scope='openid email profile',
        redirect_uri=f'{app.settings.root}/tokens/google/cb',
        state=app.auth.dump_oauth2_state(req, redurl),
        access_type='offline',
    )

    # login_hint
    refreshtoken = app.auth.read_refreshtoken(req)
    if refreshtoken is not None:
        query['login_hint'] = refreshtoken.email

    querystring = urlencode(query, quote_via=quote)
    url = f'{oauthconf.google.authurl}?{querystring}'
    raise statuses.found(url)


@app.route(r'/tokens/callbacks/google')
@app.queryguard((
    guard.String('code'),
    guard.String('state'),
))
@app.bodyguard(strict=True)
def get(req, *, code=None, state=None):
    state_ = app.auth.verify_oauth2_state(req, state)

    # Exchange for access token
    params = dict(
        code=code,
        client_id=app.settings.oauth.google.clientid,
        client_secret=app.settings.oauth.google.clientsecret,
        redirect_uri=f'{app.settings.root}/tokens/google/cb',
        grant_type='authorization_code'
    )
    resp = httpx.post(
        app.settings.oauth.google.tokenurl,
        data=params,
    )
    if resp.status_code != 200:
        print(f'Google token api error: {resp.status_code}')
        raise statuses.unauthorized()

    tokens = resp.json()
    idtoken = tokens['id_token']
    # TODO: verify id_token if possible
    info = jwt.decode(idtoken, options={"verify_signature": False})
    if 'email' not in info:
        raise statuses.unauthorized()

    email = info['email']
    name = info.get('name')
    locale = info.get('locale')
    avatar = info.get('picture')
    google_refreshtoken = tokens['refresh_token']
    google_accesstoken = tokens['access_token']

    with app.db.session.begin():
        member = Member.ensure(
            app.db.session(),
            email,
            name,
            locale,
            avatar,
            google_refreshtoken,
            google_accesstoken
        )
        member.set_refreshtoken(req)

    raise statuses.found(state_.redurl)


@app.route(r'/tokens')
@app.bodyguard(strict=True)
@json
def create(req):
    refreshtoken = app.auth.verify_refreshtoken(req)

    with app.db.session() as session:
        member = session.query(Member).filter_by(id=refreshtoken.id) \
            .first()

        if member is None:
            raise statuses.unauthorized()

    return dict(
        token=member.create_token(app),
    )


@app.route(r'/tokens')
@app.auth()
@app.bodyguard(strict=True)
def delete(req):
    app.auth.delete_refreshtoken(req)


@app.route(r'/profiles/me')
@app.auth()
@app.bodyguard(strict=True)
@json
def get(req):
    with app.db.session() as session:
        member = session.query(Member).filter_by(id=req.identity.id).first()

    if member is None:
        raise statuses.notfound()

    return member.todict(safe=True)


@app.route(r'/profiles/me')
@app.auth()
@app.bodyguard((
    guard.Nickname('nickname', optional=True),
    guard.Username('name', optional=True),
    guard.Phone('phone', optional=True),
    guard.Locale('locale', optional=True),
    guard.Timezone('timezone', optional=True),
), strict=True)
@json
def update(req):
    """Updates the authenticated user's profile.
    """
    # TODO: invalidate the token and force to refresh it

    session = app.db.session
    member = session.query(Member).filter_by(id=req.identity.id).first()
    if member is None:
        raise statuses.notfound()

    if 'name' in req.form:
        member.name = req.form['name']

    if 'phone' in req.form:
        member.phone = req.form['phone']

    if 'nickname' in req.form:
        member.nickname = req.form['nickname']
        member.nickname_isdirty = False

    if 'locale' in req.form:
        member.locale = req.form['locale']

    if 'timezone' in req.form:
        member.timezone = req.form['timezone']

    session.commit()
    return member.todict(safe=True)


@app.route(r'/publicprofiles')
@app.queryguard((
    guard.Email('email'),
))
@json
@app.auth()
@statuscode('200 Ok')
def get(req):
    with app.db.session() as session:
        member = session.query(Member).filter_by(email=req.query['email']) \
            .first()

    if member is None:
        return []

    return [{
        'nickname': member.nickname,
        'avatar': member.oauth2_avatar
    }]
