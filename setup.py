from setuptools import setup

setup(name='coloredlids',
      version='0.1',
      description='Models of heat transfer, fluid flow and structural mechanics',
      url='https://github.com/dwweiss/coloredlids',
      keywords='modelling, modeling, gray box, grey box, hybrid model',
      author='Dietmar Wilhelm Weiss',
      license='GLGP 3.0',
      platforms=['Linux', 'Windows'],
      packages=['coloredlids'],
      package_dir={'coloredlids': 'src'},
      include_package_data=True,
      install_requires=['numpy', 'matplotlib', 'pandas', 'scipy', 'grayboxes'],
      classifiers=['Programming Language :: Python :: 3',
                   'Topic :: Scientific/Engineering',
                   'License :: OSI Approved :: GLGP 3.0 License']
      )
