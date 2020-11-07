#!/usr/bin/env python

import dask
import numpy as np

from dask import delayed
from dask.distributed import Client

import argparse
import time

class DataSource(object):
    def __init__(self):
        self._sleeps = np.random.randint(1, 60, 300)

    @delayed(nout=2)
    def run(self, filename):
        arr = []
        choice = np.random.choice(self._sleeps, 1)[0]
        
        for i in range(choice):
            with open(filename, "rb") as fh:
                arr += [int(b) for b in fh.read(choice)]

        #time.sleep(choice)
        return (arr, arr[0])

if __name__ == "__main__":
    a = argparse.ArgumentParser()
    a.add_argument("filename")
    args = a.parse_args()

    cli = Client(n_workers=4)
    ds = DataSource()

    for i in range(100):
        x_arr = []
        y_arr = []

        fut = ds.run(args.filename)
        res = dask.compute()
