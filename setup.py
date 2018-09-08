from setuptools import setup

setup(
    name='ghostlord',
    packages=['ghostbin'],
    version='1.3.1',
    author='Gurkirat',
    author_email='tbhaxor@gmail.com',
    url='https://tbhaxor.me/ghostlord',
    download_url='https://github.com/tbhaxor/ghostlord/archive/master.zip',
    description='A slim line ghost bin api',
    long_description=open('LONG_DESC.rst').read(),
    license='MIT',
    install_requires=['cfscrape', 'randua'],
    keywords='ghostbin, ghostlord, tbhaxor, api',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    python_requires='>=3')
