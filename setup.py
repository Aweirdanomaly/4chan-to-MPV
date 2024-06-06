from setuptools import setup, find_packages
import distutils.sysconfig
import os 

with open("README.md", "r") as f:
    description = f.read()

setup(
    name='doom-chan',
    description='Turns 4chan threads into \"doomscrollable\" playlists',
    version='v1.0.0',
    packages=find_packages(),
    license_files=('LICENSE'),
    python_requires='>=3.10',
    install_requires=[
        'requests',
        'beautifulsoup4',
        'python-mpv',
        'colorama',
        'cowsay'
    ],
    entry_points={
        "console_scripts":[
            "dc = doomchan:main",
        ],
    },
    data_files=[("Lib\\site-packages\\doomchan", ["D:\\Users\\car\\Desktop\\projects\\wsg\\release\\doomchan\\libmpv-2.dll"])],
    keywords=["4chan", "video", "CLI", "mpv", "doom scroll", ],
    long_description=description,
    long_description_content_type="text/markdown",
    
)