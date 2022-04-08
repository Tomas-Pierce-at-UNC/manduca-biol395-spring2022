
from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize(
        ["align.pyx",
         "common.pyx",
         "tube.pyx",
         "cine.pyx",
         "tester.pyx"
         ]
        )
    )
