import json
import pprint
#from geojson import Feature, Point, FeatureCollection
import geojson

source_file = "sl_data.json"

with open(source_file,'r') as f:
    source_data = json.load(f)

points_list = list()
feature_list = list()

# for each node, create a Point and a Feature and add it to the FeatureCollection
for node in source_data['results']:
    type1_count = 0
    type2_count = 0
    if node['status'] != 'ok':
        continue
    if len(node['charge_availability']) > 1:
        charge_kind = ''
        for chargepoint in node['charge_availability']:
            if 'type2_fast' in chargepoint['availability']:
                type2_count += chargepoint['availability']['type2_fast']
            if 'type1_standard' in chargepoint['availability']:
                type1_count += chargepoint['availability']['type1_standard']
            if charge_kind == '':
                charge_kind = chargepoint['kind']
            elif charge_kind != chargepoint['kind']:
                print(str(node['id']) + " is a complex location")
                continue
    point = geojson.Point((node['lng'],node['lat']))
    parking_spaces = len(node['charge_availability'])
    feature_properties = {
        'access':'customers',
        'amenity':'charging_station',
        'capacity': parking_spaces,
        'name':node['public_name'],
        'opening_hours': '24/7',
        'operator': 'Source London',
    }
    if type2_count > 0:
        feature_properties['socket:type2'] = type2_count
    if type1_count > 0:
        feature_properties['socket:type1'] = type1_count

    feature = geojson.Feature(geometry=point,properties=feature_properties)
    feature_list.append(feature)

coll = geojson.FeatureCollection(feature_list)
f = open('sl_osm.geojson','w')
f.write(geojson.dumps(coll))
