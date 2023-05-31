from setuptools import setup

setup(name='jaiminho',
      version='0.0.2',
      description='A CLI rest client',
      url='https://github.com/rmonico/jaiminho',
      author='Rafael Monico',
      author_email='rmonico1@gmail.com',
      license='GPL3',
      packages=['jaiminho', 'jaiminho.commands'],
      entry_points={
          'console_scripts': ['jai=jaiminho.__main__:main'],
      },
      zip_safe=False)

