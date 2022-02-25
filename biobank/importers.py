"""Implementation of various file importers."""

from abc import ABC, abstractmethod
from pathlib import Path
from urllib.parse import urlsplit

import dask.dataframe as dd
import pyarrow as pa

from biobank.config import settings
from biobank.singleton import Singleton


class UnknownDataFormat(Exception):
    """Unknow dataset exception."""

    def __init__(self, suffix):
        self.suffix = suffix

    def __str__(self):
        """Converts the exception to a printable string."""
        return f"Unknown format '{self.suffix}'"


class ImportManager(metaclass=Singleton):
    """Import manager class."""

    def __init__(self):
        self.importers = dict()

    def register_importer(self, cls, suffix):
        self.importers[suffix] = cls

    @staticmethod
    def register(suffix):
        def registrar(cls):
            importer = ImportManager()
            importer.register_importer(cls, suffix)
            return cls

        return registrar

    def get_suffix(self, path):
        url = urlsplit(path)
        if url.scheme:
            path = url.path

        return Path(path).suffix

    def import_dataset(self, dictionary, path, **kwargs):
        print(f"importing dataset from {path}")
        suffix = self.get_suffix(path)
        try:
            importer = self.importers[suffix](dictionary)
            return importer(path, **kwargs)
        except KeyError:
            raise UnknownDataFormat(suffix)


class DataImporter(ABC):
    """Data importer abstract base class."""

    def __init__(self, dictionary):
        self.dictionary = dictionary

    @abstractmethod
    def __call__(self, path, **kwargs):
        raise NotImplementedError

    def import_dataset(self, path, import_func):
        header = import_func(path)
        columns = dict.fromkeys(header.columns)
        schema = {
            col: self.dictionary.get_type(col) for col, _ in columns.items()
        }
        dtypes = {
            col: self.dictionary.get_pandas_dtype(col)
            for col, _ in columns.items()
        }
        schema[settings.fields.index] = pa.int64()
        dataset = import_func(path, dtype=dtypes)
        dataset = dataset.set_index(settings.fields.index)
        return dataset, schema


@ImportManager.register(".csv")
class CommaSeparated(DataImporter):
    """Comma separated file importer."""

    def __call__(self, path, **kwargs):
        return self.import_dataset(path, import_func=dd.read_csv)


@ImportManager.register(".tsv")
class TabSeparated(DataImporter):
    """Tab separated file importer."""

    def __call__(self, path, **kwargs):
        return self.import_dataset(path, import_func=dd.read_table)
