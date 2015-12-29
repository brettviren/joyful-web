from setuptools import setup, find_packages
setup(
    name = 'joyful-web',
    version = '0.0',
    url = 'http://github.com/brettviren/joyful-web',
    packages = find_packages(),
    install_requires = [
        'Click',
    ],
    entry_points='''
    [console_scripts]
    joy=joy.cli:main
    ''',
    include_package_data = True,
)
