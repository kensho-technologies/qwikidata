====================
qwikidata Change Log
====================

v0.2.1
======

**Fixed**:

* typo in string representation of WikidataForm and WikidataSense.

v0.2.0
======

**Removed**:

* Jsonl output support from `WikidataJsonDump` class so that chunks produced by the class can always be read by the class.

v0.1.5
======

**Fixed**:

* Bug that required `datavalue` field in Qualifiers even if `snaktype` is `somevalue` or `novalue`.

v0.1.4
======

**Fixed**:

* Updated docs about module name change (`types` was renamed `typedefs`)

v0.1.3
======

**Fixed**:

* Module that was named `types` was renamed `typedefs`

v0.1.2
======

**Fixed**:

* Bug that prevented json dump file chunks from being compressed

v0.1.1
======

**Added**:

* Updated README with important links


v0.1.0
======

**Added**:

* Support for gz compressed json dump files.
* pre-commit config file.
