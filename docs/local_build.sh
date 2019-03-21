rm -rf _build
rm -rf _autosummary
rm -rf _apidocs

sphinx-apidoc -o _apidocs ../qwikidata
make clean
make html
make html
