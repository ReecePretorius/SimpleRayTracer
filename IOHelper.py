# Reece Pretorius

import numpy as np


def Parse_Input_File(infile):

    input_params = {
        "near": None,
        "left": None,
        "right": None,
        "bottom": None,
        "top": None,
        "res": None,
        "spheres": [],
        "lights": [],
        "back": None,
        "ambient": None,
        "output": None
    }
    
    with open(infile) as file:
        lines = file.readlines()
        
        for line in lines:
            words = line.split()

            if len(words) < 2:
                continue

            if words[0] == 'NEAR':
                input_params['near'] = float(words[1])

            if words[0] == 'LEFT':
                input_params['left'] = float(words[1])

            if words[0] == 'RIGHT':
                input_params['right'] = float(words[1])

            if words[0] == 'BOTTOM':
                input_params['bottom'] = float(words[1])

            if words[0] == 'TOP':
                input_params['top'] = float(words[1])

            if words[0] == 'RES':
                input_params['res'] = (int(words[1]), int(words[2]))

            if words[0] == 'SPHERE':

                if len(words) != 16:
                    continue

                sphere = {}
                sphere['pos'] = np.array([
                    float(words[2]), # x
                    float(words[3]), # y
                    float(words[4])  # z
                ])
                
                sphere['scl'] = np.array([
                    float(words[5]), # x
                    float(words[6]), # y
                    float(words[7])  # z
                ])

                sphere['rgb'] = np.array([
                    float(words[8]), # red
                    float(words[9]), # green
                    float(words[10]) # blue
                ])

                sphere['mat'] = np.array(
                [
                    [sphere['scl'][0], 0, 0, sphere['pos'][0]],
                    [0, sphere['scl'][1], 0, sphere['pos'][1]],
                    [0, 0, sphere['scl'][2], sphere['pos'][2]],
                    [0, 0, 0, 1]
                ])

                sphere['inv_mat'] = np.array(
                [
                    [1 / sphere['scl'][0], 0, 0, -sphere['pos'][0] / sphere['scl'][0]],
                    [0, 1 / sphere['scl'][1], 0, -sphere['pos'][1] / sphere['scl'][1]],
                    [0, 0, 1 / sphere['scl'][2], -sphere['pos'][2] / sphere['scl'][2]],
                    [0, 0, 0, 1]
                ])

                sphere['Ka'] = float(words[11])
                sphere['Kd'] = float(words[12])
                sphere['Ks'] = float(words[13])
                sphere['Kr'] = float(words[14])
                sphere['n'] = float(words[15])

                input_params['spheres'].append(sphere)

            if words[0] == 'LIGHT':
                
                if(len(words) != 8):
                    continue
                
                light = {}
                light['pos'] = np.array([
                    float(words[2]), 
                    float(words[3]), 
                    float(words[4])
                ])
                
                light['rgb'] = np.array([
                    float(words[5]), 
                    float(words[6]), 
                    float(words[7])
                ])

                input_params['lights'].append(light)

            if words[0] == 'BACK':
                input_params['back'] = (float(words[1]), float(words[2]), float(words[3]))

            if words[0] == 'AMBIENT':
                input_params['ambient'] = (float(words[1]), float(words[2]), float(words[3]))

            if words[0] == 'OUTPUT':
                input_params['output'] = words[1]

    return input_params


def Output_Ppm_File(file, w, h, img):
    img = np.clip(img * 255, 0, 255)
    
    header = f'P6 {w} {h} {255}\n'
    
    with open(file, 'wb') as f:
        f.write(bytearray(header, 'ascii'))
        f.write(img.astype('int8').tobytes())