from pathlib import Path
import shutil
from typing import Union, List
import os

def file_copy(path: Union[str, Path, List[str], List[Path]], 
              new_path: Union[str, Path, List[str], List[Path]],
              overwrite: bool = True) -> None:
    """Copy file(s) to new location(s).

    Parameters
    ----------
    path : str, Path, or list of str/Path
        Source path(s) to copy from
    new_path : str, Path, or list of str/Path
        Destination path(s) to copy to
    overwrite : bool, optional
        If True, overwrite existing files. If False, raise error if file exists
        Default is True

    Raises
    ------
    ValueError
        If length of source and destination paths don't match
    FileExistsError
        If destination exists and overwrite=False
    FileNotFoundError
        If source file doesn't exist

    Examples
    --------
    >>> file_copy('file.txt', 'backup/file.txt')
    >>> file_copy(['a.txt', 'b.txt'], ['backup/a.txt', 'backup/b.txt'])
    """
    # Convert to lists for unified handling
    src_paths = [Path(path)] if isinstance(path, (str, Path)) else [Path(p) for p in path]
    dst_paths = [Path(new_path)] if isinstance(new_path, (str, Path)) else [Path(p) for p in new_path]

    if len(src_paths) != len(dst_paths):
        raise ValueError("Number of source and destination paths must match")

    for src, dst in zip(src_paths, dst_paths):
        if not src.exists():
            raise FileNotFoundError(f"Source file not found: {src}")
            
        if dst.exists() and not overwrite:
            raise FileExistsError(f"Destination file exists: {dst}")
            
        # Create destination directory if it doesn't exist
        dst.parent.mkdir(parents=True, exist_ok=True)
        
        shutil.copy2(src, dst)