#!/usr/bin/env python

from mpi4py import MPI
import logging
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
i = 0
m = 1024
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
    logging.warn("{} received {}".format(rank, i))

    if i < m:
        i += 1
        c += 1

    if rank == size - 1:
        comm.send(i, dest=0)
    else:
        comm.send(i, dest=rank+1)

logging.warn("{} made {} counts towards {}".format(rank, i, m))
