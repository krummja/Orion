from setuptools import setup


setup(
    name="orion",
    version="0.1.0",
    description="A game design framework implementing modular plugins and an event system.",
    long_description="",
    keywords=["pygame", "framework", "design"],
    url="https://github.com/krummja/orion_plugin",
    author="Jonathan Crum",
    author_email="crumja4@gmail.com",
    license="MIT",
    packages=[
        "orion",
        "orion.core",
        "orion.plugins",
    ],
    zip_safe=False,
    python_requires=">=3.8.5",
    setup_requires=[],
    install_requires=["pygame>=2.0.0"],
    include_package_data=True,
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ]
)
