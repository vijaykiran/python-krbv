# -*- coding: utf-8 -*-

import os
import subprocess

from glob import glob
from setuptools import setup as _setup, Extension, find_packages

def read_content(filename):
    ''' Return whole content of the specified file simply '''

    return open(filename, 'r').read()

def build_long_description():
    '''Make long description as a reStructuredText document

    It will put AUTHORS, NEWS, README, and ChangeLog into
    a whole reStructuredText document.
    '''

    return \
        'Authors\n' \
        '=======\n\n' \
        '%(authors)s\n\n' \
        'News\n' \
        '====\n\n' \
        '%(news)s\n\n' \
        'Change Log\n' \
        '==========\n\n' \
        '%(changelog)s\n\n' \
        'ReadMe\n' \
        '=======\n\n' \
        '%(readme)s\n' % {
            'authors': read_content('AUTHORS'),
            'news': read_content('NEWS'),
            'changelog': read_content('ChangeLog'),
            'readme': read_content('README'),
        }

def locate_krb5_h():
    ''' Search krb5.h and return its absolute path '''

    join = os.path.join
    exists = os.path.exists

    for krb5_prefix in ('/usr', '/usr/kerberos', '/usr/athena'):
        for krb5_includedir in ('include/krb5', 'include'):
            filename = join(krb5_prefix, krb5_includedir, 'krb5.h')
            if exists(filename):
                return filename
    return None

def generate_krb5defines_h_from(krb5_h_filename):
    '''Generate krb5defines.h from krb5.h

    The method to generate krb5defines.h is the same as how Makefile does
    '''

    cmd = 'awk -f gendefines.awk %s > krb5defines.h' % krb5_h_filename
    proc = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
    stdout_data, stderr_data = proc.communicate()
    if proc.returncode > 0:
        raise OSError(stderr_data)

def setup(*args, **kwargs):
    ''' Wrapping setuptools' setup to add custom controls '''

    krb5_h_filename = locate_krb5_h()
    if krb5_h_filename is None:
        raise IOError('Cannot find krb5.h, enusre you have installed '
                      'krb5 development library.')
    generate_krb5defines_h_from(krb5_h_filename)

    _setup(**kwargs)

setup(
    name = 'python-krbV',
    version = '1.0.90',
    description = 'Python extension module for Kerberos 5',
    long_description = build_long_description(),
    keywords = ['kerberos',],
    license = 'GPL',
    author = 'Mike Bonnet',
    author_email = 'mikeb@redhat.com',
    url = 'https://fedorahosted.org/python-krbV/',

    packages = find_packages(exclude=['tests',]),
    data_files = [
        ('example', ['krbV-code-snippets.py',]),
        ('test', ['python-krbV-test.py',]),
    ],

    ext_modules = [
        Extension('krbV',
            glob('*.c'),
            include_dirs = ['.', 'krb5', 'com_err'],
            libraries = ['krb5', 'com_err'])
    ],

    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Environment :: X11 Applications',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX',
        'Programming Language :: C',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Systems Administration',
    ],
)

