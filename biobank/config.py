"""Biobank Dataset class."""

from pathlib import Path
from typing import Any, Tuple

import yaml
from pydantic import AnyUrl, BaseModel, BaseSettings
from pydantic.env_settings import SettingsSourceCallable


class FieldsConfig(BaseModel):
    """Fields config."""

    index: str


class DictionaryConfig(BaseModel):
    """Dictionary config."""

    url: AnyUrl


class Settings(BaseSettings):
    """Package settings."""

    debug: bool = False
    path: Path = Path(".biobank")
    fields: FieldsConfig
    dictionary: DictionaryConfig

    class Config:
        """Configuration loader."""

        config_dir = "conf"
        config_file = "config.yaml"

        @classmethod
        def file_settings(cls, settings: BaseSettings) -> dict[str, Any]:
            package_dir = Path(__file__).parent.absolute()
            config_file = package_dir / cls.config_dir / cls.config_file
            if config_file.is_file():
                with open(config_file) as f:
                    return yaml.safe_load(f)
            else:
                return settings.dict()

        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> Tuple[SettingsSourceCallable, ...]:
            return init_settings, cls.file_settings


settings = Settings()
