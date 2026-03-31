VENV_NAME = boilerplate
PKG_NAME = yhttp-boilerplate
PKG_NAMESPACE = $(PKG_NAME)
PYTEST_FLAGS = -vv
VENV_DELETE_DEPS += www-venv-delete
ENV_DEPS += www-env
ENV_POSTDEPS += completion
PYDEPS_COMMON = \
	'coveralls' \
	'bddrest >= 6.2.3, < 7' \
	'bddcli >= 2.10.1, < 3' \
	'yhttp-dev >= 3.5' \
	'pytest-mock' \
	'freezegun' 


# Assert the python-makelib version
PYTHON_MAKELIB_VERSION_REQUIRED = 2.3


# Ensure the python-makelib is installed
PYTHON_MAKELIB_PATH = /usr/local/lib/python-makelib
ifeq ("", "$(wildcard $(PYTHON_MAKELIB_PATH))")
  MAKELIB_URL = https://github.com/pylover/python-makelib
  $(error python-makelib is not installed. see "$(MAKELIB_URL)")
endif


# Include a proper bundle rule file.
include $(PYTHON_MAKELIB_PATH)/venv-lint-test-webapi.mk


YHTTP_FLAGS = \
	-Odebug=True


.PHONY: www-venv-delete
www-venv-delete:
	make -C www -f Makefile delete-nodemodules

.PHONY: www-env
www-env:
	make -C www -f Makefile env


.PHONY: completion
completion:
	$(PREFIX)/bin/boilerplate completion install --rcfile $(PREFIX)/bin/activate


run:
	$(PREFIX)/bin/boilerplate $(YHTTP_FLAGS) serve \
		--watch-directories 'boilerplate/**' \
		--watch-excludefile '**/*.mako' \
		--subprocess 'make -Cwww run'	
