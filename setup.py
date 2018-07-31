from cx_Freeze import setup, Executable


setup(
    name="GearMess_client",
    version='0.0.1',
    description='Simple client messenger.',
    url='https://github.com/StanislavAntunovich/GearMess',
    license='MIT',
    keywords=['python', 'messenger'],
    author='AntonPaly4',
    author_email='stanislav.antunovich@gmail.com',
    options={
        "build_exe": {'excludes': ['tkinter'],
                      'include_msvcr': True}
    },
    executables=[Executable("gui_client.py", base='Win32GUI')]
)
