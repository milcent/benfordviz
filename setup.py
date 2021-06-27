''' Setup for benford's module'''
from os import path
from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='benfordviz',
      version='0.2.0',
      description='A library providing interactive plotting to benford-py',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/milcent/benfordviz',
      download_url='https://github.com/milcent/benfordviz/archive/v0.2.0.tar.gz',
      author='Marcel Milcent',
      author_email='marcelmilcent@gmail.com',
      license='BSD 3-Clause',
      packages=['benfordviz'],
      install_requires=[
          'benford-py',
          'bokeh>=2.2.2'
      ],
      zip_safe=False,
      classifiers=[
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: BSD License',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Financial and Insurance Industry',
          'Intended Audience :: Science/Research',
          'Intended Audience :: Education',
          'Intended Audience :: Other Audience',
          'Topic :: Office/Business :: Financial :: Accounting',
          'Topic :: Scientific/Engineering :: Mathematics',
      ],)
