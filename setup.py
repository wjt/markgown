#!/usr/bin/env python

from distutils.core import setup

setup(name='Markgown',
      version='1.0',
      description='A live Markdown previewer for GNOME',
      author='Will Thompson',
      author_email='will@willthompson.co.uk',
      url='https://github.com/wjt/markgown',
      packages=['markgown'],
      package_data={
          'markgown': ['markdown.css'],
      },
      scripts=['bin/markgown-viewer'],
     )
