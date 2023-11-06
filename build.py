import json
import pathlib
import shutil
import sys
import yaml


def main(_) -> None:
  root = pathlib.Path(".")

  recipe_folders = root.joinpath("recipes").iterdir()
  recipe_folders = [x for x in recipe_folders if x.is_dir()]

  recipes = {}
  for folder in recipe_folders:
    fpaths = folder.glob("*.yml")
    fpaths = [x for x in fpaths if not x.name.startswith("_")]
    recipes[folder.name] = [yaml.safe_load(x.read_text()) for x in fpaths]

  # Delete the output folder.
  output = root / "public"
  shutil.rmtree(output, ignore_errors=True)

  # Copy all the source files.
  shutil.copytree(root / "src", output)

  # Write out the recipes as a single JSON file each.
  for name, fpaths in recipes.items():
    with output.joinpath(f"{name}.json").open("w") as f:
      json.dump(fpaths, f)


if __name__ == "__main__":
  main(sys.argv[1:])
