'''
Author: Uper 41718895+Hyliu-BUAA@users.noreply.github.com
Date: 2022-06-01 15:58:52
LastEditors: Uper 41718895+Hyliu-BUAA@users.noreply.github.com
LastEditTime: 2022-06-02 13:36:55
FilePath: /pyIPR/myIPR.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import pandas as pd
import numpy as np
from prettytable import PrettyTable
from pymatgen.io.vasp import Procar
from pymatgen.io.vasp.outputs import Eigenval
from pymatgen.electronic_structure.core import Spin


class IPRCalculator(object):
    '''
    Attributes
    ----------
        1. self.procar: 
            pymatgen 读取的 PROCAR 对象
        2. self.spins_lst: list of `pymatgen.electronic_structure.core.Spin`
            - 若自旋打开, self.spins_lst = [<Spin.up: 1>, [<Spin.up: -1>]]
            - 若自旋关闭, self.spins_slt = [<Spin.up: 1>]
        3. self.nkpoints: int
            The number of K-points (K 点的数目)
        4. self.nbands: int
            The number of bands (能带的数目)
        5. self.nions: int
            The number of ions (体系的总原子数)
    '''
    def __init__(self, procar_path:str, eigenval_path:str, output_csv_path:str):
        '''
        Parameters
        ----------
            1. procar_path: str
                The path of PROCAR
        '''
        self.procar_path = procar_path
        self.eigenval_path = eigenval_path
        self.output_csv_path = output_csv_path

        self.procar = Procar(procar_path)
        self.spins_lst, self.nkpoints, self.nbands, self.nions = \
                                    self._get_info()


    def __str__(self):
        return self.__repr__()

    
    def __repr__(self):
        table = PrettyTable(["spins_lst", "nkpoints", "nbands", "nions"])
        table.add_row([self.spins_lst, self.nkpoints, self.nbands, self.nions])
        print(table)
        return ''


    def _get_info(self):
        '''
        Description
        -----------
            1. Get the spins_lst:
                - `pymatgen.electronic_structure.cores.Spin`
                - e.g. spins_lst = [ Spin(1) ]
                - e.g. spins_lst = [ Spin(1), Spin(-1) ]

            2. Get the number of kpoints, bands, ions
                (计算 K点数、能带数、离子数)

        Note
        ----
            1. Procar.data:
                1.1. type(self.procar.data) = collections.defaultdict
                1.2.  {
                        spin: nd.array accessed with (k-point index, band index,
                                                    ion index, orbital index)
                      }   
        '''
        spins_lst = []

        for key, _ in self.procar.data.items():
            spins_lst.append(key)

        return spins_lst, self.procar.nkpoints, self.procar.nbands, self.procar.nions


    def get_one_item(self, spin:Spin, idx_kpoint:int, idx_band:int, idx_ion:int, idx_orbital:int):
        '''
        Description
        -----------
            1. 根据以下参数取出 dos:
                - spin
                - idx_kpoint
                - idx_band
                - idx_ion
                - idx_orbital
            2. 本函数可以用于测试功能
        
        Note
        ----
            1. 注意 VASP 输出的 PROCAR 是从 `1` 开始计数的
            2. 本函数的 `idx_kpoint`, `idx_band`, `idx_ion`, `idx_orbital` 是从 `0` 开始计数的
        '''
        ### 误差来源于小数点后第 3 位
        return self.procar.data[spin][idx_kpoint, idx_band, idx_ion, idx_orbital].astype(np.float64)
    

    def _get_array_for_IPR(self, spin:Spin=Spin(1)):
        '''
        Description
        -----------
            1. 被 `self.calculate_IPR()` 调用
        
        Note
        ----
            1. 若打开了自旋，则需要连续两次 (针对不同的自旋方向) 调用 `self._get_array_for_IPR()`

        Do Something
        ------------
            ```
            for idx_kpoint in range(self.nkpoints):
                ### 遍历所有的 kpoints

                for idx_band in range(self.nbands):
                    ### 遍历所有的 bands

                    for idx_ion in range(self.nions):
                        ### 遍历所有的 ios
                        ...
            ```
        '''
        # print(self.procar.data[Spin(1)][:, :, :, :].shape)
        # (25, 480, 108, 9)  -- (nkpoints, nbands, nions, norbits)
        # print(self.procar.data[Spin(1)][:, :, :, :].sum(axis=3).shape)        
        # (25, 480, 108) -- (nkpoints, nbands, nions)

        ### 指定 kpoint, band, ion 后，对轨道进行求和
        dos_sum_3d = self.procar.data[spin][:, :, :, :].sum(axis=3)
        return dos_sum_3d
    

    def get_IPRs_lst(self, spin:Spin=Spin(1)):
        '''
        Description
        -----------
            1. 计算 IPR
        
        Return 
        ------
            1. IPRs_lst: 
                - 与 energys_lst 一一对应

        Note
        ----
            1. 若打开了自旋，则需要连续两次 (针对不同的自旋方向) 调用 `self._get_array_for_IPR()`
        '''
        IPRs_lst = [] 

        '''
        Note
        -----
            1. 对 `dos_sum_3d` 求和得到 `tot_dos_per_kpoint_band` 最后一个数值 `0.693`

        dos_sum_3d
        ----------
            e.g. dos_sum_3d[-1, -1, :]

            [0.005 0.014 0.008 0.036 0.015 0.024 0.028 0.017 0.015 0.024 0.011 0.008
            0.008 0.009 0.011 0.012 0.013 0.006 0.005 0.026 0.003 0.01  0.013 0.006
            0.016 0.008 0.007 0.019 0.006 0.013 0.013 0.011 0.006 0.005 0.008 0.015
            0.001 0.003 0.007 0.002 0.001 0.003 0.002 0.008 0.008 0.002 0.004 0.
            0.003 0.005 0.002 0.002 0.003 0.002 0.002 0.002 0.001 0.008 0.006 0.003
            0.004 0.001 0.004 0.004 0.004 0.003 0.002 0.001 0.002 0.006 0.003 0.003
            0.009 0.004 0.003 0.003 0.003 0.003 0.003 0.002 0.002 0.002 0.005 0.004
            0.002 0.002 0.004 0.002 0.006 0.009 0.004 0.001 0.002 0.001 0.003 0.003
            0.002 0.003 0.008 0.002 0.002 0.001 0.005 0.002 0.001 0.004 0.005 0.005]

        tot_dos_per_kpoint_band
        -----------------------
            e.g.

            [[0.992 0.992 0.992 ... 0.687 0.673 0.679]
             [0.992 0.992 0.992 ... 0.676 0.691 0.695]
             [0.992 0.992 0.992 ... 0.683 0.695 0.672]
             ...
             [0.992 0.992 0.992 ... 0.695 0.683 0.693]
             [0.992 0.992 0.992 ... 0.7   0.683 0.698]
             [0.992 0.992 0.992 ... 0.676 0.688 0.693]]
        '''
        ### dos_sum_3d.shape = (nkpoints, nbands, nions)
        dos_sum_3d = self._get_array_for_IPR(spin=spin)
        #print(dos_sum_3d[-1, -1, :])

        ### tot_dos_per_kpoint_band.shape = (nkpoints, nbands)
        tot_dos_per_kpoint_band = dos_sum_3d.sum(axis=2)
        #print(tot_dos_per_kpoint_band)

        for idx_kpoint in range(self.nkpoints):
            for idx_band in range(self.nbands):
                # 对应 PROCAR 里的 “tot    0.992  0.000  0.000  0.000  0.000  0.000  0.000  0.000  0.000  0.992”
                # 对应每个 Kpoint、band 的最后一行（对所有离子进行加和）

                denominator = np.square( tot_dos_per_kpoint_band[idx_kpoint, idx_band] )
                numerator = np.sum( np.square( dos_sum_3d[idx_kpoint, idx_band, :] ) )
                IPR = numerator / denominator
                IPRs_lst.append(IPR)
        
        return IPRs_lst
                                

    def get_energys_lst(self, spin:Spin=Spin(1)):
        '''
        Description
        -----------
            1. 得到 kpoint, band 对应的 energy
            2. len( energys_lst ) == self.nkpoints * self.nbands
        
        Return 
        ------
            1. energys_lst: list of float


        Note
        ----
            1. `pymatgen.io.vasp.outputs.Eigenvalues`:
                - a dict of {(spin): np.ndarray(shape=(nkpt, nbands, 2))}. 

                - This representation is based on actual ordering in VASP
                  is meant as an intermediate representation to be converted into proper objects. 
                - The kpoint index is 0-based (unlike the 1-based indexing in VASP).
        '''

        energys_lst = []

        eigenval = Eigenval(self.eigenval_path)
        eigenval_3d_array = eigenval.eigenvalues[spin]
        for idx_kpoint in range(self.nkpoints):
            for idx_band in range(self.nbands):
                energy = eigenval_3d_array[idx_kpoint, idx_band, 0]
                energys_lst.append(energy)
        return energys_lst

    
    def concat_energys_IPRs(self, spin:Spin=Spin(1), efermi:float=None):
        '''
        Description
        -----------
            1. 调用 `self.get_IPRs_lst()` 和 `self.get_energys_lst()` 

        Parameters
        ----------
            1. spin: pymatgen.electronic_structure.core.Spin
                自旋方向
            2. efermi: float
                费米能级：
                    - None: 直接用真空能级
                    - float: 减去费米能级
        '''
        IPRs_lst = self.get_IPRs_lst(spin=spin)
        energys_lst = self.get_energys_lst(spin=spin)

        if efermi:
            energys_lst = self._sub_efermi(energys_lst=energys_lst,
                                            efermi=efermi)

        df = pd.DataFrame(np.matrix([energys_lst, IPRs_lst]).T, columns=["energy", "IPR"])
        df = df.sort_values(by=["energy"])
        df.to_csv(self.output_csv_path, sep=',', index=False)
        
    def _sub_efermi(self, energys_lst:list, efermi:float):
        '''
        Description
        -----------
            1. 被 `self.concat_energys_IPRs()` 调用

        Parameters
        ----------
            1. energys_lst: list
                EIGENVAL 中所有能量组成的 list
            2. efermi: float
                费米能级
        '''
        energys_lst = [ (energy - efermi) for energy in energys_lst ]
        return energys_lst





if __name__ == "__main__":
    procar_path = '/Users/mac/我的文件/Mycode/new/new/pyIPR/data/PROCAR'
    eigenval_path = "/Users/mac/我的文件/Mycode/new/new/pyIPR/data/EIGENVAL"
    output_path = "/Users/mac/我的文件/Mycode/new/new/pyIPR/data/IPRs.csv"
    efermi = None

    IPR_calculator = IPRCalculator(
                        procar_path=procar_path,
                        eigenval_path=eigenval_path,
                        output_csv_path=output_path
                        )

    print(IPR_calculator)

    # 计算真空能级的 IPR
    IPR_calculator.concat_energys_IPRs(spin=Spin(1), efermi=efermi)