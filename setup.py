import codecs
import os

from setuptools import setup, find_packages

from etl_ml import __version__ as version
# See this web page for explanations:
# https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/
PACKAGES = ["etl_ml",]
KEYWORDS = ["etl", "dirtyData",'ssh tunnel' ,"ml", "machine learning"]
CLASSIFIERS = [
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Natural Language :: English",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Topic :: Scientific/Engineering",
]
# Project root
ROOT = os.path.abspath(os.path.dirname(__file__))

setup(
    name="etl_ml",
    description="etl_ml is a tools could etl origin excel or csv dirty data and  send data to ftp or  server  and insert data to hive database and load data from jump hive make feature project  machine learning model train and jump the jump machine  to connect hive get hive data to pandas dataframe",
    license="Apache 2.0",
    url='https://github.com/mullerhai/etl_ml',
    version=version,
    author="mullerhai",
    author_email="hai710459649@foxmail.com",
    maintainer="muller helen",
    maintainer_email="hai710459649@foxmail.com",
    long_description=open('README.rst').read(),
    keywords=KEYWORDS,
    packages=find_packages(),
    classifiers=CLASSIFIERS,
    zip_safe=False,
    platforms=["all"],
    include_package_data=True,
    install_requires=[
        'scipy>=1.1.0',
        'numpy>=1.14.3'
        'pandas>=0.20.3',
        'PyHive>=0.5.1',
        'paramiko>=2.4.1',
        'selectors>=0.0.14',
        'sasl>=0.2.1',
        'thrift>=0.11.0',
        'thrift-sasl>=0.3.0',
        'hdfs>=2.1.0',
        'sklearn-pandas>=1.6.0',
        'scikit-learn>=0.19.1',
        'click>=6.7',
        'ast>=0.0.2',

    ],
    entry_points={
        'console_scripts': [
            'etl_label = jumps.jump_terminal:main',
            'etl = jumps.jump_gui:main'

        ]
    },
)


