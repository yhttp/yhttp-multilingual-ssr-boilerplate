# yhttp multilingual SEO friendly SSR boilerplate with SQLAlchemy


## Install

### Dependencies

- make
- postgresql
- redis-server


## Contibution

### Dependencies
- GNU Make
- [python-makelib](https://github.com/pylover/python-makelib)

### Setup development environment

```bash
make venv
make env
```

Or

```bash
make fresh env
```

#### Virtual environment  activation
```bash
make activate.sh
source activate.sh
```

### Run development server(s)

```bash
make run
```

### i18n

```
boilerplate i18n extract
boilerplate i18n init en_US
boilerplate i18n init fa_IR
boilerplate i18n update
boilerplate i18n compile
```
