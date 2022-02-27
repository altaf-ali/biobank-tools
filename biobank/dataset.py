"""Biobank Dataset class."""

import glob
import itertools
import re
import shutil

import dask.dataframe as dd
import numpy as np
import pandas as pd
import pyarrow.parquet as pq
from dask.diagnostics import ProgressBar

from biobank.config import settings
from biobank.dictionary import Dictionary
from biobank.importers import ImportManager


class Dataset:
    """Biobank Dataset class."""

    filename = "dataset.parquet"

    def __init__(self):
        """Constructor."""
        path = settings.path.absolute()
        self.path = path / self.filename
        self.dictionary = Dictionary(path)

    def delete(self) -> None:
        """Delete the dataset.

        Returns:
            None
        """
        if self.path.is_file():
            self.path.unlink()
        else:
            shutil.rmtree(str(self.path))

    def load(self, **kwargs) -> dd.DataFrame:
        """Loads a previously imported Biobank dataset.

        Args:
            **kwargs: Dictionary of keyword arguments

        Returns:
            A Dask DataFrame object
        """
        return dd.read_parquet(str(self.path), **kwargs)

    def save(self, data, schema, **kwargs) -> None:
        """Saves a Biobank dataset.

        Args:
            data: Biobank dataset as a Dask Dataframe
            schema: Parquet schema
            **kwargs: Dictionary of keyword arguments

        Returns:
            None
        """
        print(f"saving dataset to {self.path}")
        data.to_parquet(
            self.path, schema=schema, compression="snappy", engine="pyarrow"
        )

    def load_metadata(self) -> pq.FileMetaData:
        """Loads metadata for the Biobank dataset.

        Returns:
            A FileMetadata object
        """
        return pq.read_metadata(self.path / "_common_metadata")

    def filter_dictionary(self, fields, search):
        return self.dictionary.filter(self.match_fields(fields), search)

    def match_fields(self, fields=None):
        columns = self.load_metadata().schema.names
        if not fields:
            return columns

        pattern = "|".join(map(lambda field: rf"({field}-\d+\.\d+)", fields))
        pattern = rf"^{pattern}$"
        columns = filter(lambda field: re.match(pattern, field), columns)
        return list(columns)

    def import_dataset(self, path, dictionary) -> None:
        """Import a dataset.

        Args:
            path: URL or local path of dataset to import

        Returns:
            None
        """
        self.dictionary.load(dictionary, download=True)
        with ProgressBar():
            import_manager = ImportManager()
            data, schema = import_manager.import_dataset(self.dictionary, path)
        with ProgressBar():
            self.save(data, schema)

    def exclude(self, files):
        files = list(
            itertools.chain(*map(lambda path: glob.glob(str(path)), files))
        )
        exclude = (
            pd.concat(map(lambda file: pd.read_csv(file, header=None), files))
            .set_index(0)
            .index.unique()
        )

        print(f"removing {len(exclude)} records from {len(files)} files:")
        for file in files:
            print(f"- {file}")

        with ProgressBar():
            data = self.load()
            data = data.loc[~data.index.isin(exclude)]
            schema = self.load_metadata().schema.to_arrow_schema()
            schema = {
                name: dtype for name, dtype in zip(schema.names, schema.types)
            }
            self.save(data, schema)

    def select(self, fields=None, limit=None) -> pd.DataFrame:
        """Select specific fields from the Biobank dataset.

        Args:
            fields: List of fields to select
            limit: Number of rows to select

        Returns:
            A Pandas DataFrame
        """
        if fields:
            fields = self.match_fields(fields)
            if not len(fields):
                return pd.DataFrame()
        else:
            fields = None

        with ProgressBar():
            dataset = self.load(columns=fields, use_threads=True)
            dataset = dataset.replace(
                to_replace={
                    col: {np.nan: ""}
                    for col in dataset.select_dtypes(
                        [np.float64, np.datetime64, object]
                    ).columns
                }
            )
            dataset = dataset.compute()
            if limit:
                dataset = dataset.iloc[:limit]

        return dataset
