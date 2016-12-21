import os
import sys
from distutils.core import setup


if 'develop' in sys.argv or any(a.startswith('bdist') for a in sys.argv):
    import setuptools


from flexxlab.labext import write_flexx_core_js
write_flexx_core_js()


setup_args = dict(
    name                 = 'flexxlab',
    version              = '1.0.0',
    description          = 'Enable writing Jupyterlab plugins using Flexx.',
    url                  = 'http://github.com/zoofio/flexxlab',
    author               = 'Almar Klein',
    author_email         = 'almar.klein@gmail.com',
    keywords             = ['jupyterlab', 'jupyterlab extension', 'flexx'],
    
    packages             = ['flexxlab'],
    include_package_data = True,
    zip_safe             = False,
    install_requires     = ['jupyterlab>=0.3.0', 'flexx>=0.4'],
    entry_points         = {'console_scripts': ['flexxlab = flexxlab.__main__:main'], },
    
    platforms            = 'any',
    classifiers          = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)

if __name__ == '__main__':
    setup(**setup_args)
