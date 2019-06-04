#!/usr/bin/env python

from mpi4py import MPI
import argparse
import logging
import sys

if __name__ == "__main__":
    a = argparse.ArgumentParser()
    a.add_argument("m", help="Max number to count to", type=int)
    a.add_argument("-v", "--verbose", default=False, action="store_true")
    args = a.parse_args()
    m = args.m

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    i = 0
    c = 0

    while i < m:
        if rank == 0 and i == 0:
            i += 1
            c += 1
            comm.send(i, dest=rank+1)
            continue

        if rank == 0:
            i = comm.recv(source=size-1)
        else:
            i = comm.recv(source=rank-1)
        logging.debug("{} received {}".format(rank, i))

        if i < m:
            i += 1
            c += 1

        if rank == size - 1:
            comm.send(i, dest=0)
        else:
            comm.send(i, dest=rank+1)

    logging.info("{} made {} counts towards {}".format(rank, c, m))
