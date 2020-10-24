import os
import sys

from dask.dataframe import read_csv


def get_df(filename):
    if not os.path.exists(filename):
        raise RuntimeError("CSV file needs to be provided")

    df = read_csv(filename, blocksize=1024 * 1024)
    return df


if __name__ == "__main__":
    fn = os.path.expandvars(sys.argv[1])
    print(fn)
    get_df(fn)
