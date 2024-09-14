#!/usr/bin/env python

import sys
import argparse
from .core import process_dfs
from .plot import plot_lightcurve

def main():
    parser = argparse.ArgumentParser(description="lyra CLI")
    parser.add_argument('files', nargs='+', help='Data files to process')
    parser.add_argument('-l', '--labels', nargs='+', help='Labels for each data file')
    parser.add_argument('-t', '--title', type=str, default='Partial Lightcurve', help='Plot title')
    parser.add_argument('-p', '--period', type=float, default=1.0, help='Period of orbit')
    parser.add_argument('-c', '--clean', action='store_true', help='Perform data cleaning')
    args = parser.parse_args()

    if args.labels is None or len(args.labels) != len(args.files):
        print("Error: Number of labels must match the number of files.")
        return

    dataframes = [(args.files[i], args.labels[i]) for i in range(len(args.files))]
    processed_data = process_dfs(dataframes, args.period, clean=args.clean)
    plot_lightcurve(processed_data, title=args.title)

if __name__ == '__main__':
    main()
