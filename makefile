docs:
	cd docs
	make html
isort:
	isort zerobooks tests

typecheck:
	mypy zerobooks --ignore-missing-imports
lintcheck:
	flake8 --ignore=E501,W503  zerobooks tests
reformat:
	black zerobooks tests
test:
	pytest -v tests --cov zerobooks --cov-report xml --asyncio-mode auto

precommit: isort reformat lintcheck typecheck

install:
	cp zerobooks/assets/com.codelv.zerobooks.desktop ~/.local/share/applications
	# Replace ~/ with home dir
	sed -i "s!~!${HOME}!g" ~/.local/share/applications/com.codelv.zerobooks.desktop
	# Replace prefix with python prefix
	PY_EXEC_PREFIX=$$(python -c "import sys;print(sys.exec_prefix)"); \
		sed -i "s!%PREFIX%!$${PY_EXEC_PREFIX}!g" ~/.local/share/applications/com.codelv.zerobooks.desktop
	mkdir -p ~/.local/share/zerobooks
	cp zerobooks/assets/icons/icon.svg ~/.local/share/zerobooks/icon.svg
	python -m pip install -e ./
uninstall:
	rm -f ~/.local/share/applications/com.codelv.zerobooks.desktop
	rm -rf ~/.local/share/zerobooks
	python -m pip uninstall -y zerobooks
