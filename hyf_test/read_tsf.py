"""
    coding: utf-8
    Project: Fiber_Query
    File: read_tsf.py
    Author: xieyu
    Date: 2025/8/26 17:53
    IDE: PyCharm
"""

import numpy as np

import numpy as np


def read_mrtrix_tsf(filename):
    """
    Reads a MRtrix3 Track Scalar File (.tsf) and returns its header and data.
    This version is more robust against encoding errors by reading in binary mode.

    Args:
        filename (str): The path to the .tsf file.

    Returns:
        dict: A dictionary containing the header information and a list of NumPy arrays,
              where each array holds the scalar values for a single track.
    """
    tsf = {}
    header_end_offset = None

    # --- NEW: Map MRtrix datatype strings to NumPy's format ---
    # This dictionary will prevent the 'data type not understood' error
    datatype_map = {
        'float32': 'f4',
        'float64': 'f8',
        'int8': 'i1',
        'int16': 'i2',
        'int32': 'i4',
        'int64': 'i8',
    }

    try:
        # Step 1: Open the file in binary mode ('rb') to avoid encoding errors
        with open(filename, 'rb') as f:
            first_line = f.readline().decode('ascii', errors='ignore')
            if not first_line.startswith('mrtrix track scalars'):
                print(f"{filename} is not in MRtrix format.")
                return None

            for line_bytes in f:
                line = line_bytes.decode('ascii', errors='ignore').strip()

                if line == 'END':
                    break

                parts = line.split(':')
                if len(parts) >= 2:
                    key = parts[0].strip().lower()
                    value = ':'.join(parts[1:]).strip()

                    if key == 'datatype':
                        tsf['datatype'] = value
                    elif key == 'file':
                        try:
                            parts_file = value.split()
                            header_end_offset = int(parts_file[-1])
                        except (ValueError, IndexError):
                            print("Error parsing header 'file' entry. Aborting.")
                            return None
                    else:
                        tsf[key] = value

            if 'datatype' not in tsf or header_end_offset is None:
                print("Critical entries missing in header - aborting.")
                return None

            # Step 2: Set the file pointer to the start of the data based on the offset
            f.seek(header_end_offset, 0)

            # --- MODIFIED: Convert the datatype to NumPy's format ---
            datatype_str = tsf['datatype'].lower()
            if datatype_str.endswith('le'):
                byte_order = '<'
                datatype_key = datatype_str[:-2]
            elif datatype_str.endswith('be'):
                byte_order = '>'
                datatype_key = datatype_str[:-2]
            else:
                byte_order = '='
                datatype_key = datatype_str

            # Use the map to get the correct NumPy type string
            if datatype_key not in datatype_map:
                print(f"Unsupported data type '{datatype_key}' in header.")
                return None

            numpy_dtype = f'{byte_order}{datatype_map[datatype_key]}'

            # Step 3: Read the binary data
            raw_data = np.fromfile(f, dtype=numpy_dtype)

    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None

    # Step 4: Split the data based on NaN values
    nan_indices = np.where(np.isnan(raw_data))[0]

    tsf['data'] = []
    start_index = 0

    for end_index in nan_indices:
        track_data = raw_data[start_index:end_index]
        if track_data.size > 0:
            tsf['data'].append(track_data)
        start_index = end_index + 1

    return tsf


def main():
    tsf = read_mrtrix_tsf("/data/hyf/swm/hierarchy_clustering/atlas_version/scaler_replaced_downsampled_7Network_top2.tsf")

    for key in tsf.keys():
        print(key)
        if key == 'data':
            print(tsf[key][:10])
        else:
            print(tsf[key])

    # print(tsf.keys())
    #
    # print(tsf['data'][:10])

    pass


if __name__ == '__main__':
    main()
