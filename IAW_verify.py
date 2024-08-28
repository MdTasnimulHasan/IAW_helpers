import json
import os
# Specify the path to your JSON file
file_path = 'D:\IKEAAssemblyInTheWildDataset\dataset\IKEAAssemblyInTheWildDataset.json'
BASE_YOUTUBE_STR = 'https://www.youtube.com/watch?v='
DATASET_DIR = os.path.join(os.getcwd(),'dataset') # D:\IKEAAssemblyInTheWildDataset\dataset


# Open and load the JSON file
with open(file_path, 'r') as file:
    data = json.load(file)


# Now 'data' contains the content of the JSON file as a Python dictionary
print(len(data)) # 420

count = 0
for c in range (0, len(data), 1):
    # print(data[0].keys())
    '''
    "id": "s79011430",
    "name": "KIVIK",
    "category": "Furniture",
    "subCategory": "Sofas",
    '''
    for vl in range (0, len(data[c]['videoList'])):
        # print(len(data[]['videoList'])) # 6
        # print(data[0]['videoList'][0]) 
        '''
        {'url': 'https://www.youtube.com/watch?v=eJcsxzPKO-U', 'title': 'IKEA kivik 3 seat sofa assembly guide very detailed', 'duration': 2179, 'height': 1080, 'width': 1920, 'fps': 30, 'annotation': [{'start': 394.8, 'end': 513.2, 'action': 0}, {'start': 607.9, 'end': 876.4, 'action': 1}, {'start': 923.7, 'end': 1310.6, 'action': 2}, {'start': 1342.2, 'end': 1429, 'action': 3}, {'start': 1446.8, 'end': 1774.5, 'action': 4}, {'start': 1784.3, 'end': 1815.9, 'action': 5}, {'start': 1867.2, 'end': 1981.7, 'action': 6}, {'start': 1997.5, 'end': 2040.9, 'action': 7}, {'start': 2050.8, 'end': 2100.1, 'action': 8}, {'start': 2108, 'end': 2165.3, 'action': 9}], 'people_count': '1', 'person_view': 'firstPerson', 'is_fixed': 'fixed', 'is_indoor': 'indoor'}
        '''
        # print(data[0]['videoList'][0].keys())
        '''
        ['url', 'title', 'duration', 'height', 'width', 'fps', 'annotation', 'people_count', 'person_view', 'is_fixed', 'is_indoor']
        '''
        # print(data[0]['videoList'][0]['url']) # https://www.youtube.com/watch?v=eJcsxzPKO-U

        video_id = data[c]['videoList'][vl]['url'].replace(BASE_YOUTUBE_STR, "") + '.mp4'
        # print(video_id)
        video_path = os.path.join(DATASET_DIR, data[c]['category'], data[c]['subCategory'], data[c]['id'], 'video', video_id)
        # print(video_path) # D:\IKEAAssemblyInTheWildDataset\dataset\Furniture\Sofas\s79011430\video\eJcsxzPKO-U.mp4

        if os.path.exists(video_path):
            print(video_path, ": Exists")
            count += 1
        else:
            print(video_path, ": WARNING!!! VIDEO FILE NOT FOUND")
print("total videos found: ", count)