# Zerobooks

Simple desktop based, completely offline, completely free and open source,
invoicing software for linux.

See the [project site](https://codelv.com/projects/zerobooks/) for screenshots. If you find it helpful feel free to [donate](https://codelv.com/donate).

### Install

1. Install python (preferribly in a virtual environment).
2. Clone repo
3. Run `pip install -e ./`

On linux you can optionally run `make install` to install the desktop shortcut.

### Run

Run `alembic upgrade head` to generate a new database.
In the correct virtual env run `zerobooks` or `python -m zerobooks`.


## License

GPL v3.
