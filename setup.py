from setuptools import setup

setup(
    name='srpm_buildorder',
    packages=['srpm_buildorder'],
    install_requires=[
        ],
    test_suite='nose.collector',
    tests_require=[
        'nose',
        ],
    version='0.1',
    entry_points={
        'console_scripts': [
            'srpm_buildorder = srpm_buildorder.cli:entrypoint'
            ]
        },
)
