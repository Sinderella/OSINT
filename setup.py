from setuptools import setup, find_packages

setup(
    name='osint',
    version='0.1',

    description='OSINT Tool',

    author='Thanat Sirithawornsant',

    classifiers=['Development Status :: 1 - Planning',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2.7',
                 ],

    platforms=['Any'],

    scripts=[],

    provides=['osint.plugins.sources',
              ],

    packages=find_packages(),
    include_package_data=True,

    entry_points={
        'osint.plugins.source': [
            'google = osint.plugins.google:Google',
            'bing = osint.plugins.bing:Bing'
        ],
    },

    zip_safe=False,
)
