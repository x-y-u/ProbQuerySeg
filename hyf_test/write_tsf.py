"""
    coding: utf-8
    Project: Fiber_Query
    File: write_tsf.py
    Author: xieyu
    Date: 2025/8/26 18:35
    IDE: PyCharm
"""


import numpy as np

def write_mrtrix_tsf(tsf_data, filename):
    """
    将包含MRtrix纤维束标量数据的字典写入到 .tsf 文件。

    参数：
        tsf_data (dict): 一个字典，其中必须包含一个名为 'data' 的字段，
                         其值为 NumPy 数组的列表，每个数组包含一条纤维束的标量值。
                         字典中的其他字段将被写入为头部条目。
        filename (str): 输出 .tsf 文件的路径。
    """

    # 检查是否包含必需的 'data' 字段
    if 'data' not in tsf_data or not isinstance(tsf_data['data'], list):
        raise ValueError("输入 'tsf_data' 必须是一个包含 'data' 字段的字典，且该字段的值为列表。")

    # 将所有纤维束数据转换为一个扁平的 NumPy 数组
    all_scalars = []
    for track_scalars in tsf_data['data']:
        # 将当前纤维束的标量值添加到列表中
        all_scalars.extend(track_scalars)
        # 按照 .tsf 格式，在每条纤维束数据后添加一个 NaN 作为分隔符
        all_scalars.append(np.nan)

    # 将列表转换为 NumPy 数组，强制使用 float32 类型
    flat_data = np.array(all_scalars, dtype=np.float32)

    # 步骤 1：写入文件头部 (Header)
    with open(filename, 'w') as f:
        # 写入强制性的第一行和一些常见的头部字段
        f.write('mrtrix track scalars\n')
        f.write('datatype: Float32LE\n')
        f.write(f'count: {len(tsf_data["data"])}\n')

        # 写入用户提供的其他头部字段
        for key, value in tsf_data.items():
            # 跳过内部使用或强制写入的字段
            if key in ['data', 'count', 'datatype']:
                continue
            if isinstance(value, list):
                # 如果值是列表，用空格连接
                f.write(f"{key}: {' '.join(map(str, value))}\n")
            else:
                f.write(f"{key}: {value}\n")

        # 获取当前文件位置，用于计算二进制数据的偏移量
        data_offset = f.tell()

        # MATLAB 代码会对齐头部，使其字节数是4的倍数。我们也这样做。
        padding = (4 - (data_offset % 4)) % 4
        data_offset += padding

        # 写入文件偏移量和 'END' 标记
        f.write(f'file: . {data_offset}\n')
        f.write('END\n')

        # 写入用于对齐的填充字节（空格）
        f.write(' ' * padding)

    # 步骤 2：追加二进制数据
    # 我们以二进制追加模式 ('ab') 再次打开文件，以添加二进制数据
    with open(filename, 'ab') as f_binary:
        # 使用 numpy.tofile() 高效地将 NumPy 数组写入文件
        flat_data.tofile(f_binary)


def main():
    pass


if __name__ == '__main__':
    main()
