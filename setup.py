from distutils.core import setup

setup(
    name='qpushbullet',
    version='0.0.1',
    packages=['qpushbullet', 'qpushbullet.ui'],
    url='https://github.com/n3wtron/qpushbullet',
    license='GPL v3',
    author='Igor Maculan',
    author_email='n3wtron@gmail.com',
    description='pyQt GUI interface for pushbullet',
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Environment :: X11 Applications :: Qt",
        "Topic :: Utilities"
    ],
    install_requires=[
        'pushbullet.py=0.5.0'
    ],
     scripts=[
        'scripts/qpushbullet'
    ]
)
