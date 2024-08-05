from setuptools import setup, find_packages

setup(
    name='tomfig',
    version='0.1',
    packages=find_packages(),
    install_requires=[],  # Add your dependencies here
    author='Luke Shuttleworth',
    author_email='sluke950@gmail.com',
    description='A short description of your application',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/example_app',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)