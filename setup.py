from setuptools import setup

setup(name='baseball',
      version='16.0',
      description='Library to download, anaylyze, and visualize events in Major League Baseball games.',
      url='https://github.com/benjamincrom/baseball',
      author='Benjamin B. Crom',
      author_email='benjamincrom@gmail.com',
      include_package_data=True,
      license='MIT',
      packages=['baseball'],
      zip_safe=False,
      install_requires=['python-dateutil', 'pytz', 'requests'])
