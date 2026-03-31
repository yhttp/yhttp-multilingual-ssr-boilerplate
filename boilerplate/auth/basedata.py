import datetime


BUILTIN_USERS = [
    ('god', 'god@example.com'),
    ('admin', 'admin@example.com')
]


GODS = [
    'god@example.com',
    'admin@example.com',
]


def insert(db):
    from . import models

    print('generating authentication module\'s base data')
    with db.session() as session:
        for name, email in BUILTIN_USERS:
            print(f'Creating member: {name}')
            member = models.Member(
                nickname=name,
                nickname_isdirty=True,
                email=email,
                name=name.capitalize(),
                created_at=datetime.datetime.now(datetime.UTC),
                modified_at=datetime.datetime.now(datetime.UTC),
            )

            if email in GODS:
                member.roles = ['god']

            session.add(member)
            session.commit()
