from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
	long_description = f.read()

setup(
	name='colouration',
	version='2020.4.6',
	license='MIT',
	author='Idin',
	author_email='py@idin.ca',
	url='https://github.com/idin/colouration',
	keywords='colour',
	description='Python library for working with colours',
	long_description=long_description,
	long_description_content_type='text/markdown',
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3 :: Only',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Topic :: Software Development :: Libraries :: Python Modules'
	],

	packages=find_packages(exclude=("jupyter_tests", ".idea", ".git", "data_files")),
	install_requires=[],
	package_data={'colouration': ['data_files/*.pickle']},
	python_requires='~=3.6',
	zip_safe=True,
	test_suite='nose.collector',
	tests_require=['nose', 'coverage']
)
