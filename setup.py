#!/usr/bin/env python
install_requires=['numpy','matplotlib','scipy','scikit-image','imageio',
     'spectral']
# %%
from setuptools import setup, find_packages

setup(name='pyimagefilter',
      packages=find_packages(),
      author='Michael Hirsch, Ph.D.',
      url='https://github.com/scivision/python-image-processing',
	  description='examples of image processing in Python',
	  long_description=open('README.rst').read(),
      install_requires=install_requires,
      python_requires='>=3.5',
	  )
