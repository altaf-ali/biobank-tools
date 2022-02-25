"""Console script for biobank."""

from pathlib import Path
from typing import List

import typer

from biobank.dataset import Dataset


class AlertMarkers:
    """CLI alert markers."""

    error = typer.style("x ", fg=typer.colors.RED)
    success = typer.style("✓ ", fg=typer.colors.GREEN)
    warning = typer.style("! ", fg=typer.colors.YELLOW)


class Commands(typer.Typer):
    """CLI Command base class."""

    def __init__(self, **kwargs):
        """Constructor."""
        super().__init__(**kwargs)
        self.dataset = Dataset()

    def validate_dataset(self):
        if not self.dataset.path.exists():
            self.exit("Dataset does not exist. Please import a dataset first.")

    def exit(self, message, *args, **kwargs):
        self.alert_error(message, *args, **kwargs)
        raise typer.Exit()

    def echo(self, message, *args, **kwargs):
        typer.echo(message, *args, **kwargs)

    def alert(self, success, message, *args, **kwargs):
        if success:
            return self.alert_success(message, *args, **kwargs)
        else:
            return self.alert_error(message, *args, **kwargs)

    def alert_error(self, message, *args, **kwargs):
        self.echo(AlertMarkers.error + message, *args, **kwargs)

    def alert_success(self, message, *args, **kwargs):
        self.echo(AlertMarkers.success + message, *args, **kwargs)

    def alert_warning(self, message, *args, **kwargs):
        self.echo(AlertMarkers.warning + message, *args, **kwargs)


commands = Commands()


@commands.command(name="import")
def import_dataset(path: str, force: bool = False) -> None:
    """Import biobank dataset."""
    if commands.dataset.path.exists():
        if force:
            commands.dataset.delete()
        else:
            commands.exit(
                "Dataset already imported. Use --force to overwite it."
            )
    commands.dataset.import_dataset(path)


@commands.command()
def exclude(files: List[Path], force: bool = False) -> None:
    """Exclude from biobank dataset."""
    commands.validate_dataset()
    commands.dataset.exclude(files)


@commands.command()
def select(
    fields: List[str] = typer.Argument(None),
    limit: int = None,
    output: Path = None,
) -> None:
    """Select fields from a dataset."""
    commands.validate_dataset()
    dataset = commands.dataset.select(fields, limit)
    if dataset.empty:
        commands.exit("No matching fields found.")

    if output:
        print(f"writing {output}")
        dataset.to_csv(output)
    else:
        print(dataset)


@commands.command()
def fields(
    fields: List[str] = typer.Argument(None),
    search: str = None,
    output: Path = None,
) -> None:
    """Show dataset fields."""
    commands.validate_dataset()
    dictionary = commands.dataset.filter_dictionary(fields, search)
    if dictionary.empty:
        commands.exit("No matching fields found.")

    if output:
        print(f"writing {output}")
        dictionary.to_csv(output, index=False)
    else:
        print(dictionary[["FieldID", "ValueType", "Units", "Field"]])


if __name__ == "__main__":
    commands()  # pragma: no cover
