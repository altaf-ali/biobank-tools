# Biobank Tools


[![pypi](https://img.shields.io/pypi/v/biobank-tools.svg)](https://pypi.org/project/biobank-tools/)
[![python](https://img.shields.io/pypi/pyversions/biobank-tools.svg)](https://pypi.org/project/biobank-tools/)
[![Build Status](https://github.com/altaf-ali/biobank-tools/actions/workflows/dev.yml/badge.svg)](https://github.com/altaf-ali/biobank-tools/actions/workflows/dev.yml)
[![codecov](https://codecov.io/gh/altaf-ali/biobank-tools/branch/main/graphs/badge.svg)](https://codecov.io/github/altaf-ali/biobank-tools)

* Documentation: <https://altaf-ali.github.io/biobank-tools>
* GitHub: <https://github.com/altaf-ali/biobank-tools>
* PyPI: <https://pypi.org/project/biobank-tools/>


## Features

The Biobank Tools package provides simple, fast, and efficient access to UK
Biobank data. Once you've downloaded and extracted the UK Biobank data to
comma or tab separated files, you can use Biobank Tools to convert the data
to a format that's better suited for searching and filtering than plain text
files. Internally, Biobank Tools convert the data to [Apache Parquet][]
format for optimized column-wise access.

## Requirements

Biobank Tools require Python 3.8 or above.

## Credits

This package was created with [Cookiecutter][] and the [altaf-ali/cookiecutter-pypackage][] project template.

[Apache Parquet]: https://parquet.apache.org/documentation/latest
[Cookiecutter]: https://cookiecutter.readthedocs.io/en/latest/
[altaf-ali/cookiecutter-pypackage]: https://altaf-ali.github.io/cookiecutter-pypackage
