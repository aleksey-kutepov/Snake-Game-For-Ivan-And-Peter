from setuptools import find_packages
from setuptools import setup

major_version = '0.1'
minor_version = '0'
name = 'snake_game'

version = "%s.%s" % (major_version, minor_version)

if __name__ == "__main__":
    setup(name=name,
          version=version,
          description='Snake Game For Ivan And Peter',
          classifiers=[
              "Development Status :: 1 - Beta",
              "Programming Language :: Python",
          ],
          author='Aleksey Kutepov',
          author_email='kutepoff@gmail.com',
          packages=find_packages(),
          zip_safe=False,
          install_requires=[
              'pygame==1.9.2'
          ],
          entry_points={
              'console_scripts': [
                  'snake_game = snake.snake_main:main',
              ],
          },
          )
