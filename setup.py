from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="GearMess",
    version='0.0.1.3',
    description='Simple messenger.',
    long_description=long_description,
    url='https://github.com/StanislavAntunovich/GearMess',
    license='MIT',
    keywords=['python', 'messenger'],
    author='AntonPaly4',
    author_email='stanislav.antunovich@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'PyQt5',
        'SQLAlchemy',
    ],
)
