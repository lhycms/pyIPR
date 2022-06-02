<!--
 * @Author: Uper 41718895+Hyliu-BUAA@users.noreply.github.com
 * @Date: 2022-06-01 21:52:17
 * @LastEditors: Uper 41718895+Hyliu-BUAA@users.noreply.github.com
 * @LastEditTime: 2022-06-02 13:53:25
 * @FilePath: /pyIPR/README.md
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->

# 1. 安装方法
```shell
$ cd pyIPR
$ ls .
README.md data      pyIPR     setup.py
$ pip3 install -e .
```


# 2. 使用方法
## 2.1. 计算真空能级的 IPR
```python
>>> from pyIPR.IPRGenerator import IPRCalculator
>>> from pymatgen.electronic_structure.core import Spin
>>> procar_path = '/Users/mac/我的文件/Mycode/new/new/pyIPR/data/PROCAR'
>>> eigenval_path = "/Users/mac/我的文件/Mycode/new/new/pyIPR/data/EIGENVAL"
>>> output_path = "/Users/mac/我的文件/Mycode/new/new/pyIPR/data/IPRs.csv"
>>> IPR_calculator = IPRCalculator(
                        procar_path=procar_path,
                        eigenval_path=eigenval_path,
                        output_csv_path=output_path
                        )
>>> print(IPR_calculator)
+----------------+----------+--------+-------+
|   spins_lst    | nkpoints | nbands | nions |
+----------------+----------+--------+-------+
| [<Spin.up: 1>] |    25    |  480   |  108  |
+----------------+----------+--------+-------+

# 计算真空能级的 IPR
>>> IPR_calculator.concat_energys_IPRs(Spin(1), efermi=None)    # 运行完毕后，产生 "/Users/mac/我的文件/Mycode/new/new/pyIPR/data/IPRs.csv" 文件
```

## 2.2. 计算减去费米能级后的 IPR
```python
>>> from pyIPR.IPRGenerator import IPRCalculator
>>> from pymatgen.electronic_structure.core import Spin
>>> from pymatgen.io.vasp.outputs import Vasprun
>>> procar_path = '/Users/mac/我的文件/Mycode/new/new/pyIPR/data/PROCAR'
>>> eigenval_path = "/Users/mac/我的文件/Mycode/new/new/pyIPR/data/EIGENVAL"
>>> vasprun_path = "/Users/mac/我的文件/Mycode/new/new/pyIPR/data/vasprun.xml"
>>> output_path = "/Users/mac/我的文件/Mycode/new/new/pyIPR/data/IPRs.csv"
>>> IPR_calculator = IPRCalculator(
                        procar_path=procar_path,
                        eigenval_path=eigenval_path,
                        output_csv_path=output_path
                        )
>>> print(IPR_calculator)
+----------------+----------+--------+-------+
|   spins_lst    | nkpoints | nbands | nions |
+----------------+----------+--------+-------+
| [<Spin.up: 1>] |    25    |  480   |  108  |
+----------------+----------+--------+-------+

# 计算 feimi 能级
>>> vasprun = Vasprun(vasprun_path)
>>> dos_data = vasprun.complete_dos
>>> fermi = dos_data.efermi

# 计算减去 fermi 能级的 IPR
>>> IPR_calculator.concat_energys_IPRs(Spin(1), efermi=efermi)    # 运行完毕后，产生 "/Users/mac/我的文件/Mycode/new/new/pyIPR/data/IPRs.csv" 文件
```