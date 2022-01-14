from io import StringIO
import os
import string
import json
from typing import NamedTuple, Optional


IMPORTER_FILE = "importer.template"
PACKAGE_FILE = "package.template"


class File(NamedTuple):
    path: str
    is_package: bool
    code: str
    timestamp: int


def is_module(module: bool) -> bool:
    return os.path.isfile(module) and module.endswith(".py")


def is_package(package: str) -> bool:
    init_file = os.path.join(package, "__init__.py")
    return os.path.isdir(package) and os.path.isfile(init_file)


def get_importer() -> str:
    importer_path = os.path.join(os.path.dirname(__file__), IMPORTER_FILE)
    with open(importer_path) as importer_object:
        importer = importer_object.read()
    return importer


def get_template() -> string.Template:
    template_path = os.path.join(os.path.dirname(__file__), PACKAGE_FILE)
    with open(template_path) as template_object:
        template = string.Template(template_object.read())
    return template


def collect_file(base_dir: str, package_path: str) -> File:
    path = os.path.splitext(package_path)[0].replace(os.path.sep, ".")

    full_path = os.path.join(base_dir, package_path)
    with open(full_path, "r") as f:
        code = f.read()

    is_package = path.endswith("__init__")
    if is_package:
        path = path[:-9]

    timestamp = int(os.path.getmtime(full_path))
    return File(path, is_package, code, timestamp)


def collect_directory(base_dir: str, package_path: str) -> list[File]:
    files = []
    contents = os.listdir(os.path.join(base_dir, package_path))
    for content in contents:
        next_path = os.path.join(package_path, content)
        path = os.path.join(base_dir, next_path)
        if is_module(path):
            files.append(collect_file(base_dir, next_path))
        elif is_package(path):
            files.extend(collect_directory(base_dir, next_path))
    return files


def bundle(packages: list[str], default_package: str, outfile: StringIO, set_hook: Optional[bool] = None):
    package_template = get_template()

    files = []

    for package_path in packages:
        base_dir, module_name = os.path.split(package_path)
        files.extend(collect_directory(base_dir, module_name))

    packages = {path: data for path, *data in files}

    outfile.write(package_template.substitute(
        PACKAGES=json.dumps(packages).replace(
            "true", "True").replace("false", "False"),
        FORCE_EXC_HOOK=str(set_hook),
        DEFAULT_PACKAGE=json.dumps(default_package),
        IMPORTER=json.dumps(get_importer())
    ))
    outfile.close()
