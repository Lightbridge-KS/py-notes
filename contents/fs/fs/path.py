from pathlib import Path
from typing import Union, List


def path_file(path: Union[str, Path, List[str], List[Path]]) -> Union[Path, List[Path]]:
    """Get filename(s) from path(s).

    Parameters
    ----------
    path : str, Path, or list of str/Path
        Single path or list of paths

    Returns
    -------
    Path or list of Path
        Filename(s) as PosixPath object(s)
    """
    if isinstance(path, (str, Path)):
        return Path(Path(path).name)
    return [Path(Path(p).name) for p in path]