from setuptools import setup

setup(name='seam_carving',
      version='0.1',
      description='The funniest joke in the world',
      url='http://github.com/storborg/funniest',
      author='Flying Circus',
      author_email='flyingcircus@example.com',
      license='MIT',
      packages=['seam_carving'],
      install_requires=[
          'matplotlib',
          'imageio',
          'numpy',
          'tkinter'
      ],
      zip_safe=False)