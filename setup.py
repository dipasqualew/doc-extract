import os
from setuptools import find_packages, setup
from doc_extract.info import (
    VERSION,
    PROJECT_TAG,
    PROJECT_URL,
    AUTHORS,
    SHORT_DESCRIPTION,
    LICENSE_TYPE,
)

with open(os.path.join(os.path.dirname(__file__), "README.md")) as fp:
    README = fp.read()

setup(
    name=PROJECT_TAG,
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    license=LICENSE_TYPE,
    description=SHORT_DESCRIPTION,
    long_description=README,
    url=PROJECT_URL,
    author=", ".join(author["name"] for author in AUTHORS),
    author_email=", ".join(author["email"] for author in AUTHORS),
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
