from setuptools import setup, find_packages

setup(
    name='42M',
    description="Turns 4chan threads into playlists",
    version='v1.0.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'python-mpv',
        'colorama',
        'cowsay'
    ],
    
)