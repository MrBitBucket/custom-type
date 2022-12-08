from setuptools import setup, Extension
from wheel.bdist_wheel import bdist_wheel, get_abi_tag
from os.path import join as pjoin
import sys, os, sysconfig, re

def specialOption(n,ceq=False):
    v = 0
    while n in sys.argv:
        v += 1
        sys.argv.remove(n)
    if ceq:
        n += '='
        V = [_ for _ in sys.argv if _.startswith(n)]
        for _ in V: sys.argv.remove(_)
        if V:
            n = len(n)
            v = V[-1][n:]
    return v

def getVersionFromCCode(fn):
    tag = re.search(r'^#define\s+VERSION\s+"([^"]*)"',open(fn,'r').read(),re.M)
    return tag and tag.group(1) or ''

def get_la_info():
    limited_api_kwds = {}
    if specialOption('--abi3') or os.environ.get('ABI3_WHEEL','0')=='1':
        cpstr = get_abi_tag()
        if cpstr.startswith("cp"):
            lav = '0x03070000'
            cpstr = 'cp37'
            if sys.platform == "darwin":
                machine = sysconfig.get_platform().split('-')[-1]
                if machine=='arm64' or os.environ.get('ARCHFLAGS','')=='-arch arm64':
                    #according to cibuildwheel/github M1 supports pythons >= 3.8
                    cpstr = 'cp38'
                    lav = '0x03080000'

            class bdist_wheel_abi3(bdist_wheel):
                __cpstr = cpstr
                def get_tag(self):
                    python, abi, plat = super().get_tag()
                    if python.startswith("cp"):
                        abi = 'abi3'
                        python = self.__cpstr
                    return python,abi,plat

            limited_api_kwds = dict(
                        cmdclass=dict(
                            bdist_wheel=bdist_wheel_abi3,
                            ),
                        macros=[("Py_LIMITED_API", lav)],
                        )

    return limited_api_kwds

def main():
    limited_api_kwds = get_la_info()
    limited_api_macros = limited_api_kwds.pop('macros',[])
    setup(
        ext_modules=[
            Extension(
                "_custom",
                sources=[pjoin('src','_custom.c')],
                define_macros = limited_api_macros,
                py_limited_api = limited_api_macros!=[],
                )
            ],
        name="custom",
        version=getVersionFromCCode(pjoin('src','_custom.c')),
        license="BSD 2 Clause license",
        description="custom type test module",
        long_description="""custom type test module""",
        author="the community",
        url="http://www.reportlab.com/",
        packages=[],
        package_data = {},
        classifiers = [
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Topic :: Printing',
            'Topic :: Text Processing :: Markup',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
            ],
        license_files = ['LICENSE'],

        #this probably only works for setuptools, but distutils seems to ignore it
        install_requires=[],
        python_requires='>=3.7,<4',
        extras_require={
            },
        **limited_api_kwds
        )

if __name__=='__main__':
    main()
