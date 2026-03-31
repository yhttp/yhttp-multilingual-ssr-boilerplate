NPM = pnpm


.PHONY: env
env:
	$(NPM) install


.PHONY: delete-modemodules
delete-nodemodules:
	- rm -r node_modules


env:
.PHONY: run
run:
	$(NPM) run dev


.PHONY: release
release:
	$(NPM) run build
