#! /usr/bin/env python

# System imports
from setuptools import Extension, setup
from setuptools.command.build_py import build_py

# Third-party modules - we depend on numpy for everything
import numpy
import os
# Obtain the numpy include directory.  This logic works across numpy versions.
try:
    numpy_include = numpy.get_include()
except AttributeError:
    numpy_include = numpy.get_numpy_include()
# HexitecIO extension module
_AmptekHardwareInterface = Extension("amptek_hardware_interface._AmptekHardwareInterface",
                   ["python/amptek_hardware_interface/AmptekHardwareInterface.i",] + ["src/" + f for f in os.listdir("src") if os.path.isfile("src/" + f)],
                   include_dirs = [numpy_include, "include", "src"],
                   swig_opts=['-c++',"-doxygen"],
                   extra_compile_args = ["-std=c++11", "-g"], 
                   libraries=["usb-1.0"]
                   )

class BuildPy(build_py):
    def run(self):
        self.run_command("build_ext")
        super().run()


# NumyTypemapTests setup
setup(  name        = "AmptekHardwareInterface",
        description = "Implementation of the Amptek DP5 Protocol",
        package_dir = {"amptek_hardware_interface": "python/amptek_hardware_interface"},
        packages    = ["amptek_hardware_interface"],
        scripts     = ["python/amptek_hardware_interface/AmptekPX5"],    
        author      = "Christian Koernig",
        version     = "0.1",
        ext_modules = [_AmptekHardwareInterface],
        cmdclass = {"build_py": BuildPy}
        )
