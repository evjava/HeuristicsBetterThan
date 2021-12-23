from setuptools import setup, find_packages

requirements = (
  'setuptools>=59.2.0',
  'matplotlib>=3.3.4',
  'numpy>=1.21.4',
  'imageio>=2.13.3',
  'ipython>=7.29.0',
  'pillow>=8.4.0',
  'loguru>=0.5.3',
  'sortedcontainers>=2.4.0',
  'scipy>=1.6.1'
)

extra_requirements = {
}

setup(name='mra_and_rstar_comparation',
      version='0.1',
      license='',
      packages=find_packages(),
      python_requires='>=3.6',
      install_requires=requirements,
      extras_require=extra_requirements)