from distutils.core import setup, Extension

ybc_scrypt_module = Extension('ybc_scrypt',
                               sources = ['scryptmodule.c',
                                          './scrypt-jane/scrypt-jane.c'],
                               include_dirs=['.', './scrypt-jane', './scrypt-jane/code'])

setup (name = 'ybc_scrypt',
       version = '1.0',
       description = 'Bindings for scrypt proof of work used by ybcoin',
       ext_modules = [ybc_scrypt_module])
