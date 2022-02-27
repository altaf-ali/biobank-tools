# Installation

## Stable release

To install Biobank Tools, run this command in your
terminal:

<div class="termy">

``` console
$ pip install biobank-tools
---> 100%
Successfully installed biobank-tools
```

</div>


This is the preferred method to install Biobank Tools, as it will always install the most recent stable release.

If you don't have [pip][] installed, this [Python installation guide][]
can guide you through the process.

## From source

The source for Biobank Tools can be downloaded from
the [Github repo][].

You can either clone the public repository:

``` console
$ git clone git://github.com/altaf-ali/biobank-tools
```

Or download the [tarball][]:

``` console
$ curl -OJL https://github.com/altaf-ali/biobank-tools/tarball/master
```

Once you have a copy of the source, you can install it with:

``` console
$ pip install .
```

# Verify installation

Verify that Biobank Tools are installed correctly by running the `biobank`
command.

<div class="termy">

``` console
$ biobank --help
Usage: biobank [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or
                        customize the installation.
  --help                Show this message and exit.

Commands:
  exclude  Exclude from biobank dataset.
  fields   Show dataset fields.
  import   Import biobank dataset.
  select   Select fields from a dataset.
```

</div>


  [pip]: https://pip.pypa.io
  [Python installation guide]: http://docs.python-guide.org/en/latest/starting/installation/
  [Github repo]: https://github.com/altaf-ali/biobank-tools
  [tarball]: https://github.com/altaf-ali/biobank-tools/tarball/master
