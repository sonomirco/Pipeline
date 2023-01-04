import os
import sys
import re
import argparse
import distutils.util
from github import Github

def read_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create player id dataframe")
    # we will parse the list as a string.
    parser.add_argument("--token", type=str, help="The GitHub token")
    
    args = parser.parse_args()
    return args
  
def bump_versions():
    args = read_args()
    print(f"inputs -> {args.token} - type -> {type(args.token)}")
