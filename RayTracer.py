# Reece Pretorius

import sys
import numpy as np
from IOHelper import *
import matplotlib.pyplot as plt


def raytrace(params):
    if params["depth"] > 3:
        return np.zeros(3)

    intersection = calculate_intersects(params)

    if intersection is None:
        if params["depth"] > 1:
            return np.zeros(3)
        else:
            return params["back"]
    
    sphere, dist = intersection
    ambient = sphere['rgb'] * sphere['Ka'] * params["ambient"]
    diffuse = np.zeros(3)
    specular = np.zeros(3)
    intersect_point = params["eye_pos"] + params["ray_dir"] * dist
    normal = intersect_point - sphere['pos']
    normal = np.matmul(np.linalg.inv(sphere['mat'].transpose()), np.matmul(np.append(normal, 1), sphere['inv_mat']))[:3]
    normal = normal / np.linalg.norm(normal)

    if not(sphere['Kd'] == 0.0 and sphere['Ks'] == 0.0):
        for light in params["lights"]: # diffuse + specular
            light_intersect_point = light['pos'] - intersect_point

            diffuse_params = {
                "eye_pos": intersect_point,
                "ray_dir": light_intersect_point,
                "spheres": params["spheres"],
                "lights": params["lights"],
                "depth": 1
            }

            shadow = calculate_intersects(diffuse_params)
            
            if shadow is not None:
                continue

            intensity = 2 * (np.dot(normal, light_intersect_point)) * normal - light_intersect_point
            reflection_dir = intensity / np.linalg.norm(intensity)
            light_intersect_point = light_intersect_point / np.linalg.norm(light_intersect_point)
            viewing_dir = -intersect_point / np.linalg.norm(-intersect_point)
            diffuse = np.add(diffuse, sphere['Kd'] * light['rgb'] * np.dot(light_intersect_point, normal) * sphere['rgb'])
            specular = np.add(specular, sphere['Ks'] * light['rgb'] * np.dot(reflection_dir, viewing_dir) ** sphere['n'])
    
    reflection = np.zeros(3) # color of reflection.

    if sphere['Kr'] != 0.0: # getting reflection color an next depth.
        params["depth"] = params["depth"] + 1
        ray_dir_reflect = (-2) * np.dot(normal, params["ray_dir"]) * normal + params["ray_dir"]

        refelection_params = {
            "eye_pos": intersect_point,
            "ray_dir": ray_dir_reflect,
            "spheres": params["spheres"],
            "lights": params["lights"],
            "depth": params["depth"],
            "ambient": params["ambient"],
            "back": params["back"]
        }

        reflection = sphere['Kr'] * raytrace(refelection_params)

    return ambient + diffuse + specular + reflection


def calculate_intersects(params):
    result = None
    dist = np.inf

    for sphere in params["spheres"]:
        eye_inverse = np.matmul(sphere['inv_mat'], np.append(params["eye_pos"], 1))[:3]
        ray_inverse = np.matmul(sphere['inv_mat'], np.append(params["ray_dir"], 0))[:3]

        a = np.linalg.norm(ray_inverse) ** 2
        b = np.dot(eye_inverse, ray_inverse)
        c = np.linalg.norm(eye_inverse) ** 2 - 1

        if (b ** 2 - a * c) >= 0:
            intersections = (
                (-b + np.sqrt(b ** 2 - a * c)) / a,
                (-b - np.sqrt(b ** 2 - a * c)) / a
            )
        else:
            intersections = None
        
        if intersections is not None:
            for intersection in intersections:
                if intersection < dist and intersection > 1e-6:
                    result = (sphere, intersection)
                    dist = intersection
    return result


def main():
    file = sys.argv[1]
    input_params = Parse_Input_File(file)

    eye_pos = np.array([0, 0, 0])
    img = np.empty((input_params["res"][0], input_params["res"][1], 3))

    for i in range(input_params["res"][0]): # HEIGHT
        for j in range(input_params["res"][1]): # WIDTH
            direction = np.array([ # (x, y, z) direction vector.
                (input_params["right"] * (2 * j / input_params["res"][1] - 1)), 
                (input_params["top"] * (2 * (input_params["res"][0] - i) / input_params["res"][0] - 1)), 
                (-input_params["near"])
            ])
            
            rayTrace_Params = {
                "eye_pos": eye_pos,
                "ray_dir": direction + eye_pos,
                "spheres": input_params["spheres"],
                "lights": input_params["lights"],
                "depth": 1,
                "ambient": input_params["ambient"],
                "back": input_params["back"],
                "near": input_params["near"]
            }
            img[i, j] = raytrace(rayTrace_Params)

    Output_Ppm_File(input_params["output"], input_params["res"][1], input_params["res"][0], img)

if __name__ == "__main__":
    main()