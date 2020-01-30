import os as _os
from importlib import machinery
import importlib.util
import sys


def _get_extention_dir():
    return _os.path.join(_os.path.dirname(_os.path.realpath(__file__)), "_ext")


def _import_module(module_name, extension_name):
    mod_path = _os.path.join(_get_extention_dir(), extension_name)
    loader = machinery.ExtensionFileLoader(extension_name, mod_path)
    spec = importlib.util.spec_from_loader(extension_name, loader)
    mod = loader.create_module(spec)
    loader.exec_module(mod)
    for name, attr in mod.__dict__.items():
        if name[0] == "_":
            continue
        setattr(sys.modules[module_name], name, attr)
    return mod
