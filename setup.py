'''
Author: Uper 41718895+Hyliu-BUAA@users.noreply.github.com
Date: 2022-06-01 21:50:16
LastEditors: Uper 41718895+Hyliu-BUAA@users.noreply.github.com
LastEditTime: 2022-06-01 21:50:19
FilePath: /pyIPR/setup.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from setuptools import setup, find_packages


setup(
    name="pyIPR",
    version="v1.0",
    packages=find_packages(),
    include_package_data=True
)