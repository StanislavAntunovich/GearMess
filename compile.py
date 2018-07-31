from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [
    Extension("GearMess.client", ["GearMess\\client_src\\client.py"]),
    Extension("GearMess.client_models", ["GearMess\\client_src\\client_models.py"]),
    Extension("GearMess.client_storage_handler", ["GearMess\\client_src\\client_storage_handler.py"]),
    Extension("GearMess.client_views", ["GearMess\\client_src\\client_views.py"]),
    Extension("GearMess.JIM.JIMs", ["GearMess\\JIM\\JIMs.py"]),
    Extension("GearMess.JIM.jim_config", ["GearMess\\JIM\\jim_config.py"]),
    Extension("GearMess.crypto", ["GearMess\\crypto\\crypto.py"]),
]

setup(
    name='gui client',
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
)
