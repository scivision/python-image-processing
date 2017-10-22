#!/usr/bin/env python
req=['pathlib2','spectral','nose','numpy','matplotlib','scipy','scikit-image']
# %%
try:
    import conda.cli
    conda.cli.main('install',*req)
except Exception as e:
    import pip
    pip.main(['install'] + req)
# %%

from setuptools import setup


setup(name='pyimagefilter',
      packages=['pyimagefilter'],
      author='Michael Hirsch, Ph.D.',
      url='https://github.com/scivision/python-image-processing',
	  description='examples of image processing in Python',
	  )
