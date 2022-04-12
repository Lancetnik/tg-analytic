import os
from importlib.machinery import SourceFileLoader

from pkg_resources import parse_requirements
from setuptools import find_packages, setup


module_name = 'app'


module = SourceFileLoader(
    module_name, os.path.join(module_name, '__init__.py')
).load_module()

def load_requirements(fname: str) -> list:
    requirements = []
    with open(fname, 'r') as fp:
        for req in parse_requirements(fp.read()):
            extras = '[{}]'.format(','.join(req.extras)) if req.extras else ''
            requirements.append(
                '{}{}{}'.format(req.name, extras, req.specifier)
            )
    return requirements

setup(
    name=module_name,
    version=module.__version__,
    author="Lancetnik",
    description=module.__doc__,
    platforms='all',
    classifiers=[
        'Natural Language :: Russian',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython'
    ],
    python_requires='>=3.8',
    packages=find_packages(exclude=['tests']),
    install_requires=load_requirements('requirements.txt'),
    extras_require={'dev': load_requirements('dev_requirements.txt')},
    entry_points={
        'console_scripts': [
            'tg-analytic = {0}.__main__:main'.format(module_name),
        ]
    },
    include_package_data=True
)