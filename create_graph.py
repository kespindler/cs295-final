#!/usr/bin/env python
import argparse
import matplotlib.pyplot as plt
import numpy as np

def read_and_create_graph(files, outfname):
    numlist = [np.loadtxt(f, comments='BEGAN') for f in files]
    plt.plot(np.arange(max(len(d) for d in numlist)),numlist[0])
    if outfname:
        plt.savefig(outfname)
    else:
        plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='+')
    parser.add_argument('-o', '--out')
    parsed = parser.parse_args()
    read_and_create_graph(parsed.files, parsed.out)


