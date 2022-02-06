from setuptools import setup

setup(
    name='style_transfer',
    packages=['web', 'MLModel'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)
