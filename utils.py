import numpy as np
import xml.etree.ElementTree as ET



def CABC_Force(real_time, real_force, guess_time, guess_force):
    common_time = np.linspace(0.0, max(real_time.max(), guess_time.max()), num=200)

    # Resample both curves on this time grid
    real_force_resampled = np.interp(common_time, real_time, real_force)
    guess_force_resampled = np.interp(common_time, guess_time, guess_force)

    mse_force = np.mean((real_force_resampled-guess_force_resampled)**2)
    
    return mse_force




def CABC_Displacement(real_time, real_disp, guess_time, guess_disp):
    common_time = np.linspace(0.0, max(real_time.max(), guess_time.max()), num=200)

    # Resample both curves on this time grid
    real_disp_resampled = np.interp(common_time, real_time, real_disp)
    guess_disp_resampled = np.interp(common_time, guess_time, guess_disp)

    mse_disp = np.mean((real_disp_resampled-guess_disp_resampled)**2)
    
    return mse_disp

def parse_real_disp(real_disp_path):
    real_tree = ET.parse(real_disp_path)
    real_root = real_tree.getroot()
    real_data = []

    for time_block, dept_block in zip(real_root.findall('.//Block//IndpVar'), real_root.findall('.//Block')):
        time_value = time_block.attrib.get('Value')
        dept_value = dept_block.find('DeptValues').text.strip()
        real_data.append((time_value, dept_value))

    real_data_array = np.array([(float(x), float(y)) for x, y in real_data])
    real_disp_time = real_data_array[:, 0]
    real_disp = real_data_array[:, 1] * 1000
    
    return real_disp_time, real_disp



def parse_real_force(real_force_path):
    real_tree = ET.parse(real_force_path)
    real_root = real_tree.getroot()
    real_data = []

    for time_block, dept_block in zip(real_root.findall('.//Block//IndpVar'), real_root.findall('.//Block')):
        time_value = time_block.attrib.get('Value')
        dept_value = dept_block.find('DeptValues').text.strip()
        real_data.append((time_value, dept_value))

    real_data_array = np.array([(float(x), float(y)) for x, y in real_data])
    real_force_time = real_data_array[:, 0]
    real_force = real_data_array[:, 1] * 0.0001019716
    
    return real_force_time, real_force