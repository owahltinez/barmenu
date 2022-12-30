#!/bin/env python

import json
import pathlib
import shutil

from absl import app
from absl import logging


def main(_):
  src = pathlib.Path('src')
  public = pathlib.Path('public')

  # Clean the public (output) directory.
  shutil.rmtree(public, ignore_errors=True)

  # Move sources to output.
  shutil.copytree(src, public, ignore=shutil.ignore_patterns('_*.yml'))

  # Create a data file index.
  data_file_index = {}
  for subdir in src.iterdir():
    logging.info('indexing %s', subdir)
    if subdir.is_file(): continue
    data_file_index[subdir.name] = []
    for file_path in subdir.glob('*.yml'):
      logging.info('found %s', file_path)
      if not file_path.name.startswith('_'):
        rel_path = file_path.relative_to(src)
        data_file_index[subdir.name].append(str(rel_path))

  # Write the data file index.
  with open(public / 'index.json', 'w') as fh:
    json.dump(data_file_index, fh)


if __name__ == '__main__':
  app.run(main)
