import json

# get the bounding box for the dataset
# check if the number of nodes is as expected (we don't get extra nodes if we zoom in?)
dataset_filename = 'sl_data.json'
(max_long, min_long, max_lat, min_lat) = (-180,180,-90,90)

with open('sl_data.json', 'r') as d:
    data = json.load(d)
    for node in data['results']:
        if node['lat'] > max_lat:
            max_lat = node['lat']
        if node['lat'] < min_lat:
            min_lat = node['lat']
        if node['lng'] > max_long:
            max_long = node['lng']
        if node['lng'] < min_long:
            min_long = node['lng']
    print("Bounding box: "+str(max_long)+","+str(min_lat)+";"+str(min_long)+","+str(max_lat))
