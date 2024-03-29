from setuptools import setup, find_packages

setup(
    name='cpuex_asm',
    version="0.0.4",
    author='Takashi Yoneuchi',
    author_email='takahsi.yoneuchi@shift-js.info',
    packages = ['cpuex_asm'],
    entry_points={
        "console_scripts": [
            "cpuex_asm=cpuex_asm.asm:main",
            "cpuex_bin2coe=cpuex_asm.bin2coe:main"
        ]
    },
)
