from setuptools import setup, find_packages
from pathlib import Path

# parse package and test requirements from requirements.txt
with open('requirements.txt') as f:
  # use f.read().splitlines() instead of f.readlines() so that the newline char gets removed automatically
 lines = f.read().splitlines()

index = 0
# populate package requirements, these are listed first
package_requirements = []
while index < len(lines):
  line = lines[index]
  index += 1
  if not line:
    continue
  if line.lower().startswith('# test'):
    break
  package_requirements.append(line)

# populate the test requirements, these are listed after # testing
test_requirements = []
while index < len(lines):
  line = lines[index]
  index += 1
  if not line:
    continue
  test_requirements.append(line)


# get long description from README
with open('README.md') as f:
  long_description = f.read()


setup(
  name='telempy',
  version=0.1,
  author='Lucas Pettit',
  author_email='lucaspettit64@gmail.com',
  description='Get Grand Turismo telemetry data from the PlayStation console',
  long_description=long_description,
  license='MIT',
  packages=find_packages(where='src'),
  package_dir={'': 'src'},
  data_files=[],
  scripts=list(map(str, Path('examples').glob('*.py'))),
  test_require=test_requirements,
  test_command='test',
  test_suite='tests',
  python_requires='>=3.7',
  clasifiiers=[
    'Programming Language :: Python :: 3',
    'Operating System :: Windows :: Linux :: POSIX :: MacOS'
  ],
  install_requires=package_requirements,
  zip_safe=False
)