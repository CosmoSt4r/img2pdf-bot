"""Module for working with files."""
import os


async def delete_files(filenames: list) -> None:
    """
    Delete files with given file names.

    Args:
        filenames: names of files to delete
    """
    for filename in filenames:
        os.remove(filename)
