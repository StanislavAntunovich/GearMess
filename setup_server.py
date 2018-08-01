from setuptools import setup, find_packages

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setup(
    name="GearMess_server",
    version='0.1.1',
    description='Simple server for messenger.',
    url='https://github.com/StanislavAntunovich/GearMess',
    license='MIT',
    keywords=['python', 'messenger'],
    author='StanislavAntunovich',
    author_email='stanislav.antunovich@yandex.ru',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'console_server = server_src.server:start_server']

    },
    install_requires=[
        'SQLAlchemy',
        'pycryptodomex',
    ],
)
