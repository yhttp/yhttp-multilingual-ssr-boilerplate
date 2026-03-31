import datetime


USERS = [
    ('bob', 'bob@example.com'),
    ('alice', 'alice@example.com')
]


def insert(db):
    from . import models

    print('generating authentication module\'s base data')
    with db.session() as session:
        for name, email in USERS:
            print(f'Creating member: {name}')
            member = models.Member(
                nickname=name,
                nickname_isdirty=True,
                email=email,
                name=name.capitalize(),
                created_at=datetime.datetime.now(datetime.UTC),
                modified_at=datetime.datetime.now(datetime.UTC),
            )

            session.add(member)
            session.commit()
