from os.path import exists
from setuptools import setup

setup(name='intrograph',
      version='0.1',
      description='Represent computation DAGs with introspection',
      url='http://github.com/mrocklin/intrograph',
      author='Matthew Rocklin',
      author_email='mrocklin@gmail.com',
      license='BSD',
      packages=['intrograph'],
      long_description=open('README.md').read() if exists("README.md") else "",
      zip_safe=False)
