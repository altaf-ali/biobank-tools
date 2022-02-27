# Tutorial

This tutorial walks you through the following stages of working with UK biobank
data:

- Importing UK biobank data and converting to Parquet format.
- Filtering and exporting the dataset from the command line.
- Loading and filtering the dataset from Python.

## Importing dataset

This tutorial assumes that you have access to UK Biobank data and have
downloaded and extracted the data to either comma separated (.CSV) or tab
separated (.TSV) format.

Use the `biobank import` command to import UK Biobank data.

```console
$ biobank import --help

Usage: biobank import [OPTIONS] FILENAME

  Import biobank dataset.

Arguments:
  FILENAME  [required]

Options:
  --dictionary PATH
  --force / --no-force  [default: no-force]
  --help                Show this message and exit.
```

Depending on the size of the dataset, the import command could take several
minutes.

<div class="termy">

```console
$ biobank import ukb12345.csv

loading dictionary from https://biobank.ctsu.ox.ac.uk
---> 100%
importing ukb12345.csv
---> 100%
saving dataset to .biobank/dataset.parquet
---> 100%
```

</div>

## Working with data dictionary

With Biobank Tools, you can search the data dictionary for fields by ID or by
search terms.

If you already know the field ID, you can check whether the field is available
in your dataset.

```console
$ biobank fields 20006 20007
    FieldID   ValueType        Units                                              Field
849   20006  Continuous  micrometres      Interpolated Year when cancer first diagnosed
850   20007  Continuous  micrometres  Interpolated Age of participant when cancer fi...
```

You can get the same results using regular expressions as well.

```console
$ biobank fields "2000[67]"
    FieldID   ValueType        Units                                              Field
849   20006  Continuous  micrometres      Interpolated Year when cancer first diagnosed
850   20007  Continuous  micrometres  Interpolated Age of participant when cancer fi...
```

If you don't know the field ID, you can use a search term to find the field
IDs.

```console
$ biobank fields --search cancer
    FieldID   ValueType        Units                                              Field
849   20006  Continuous  micrometres      Interpolated Year when cancer first diagnosed
850   20007  Continuous  micrometres  Interpolated Age of participant when cancer fi...
851   20008  Continuous  micrometres  Interpolated Year when non-cancer illness firs...
852   20009  Continuous  micrometres  Interpolated Age of participant when non-cance...
```

Finally, you can combine field ID and search terms to further narrow the
results.

```console
$ biobank fields 200.. --search age
    FieldID   ValueType        Units                                              Field
850   20007  Continuous  micrometres  Interpolated Age of participant when cancer fi...
852   20009  Continuous  micrometres  Interpolated Age of participant when non-cance...
854   20011  Continuous  micrometres  Interpolated Age of participant when operation...
```

## Excluding withdrawn participants

When you receive a list of withdrawn participants, you can exclude them from
the dataset permanently.

<div class="termy">

```console
$ biobank exclude data/w12345_*.csv

removing 20 records from 2 files:
- data/w12345_20220101.csv
- data/w12345_20220201.csv
saving dataset to .biobank/dataset.parquet
---> 100%
```

</div>

## Extracting data

There are two ways to work with dataset created by Biobank Tools.

1. You can export the data to a .CSV file
2. You can load the dataset directly in Python

### Exporting to .CSV

With `biobank select` command, you can export a subset of the dataset that
only contains the fields you're interested in.

<div class="termy">


```console
$ biobank select "2000[67]" --output data/ukb_cancer.csv
---> 100%
writing data/ukb_cancer.csv
```

</div>

If you omit the `--output` option, the `biobank select` command will output the
results to the screen instead.

```console
$ biobank select "2000[67]"
[########################################] | 100% Completed |  9.8s
           20006-0.0    20006-0.1    20006-0.2    20006-0.3    20006-0.4    20006-0.5 20006-1.0 20006-1.1  ... 20007-1.3  20007-2.0  20007-2.1  20007-2.2  20007-2.3  20007-2.4  20007-3.0  20007-3.1
eid                                                                                                        ...
1000016  1951.771450  1959.965254  1959.758862  2108.331238  1793.185997  2052.090334                      ...
1000048  1927.954080  1780.621043  1768.346392  2166.976559  1092.823152  1958.248591                      ...            57.135394  52.331757  49.393116  64.879196  68.577423  51.484781  66.384343
1000057  1783.957575  2055.652053  2055.706534  1854.930873  1398.633216  1942.852454                      ...
1000059  2036.818137  2222.614293  2239.943216  1932.932354  2801.628978  1920.073145                      ...
1000063  2037.248163  2142.236323  2146.492165  2092.512233  1534.692268  1844.065170                      ...
...              ...          ...          ...          ...          ...          ...       ...       ...  ...       ...        ...        ...        ...        ...        ...        ...        ...
9999968  2175.387378  2169.194698  2177.700380  1996.962135  1942.853501  1916.324173                      ...
9999979  1994.938137  1830.922253  1823.217556  1993.885899  1436.625129  1899.035208                      ...
9999980  1958.735897  2086.810754  2103.205981  2000.599709  3291.533833  1963.010565                      ...
9999986  2002.481976  2039.945909  2038.244240  2068.425323  1250.346010  2066.319885                      ...
9999992  1977.196447  1949.820874  1951.181053  1881.749111  2033.254502  1808.468535                      ...

[599995 rows x 34 columns]
```

### Loading dataset in Python

You can load the dataset in Python and apply the same field filters that you
would at the command line. The `select` method returns the data as a Pandas
DataFrame.

```python
from biobank import Dataset

dataset = Dataset()
cancer_data = dataset.select(fields=["2000[67]"])

print(cancer_data)
```

```text
           20006-0.0    20006-0.1    20006-0.2    20006-0.3    20006-0.4    20006-0.5 20006-1.0 20006-1.1  ... 20007-1.3  20007-2.0  20007-2.1  20007-2.2  20007-2.3  20007-2.4  20007-3.0  20007-3.1
eid                                                                                                        ...
1000016  1951.771450  1959.965254  1959.758862  2108.331238  1793.185997  2052.090334                      ...
1000048  1927.954080  1780.621043  1768.346392  2166.976559  1092.823152  1958.248591                      ...            57.135394  52.331757  49.393116  64.879196  68.577423  51.484781  66.384343
1000057  1783.957575  2055.652053  2055.706534  1854.930873  1398.633216  1942.852454                      ...
1000059  2036.818137  2222.614293  2239.943216  1932.932354  2801.628978  1920.073145                      ...
1000063  2037.248163  2142.236323  2146.492165  2092.512233  1534.692268  1844.065170                      ...
...              ...          ...          ...          ...          ...          ...       ...       ...  ...       ...        ...        ...        ...        ...        ...        ...        ...
9999968  2175.387378  2169.194698  2177.700380  1996.962135  1942.853501  1916.324173                      ...
9999979  1994.938137  1830.922253  1823.217556  1993.885899  1436.625129  1899.035208                      ...
9999980  1958.735897  2086.810754  2103.205981  2000.599709  3291.533833  1963.010565                      ...
9999986  2002.481976  2039.945909  2038.244240  2068.425323  1250.346010  2066.319885                      ...
9999992  1977.196447  1949.820874  1951.181053  1881.749111  2033.254502  1808.468535                      ...

[599995 rows x 34 columns]
```
