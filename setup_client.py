from setuptools import setup, find_packages

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setup(
    name="GearMess_client",
    version='0.3.1',
    description='Simple messenger.',
    url='https://github.com/StanislavAntunovich/GearMess',
    license='MIT',
    keywords=['python', 'messenger'],
    author='StanislavAntunovich',
    author_email='stanislav.antunovich@yandex.ru',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'console_client = client_src.console_client:start_console',
        ],
        'gui_scripts': [
            'gui_client = client_src.client_gui:start_client',
        ]
    },
    install_requires=[
        'PyQt5',
        'SQLAlchemy',
        'pycryptodomex',
    ],
)
