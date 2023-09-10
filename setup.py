#!/usr/bin/env python

"""discretize

Discretization tools for finite volume and inverse problems.

"""

import os
import sys
import numpy
from setuptools import setup
from setuptools import Extension
from Cython.Build import cythonize
from setuptools.command.build_ext import build_ext as _build_ext

ext_kwargs = {}
if os.environ.get("DISC_COV", None) is not None:
    ext_kwargs["define_macros"].append(("CYTHON_TRACE_NOGIL", 1))

osname = os.name
if os.name == "nt":  # windows
    std_arg = "/std:c++17"
else:  # posix i.e. linux and mac
    std_arg = "-std=c++17"

extensions = [
    Extension(
        "discretize._extensions.interputils_cython",
        sources=["src/discretize/_extensions/interputils_cython.pyx"],
        include_dirs=[numpy.get_include()],
        language="c",
        **ext_kwargs
    ),
    Extension(
        "discretize._extensions.simplex_helpers",
        sources=["src/discretize/_extensions/simplex_helpers.pyx"],
        include_dirs=[numpy.get_include()],
        language="c",
        **ext_kwargs
    ),
    Extension(
        "discretize._extensions.tree_ext",
        sources=[
            "src/discretize/_extensions/tree_ext.pyx",
            "src/discretize/_extensions/tree.cpp",
        ],
        include_dirs=[numpy.get_include()],
        language="c++",
        extra_compile_args=[std_arg],
        **ext_kwargs
    ),
]

# cmdclass['bdist_wheel']
try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            self.root_is_pure = False
            _bdist_wheel.finalize_options(self)

except ImportError:
    bdist_wheel = None


# cmdclass['_build_ext']
class build_ext(_build_ext):
    def finalize_options(self):
        _build_ext.finalize_options(self)
        self.include_dirs.append(numpy.get_include())


setup_kwargs = {}
setup_kwargs["name"] = "discretize"
setup_kwargs["use_scm_version"] = {
    "write_to": os.path.join("src", "discretize", "version.py")
}
setup_kwargs["cmdclass"] = {"bdist_wheel": bdist_wheel, "build_ext": build_ext}
setup_kwargs["ext_modules"] = cythonize(
    extensions, compiler_directives={"language_level": 3}
)

setup(**setup_kwargs)
