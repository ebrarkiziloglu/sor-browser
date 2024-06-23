from setuptools import setup, find_packages

setup(
    name='Sor Browser',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'PyQt5==5.15.10',
        'PyQt5-Qt5==5.15.14',
        'PyQt5-sip==12.13.0',
        'PyQtWebEngine==5.15.6',
        'PyQtWebEngine-Qt5==5.15.14'
    ],
    entry_points={
        'console_scripts': [
            'my_browser = my_browser.main_window:main'
        ]
    },
)
