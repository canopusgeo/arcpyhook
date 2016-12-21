from setuptools import setup, find_packages

config = {
    'name' : 'arcpyhook',
    'version' : "0.1.0",
    'description' : 'Determines the location of the ArcGIS install and append the appropiate paths to python sys.path environment.',
    'author' : 'Canopus Geoinformatics Ltd',
    'author_email' : 'info@canopusgeo.com',
    'url' : 'https://github.com/canopusgeo/arcpyhook',
    'packages' : find_packages(),
	'test_suite' : 'nose.collector',
    'install_requires' : ['nose'],
    'include_package_data' : True,
    'classifiers' : [
        'Environment :: Console',
        'Intended Audience :: Science/Research/GIS',
		'License :: GPLv2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering/GIS',
        'Operating System :: Microsoft :: Windows'
    ]
    }
setup(**config)



