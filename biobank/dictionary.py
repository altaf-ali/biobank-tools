"""Dictionary class for managing data dictionary."""

from pathlib import Path
from typing import Any, List

import dask.dataframe as dd
import pandas as pd
import pyarrow as pa
from dask.diagnostics import ProgressBar

from biobank.config import settings


class Dictionary:
    """Dictionary class for managing data dictionary."""

    field_types = {
        "Integer": pa.int64(),
        "Continuous": pa.float64(),
        "Text": pa.string(),
        "Date": pa.string(),  # pa.date64(),
        "Time": pa.string(),  # pa.timestamp("s"),
        "Compound": pa.string(),
        "Categorical single": pa.string(),
        "Categorical multiple": pa.string(),
    }
    filename = "dictionary.parquet"

    def __init__(self, path: Path):
        """Constructor.

        Args:
            path: Directory to store the dictionary
        """
        self._fields = None
        self.path = path / self.filename

    def exists(self) -> bool:
        return self.path.exists()

    @property
    def fields(self):
        if self._fields is not None:
            return self._fields

        dictionary = self.load()
        dictionary["Type"] = dictionary.ValueType.map(self.field_types)
        self._fields = dictionary.set_index(dictionary.FieldID)
        return self._fields

    def filter(self, fields: List[str], search: str) -> pd.DataFrame:
        """Filter dictionary.

        Args:
            fields:
            search:

        Returns:
            None
        """
        dictionary = self.load()
        field_ids = set(map(self.get_field_id, fields))
        dictionary = dictionary[dictionary.FieldID.isin(field_ids)]
        if search:
            dictionary = dictionary[
                dictionary.Field.str.contains(search, case=False)
            ]
        return dictionary

    def load(self, download: bool = False) -> pd.DataFrame:
        if not self.exists() and download:
            self.download()

        dictionary = pd.read_parquet(self.path)
        dictionary.FieldID = dictionary.FieldID.astype(str)
        return dictionary

    def download(self) -> None:
        """Download dictionary from URL.

        Returns:
            None
        """
        print(f"downloading dictionary from {settings.dictionary.url}")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with ProgressBar():
            dictionary = dd.read_table(settings.dictionary.url)
            dictionary = dictionary.compute()
            dictionary.to_parquet(self.path)

    def get_field_id(self, field: str) -> str:
        """Get field ID.

        Args:
            field: Field name

        Returns:
            Field ID as str
        """
        return field.split("-")[0]

    def get_type(self, field) -> pa.DataType:
        """Get Arrow data type for a field.

        Args:
            field: Name of field

        Returns:
            Arrow field type
        """
        field = self.get_field_id(field)
        if field in self.fields.index:
            return self.fields.loc[field].Type

    def get_pandas_dtype(self, field) -> Any:
        """Get Pandas type for a field.

        Args:
            field: Name of field

        Returns:
            Pandas dtype
        """
        field_type = self.get_type(field)
        if not field_type:
            return None

        if field_type == pa.int64():
            return "Int64"  # use pandas nullable integer type

        return field_type.to_pandas_dtype()
