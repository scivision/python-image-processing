#!/usr/bin/env python
from setuptools import setup
import subprocess

try:
    subprocess.call(['conda','install','--file','requirements.txt'])
except Exception:
    pass

setup(name='pyimagefilter',
	  description='examples of image processing in Python',
	  url='https://github.com/scienceopen/isrutils',
	  install_requires=['pathlib2','spectral'],
      packages=['pyimagefilter'],
	  )
