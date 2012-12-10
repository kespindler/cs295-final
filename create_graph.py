#!/usr/bin/env python
import argparse
import matplotlib.pyplot as plt

#plt.plot(x, y)


def read_and_create_graph(files):
    filelines = [open(f).readlines() for f in files]
    for file_index, lines in enumerate(filelines):
        for i, l in enumerate(reversed(lines)):
            if l.startswith('BEGIN'):
                line_index = i
                break
        filelines[file_index] = lines[line_index+1:]
    xs = list(range(len(filelines[0]))) + filelines
    plt.plot(zip(*xs))
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='+')
    parsed = parser.parse_args()
    read_and_create_graph(parsed.files)


