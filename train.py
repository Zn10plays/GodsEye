from ultralytics import YOLO
import argparse
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument('-m', '-model', required=False)
parser.add_argument('-t', '-type')
parser.add_argument('-epoch', default=500)
parser.add_argument('-b', '-batch_size', default=32)

options = parser.parse_args(sys.argv[1:])

print(options.m)

