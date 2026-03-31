import easycli


class InsertBaseDataCommand(easycli.SubCommand):
    __command__ = 'insert'
    __aliases__ = ['i']

    def __call__(self, args):
        from . import basedata

        app = args.application
        app.ready()
        basedata.insert(app.db)
        app.shutdown()


class BaseDataCommand(easycli.SubCommand):
    __command__ = 'basedata'
    __aliases__ = ['b']
    __arguments__ = [
        InsertBaseDataCommand
    ]


class InsertMockupDataCommand(easycli.SubCommand):
    __command__ = 'insert'
    __aliases__ = ['i']

    def __call__(self, args):
        from . import mockup

        app = args.application
        app.ready()
        mockup.insert(app.db)
        app.shutdown()


class MockupDataCommand(easycli.SubCommand):
    __command__ = 'mockup'
    __aliases__ = ['m']
    __arguments__ = [
        InsertMockupDataCommand
    ]
