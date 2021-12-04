import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup_info = {
    "name": "roblox-studio",
    "version": "0.0.1",
    "author": "jmkdev",
    "author_email": "jmk@jmksite.dev",
    "description": "ro.py-studio is a library for interacting with Roblox clients.",
    "long_description": long_description,
    "long_description_content_type": "text/markdown",
    "url": "https://github.com/ro-py/ro.py-studio",
    "packages": setuptools.find_packages(),
    "classifiers": [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: AsyncIO",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries",
        "Topic :: Software Development :: Libraries"
    ],
    "project_urls": {
        "Discord": "https://discord.gg/tjRfCbDMSk",
        "Issue Tracker": "https://github.com/ro-py/ro.py-studio/issues",
        "GitHub": "https://github.com/ro-py/ro.py-studio/",
        "Examples": "https://github.com/ro-py/ro.py-studio/tree/main/examples",
        "Twitter": "https://twitter.com/jmkdev"
    },
    "python_requires": '>=3.7',
    "install_requires": [
        "roblox>=2.0.0",
        "orjson>=3.0.0",
        "aiofiles>=0.8.0",
        "beautifulsoup4>=4.9.0"
    ]
}


setuptools.setup(**setup_info)
