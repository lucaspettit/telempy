import os.path

from setuptools import setup, find_packages
from pathlib import Path


# get long description from README
with open('README.md') as f:
  long_description = f.read()

package_requirements=['salsa20', 'marshmallow-dataclass', 'marshmallow-enum']
test_requirements=['sure', 'unittest', 'pytest-cov', 'pylint-fail-under']

setup(
  name='granturismo',
  version="0.0.8",
  author='Lucas Pettit',
  author_email='lucaspettit64@gmail.com',
  description='Get Grand Turismo telemetry data from the PlayStation console',
  project_urls={
    'Bug Tracker': 'https://github.com/lucaspettit/telempy/issues',
    'Source Code': 'https://github.com/lucaspettit/telempy'
  },
  long_description=long_description,
  long_description_content_type='text/markdown',
  license='MIT',
  packages=find_packages(where='src'),
  package_dir={'': 'src'},
  data_files=[],
  scripts=list(map(str, Path('examples').glob('*.py'))),
  test_require=test_requirements,
  test_command='test',
  test_suite='tests',
  python_requires='>=3.7',
  platforms=["Windows", "Linux", "Solaris", "Mac OS-X", "Unix"],
  clasifiiers=[
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Operating System :: POSIX',
    'Operating System :: Unix',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: MacOS',
    'Topic :: Software Development',
    'Topic :: Games/Entertainment'
    'Topic :: Games/Entertainment :: Simulation',
    'Intended Audience :: Developers',
    'Intended Audience :: Other Audience'
  ],
  install_requires=package_requirements,
  zip_safe=False
)