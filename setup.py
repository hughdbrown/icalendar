try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='icalendar',
    version='0.1',
    description='ical helper classes',
    author='Hugh Brown',
    author_email='hughdbrown@yahoo.com',
    url='iwebthereforeiam.com',
    install_requires=[
        'nose',
    ],
    tests_require=[
        'simplejson',
    ],
    setup_requires=[],
    packages=find_packages(exclude=['test']),
    include_package_data=True,
    test_suite='nose.collector',
    zip_safe=False,
)
