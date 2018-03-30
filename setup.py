# coding: utf8

from setuptools import setup

setup(name='yandex_pdd',
      version='0.1',
      description='Internetbs Python API',
      url='http://github.com/alephyud/pyinternetbs',
      author='vmax@github',
      license='MIT',
      packages=['pyinternetbs'],
      install_requires=[
          'requests',
      ],
      zip_safe=False)
