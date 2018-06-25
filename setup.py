from setuptools import setup, find_packages

setup(name='coloredlids',
      version='0.1',
      description='Models of heat transfer, fluid flow and structural mechanics',
      url='https://github.com/dwweiss/coloredlids',
      keywords='theoretical, modelling, modeling, white box, gray box, grey box',
      author='Dietmar Wilhelm Weiss',
      license='GLGP 3.0',
      platforms=['Linux', 'Windows'],
      packages=find_packages(), 
      include_package_data=True,
      install_requires=['numpy', 'matplotlib', 'pandas', 'scipy', 'grayboxes'],
      classifiers=['Programming Language :: Python :: 3',
                   'Topic :: Scientific/Engineering',
                   'License :: OSI Approved :: GLGP 3.0 License']
      )
