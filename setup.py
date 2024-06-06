from setuptools import setup, find_packages
import distutils.sysconfig
import os 

with open("README.md", "r") as f:
    description = f.read()

setup(
    name='doom_chan',
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
            "dc = doom_chan:main",
        ],
    },
    data_files=[("Lib\\site-packages\\doom_chan", [".\\doom_chan\\libmpv-2.dll"])],
    keywords=["4chan", "video", "CLI", "mpv", "doom scroll", ],
    long_description=description,
    long_description_content_type="text/markdown",
    
)