from typing import Optional, TypedDict, NamedTuple
from io import StringIO


class CFG(TypedDict):
    packages: list[str]
    default_package: str
    outfile: StringIO
    set_hook: Optional[bool]


class File(NamedTuple):
    path: str
    is_package: bool
    code: str
    timestamp: int
