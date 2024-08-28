

import json
import os
import shutil

# Specify the path to your JSON file
file_path = 'E:/Tasnim/PhD_Project/IAW_3D_CAD_file_retrieval/IKEAAssemblyInTheWildDataset.json'
DATASET_DIR = os.path.join(os.getcwd(),'dataset') # D:\IKEAAssemblyInTheWildDataset\dataset


def main():

    # Open and load the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)


    # Now 'data' contains the content of the JSON file as a Python dictionary
    print(len(data)) # 420

    subcat_count = 0
    video_count = 0

    for c in range (0, len(data), 1):
       
        cad_path = os.path.join(DATASET_DIR, data[c]['category'], data[c]['subCategory'], data[c]['id'], '3D_model')

        if  len(os.listdir(cad_path))!= 0:
            subcat_count += 1
            video_count += len(data[c]['videoList'])

    print("total sub category: ", subcat_count)
    print("total videos: ", video_count)  
        

        


      
    

if __name__ == "__main__":
    main()








