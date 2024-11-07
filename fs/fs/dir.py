from pathlib import Path
import fnmatch

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