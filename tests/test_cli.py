import os

from bddcli import status, stderr, stdout, when

from boilerplate.auth.models import Member


def test_cli_insert_basedata(app, cliapp, mockupfs, freshdb):
    filename = 'boilerplate'
    fsroot = mockupfs(**{
        filename: f'db: {{url: {freshdb}}}'
    })
    configfile = os.path.join(fsroot, filename)

    with cliapp(f'-c {configfile} db basedata insert'):
        assert not stderr
        assert stdout
        assert status == 0

        with app.db.session() as session:
            assert session.query(Member).count() == 2
            assert session.query(Member).filter_by(name='God').one().email == \
                'god@example.com'

        # Duplicate
        when()
        assert stderr
        assert status == 1

        with app.db.session() as session:
            assert session.query(Member).count() == 2
            assert session.query(Member).filter_by(name='God').one().email == \
                'god@example.com'


def test_cli_insert_mockupdata(app, cliapp, mockupfs, freshdb):
    filename = 'boilerplate'
    fsroot = mockupfs(**{
        filename: f'db: {{url: {freshdb}}}'
    })
    configfile = os.path.join(fsroot, filename)

    with cliapp(f'-c {configfile} db mockup insert'):
        assert not stderr
        assert stdout
        assert status == 0

        with app.db.session() as session:
            assert session.query(Member).count() == 2
            assert session.query(Member).filter_by(name='Bob').one().email == \
                'bob@example.com'
