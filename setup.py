from setuptools import setup

LONG_DESCRIPTION = open('README.md', 'r', encoding='utf-8').read()

setup(
    name='f-icon',
    version='0.0.2',
    author='Burve',
    author_email='aleksandrs.ivancenko@gmail.com',
    url='https://github.com/Burve/f-icon',
    description='Set image as an icon of the target folder',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    py_modules=['f_icon', 'mac_icon', 'windows_icon'],
    package_dir={'': 'f_icon'},
    install_requires=[
        "Pillow >= 8.4.0",
        "numpy >= 1.20.1",
        "opencv_python >= 4.5.4.56"
    ],
    extras_require={
      'platform_system=="Darwin"': [
          'pyobjc-framework-cocoa >= 8.0'
      ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.8',
)