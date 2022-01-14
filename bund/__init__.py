__version__ = "0.0.0"


import os
import string
import json

from bund.typings import CFG, File


IMPORTER_FILE = "importer.template"
PACKAGE_FILE = "package.template"


def is_module(module: bool) -> bool:
    return os.path.isfile(module) and module.endswith(".py")


def is_package(package: str) -> bool:
    init_file = os.path.join(package, "__init__.py")
    return os.path.isdir(package) and os.path.isfile(init_file)


def output(cfg: CFG, what: str):
    cfg.outfile.write(what)


def importer() -> str:
    importer_path = os.path.join(os.path.dirname(__file__), IMPORTER_FILE)
    with open(importer_path) as importer_object:
        importer = importer_object.read()
    return importer


def template() -> string.Template:
    template_path = os.path.join(os.path.dirname(__file__), PACKAGE_FILE)
    with open(template_path) as template_object:
        template = string.Template(template_object.read())
    return template


def process_file(base_dir: str, package_path: str) -> File:
    path = os.path.splitext(package_path)[0].replace(os.path.sep, ".")

    full_path = os.path.join(base_dir, package_path)
    print(full_path)
    with open(full_path, "r") as f:
        code = f.read()

    is_package = path.endswith("__init__")
    if is_package:
        path = path[:-9]

    timestamp = int(os.path.getmtime(full_path))
    return File(path, is_package, code, timestamp)


def process_directory(base_dir: str, package_path: str) -> list[File]:
    files = []
    contents = os.listdir(os.path.join(base_dir, package_path))
    for content in contents:
        next_path = os.path.join(package_path, content)
        path = os.path.join(base_dir, next_path)
        if is_module(path):
            files.append(process_file(base_dir, next_path))
        elif is_package(path):
            files.extend(process_directory(base_dir, next_path))
    return files


def process_files(cfg: CFG):
    package_template = template()

    files = []

    for package_path in cfg.packages:
        base_dir, module_name = os.path.split(package_path)
        files.extend(process_directory(base_dir, module_name))

    packages = {path: data for path, *data in files}

    output(cfg, package_template.substitute(
        PACKAGES=json.dumps(packages).replace(
            "true", "True").replace("false", "False"),
        FORCE_EXC_HOOK=str(cfg.set_hook),
        DEFAULT_PACKAGE=json.dumps(cfg.default_package),
        IMPORTER=json.dumps(importer())
    ))
    cfg.outfile.close()
