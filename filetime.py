import os
from pathlib import Path


def get_filepaths(directory: str) -> list[Path]:
    path = Path(directory)
    filepaths = [file for file in path.glob('**/*') if file.is_file()]
    return filepaths


def sort_filepaths(filepaths: list[Path]) -> list[Path]:
    return sorted(filepaths)


def get_alpha_dirlist(directory: str) -> list[Path]:
    filepaths = get_filepaths(directory)
    sorted_filepaths = sort_filepaths(filepaths)
    return [filepath for filepath in sorted_filepaths]
