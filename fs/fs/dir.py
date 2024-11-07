from pathlib import Path
import shutil
import fnmatch
import os
from typing import Union, List

def dir_ls(path, recurse=False, glob=None, invert=False):
    """List directory contents with optional recursion and filtering.

    Parameters
    ----------
    path : str or Path
        Directory path to list
    recurse : bool or int, optional
        If True, recurse fully. If int, specifies recursion depth
    glob : str, optional
        Globbing pattern for filtering (e.g. "*.csv")
    invert : bool, optional
        If True, return non-matching files (inverse match)

    Returns
    -------
    list
        List of matching PosixPath objects
    """
    path = Path(path)
    results = []
    
    def should_include(p):
        if glob is None:
            return True
        matches = fnmatch.fnmatch(p.name, glob)
        return not matches if invert else matches
    
    def walk(current_path, current_depth):
        if not current_path.is_dir():
            return
            
        for p in current_path.iterdir():
            if should_include(p):
                results.append(p)  # Now appending PosixPath object directly
                
            if p.is_dir() and (recurse is True or 
                              (isinstance(recurse, int) and current_depth < recurse)):
                walk(p, current_depth + 1)
    
    walk(path, 0)
    return results




def dir_copy(path: Union[str, Path, List[str], List[Path]],
             new_path: Union[str, Path, List[str], List[Path]],
             overwrite: bool = True) -> None:
    """Copy directory/directories recursively to new location(s).

    Parameters
    ----------
    path : str, Path, or list of str/Path
        Source directory path(s) to copy from
    new_path : str, Path, or list of str/Path
        Destination directory path(s) to copy to
    overwrite : bool, optional
        If True, overwrite existing directories. If False, raise error if directory exists
        Default is True

    Raises
    ------
    ValueError
        If length of source and destination paths don't match
    FileExistsError
        If destination exists and overwrite=False
    NotADirectoryError
        If source path is not a directory
    FileNotFoundError
        If source directory doesn't exist

    Examples
    --------
    >>> dir_copy('docs', 'backup/docs')
    >>> dir_copy(['dir1', 'dir2'], ['backup/dir1', 'backup/dir2'])
    """
    # Convert to lists for unified handling
    src_paths = [Path(path)] if isinstance(path, (str, Path)) else [Path(p) for p in path]
    dst_paths = [Path(new_path)] if isinstance(new_path, (str, Path)) else [Path(p) for p in new_path]

    if len(src_paths) != len(dst_paths):
        raise ValueError("Number of source and destination paths must match")

    for src, dst in zip(src_paths, dst_paths):
        if not src.exists():
            raise FileNotFoundError(f"Source directory not found: {src}")
            
        if not src.is_dir():
            raise NotADirectoryError(f"Source path is not a directory: {src}")
            
        if dst.exists():
            if not overwrite:
                raise FileExistsError(f"Destination directory exists: {dst}")
            shutil.rmtree(dst)
            
        # Create parent directory if it doesn't exist
        dst.parent.mkdir(parents=True, exist_ok=True)
        
        shutil.copytree(src, dst)