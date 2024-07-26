# https://koncept.orientering.se/provapaaktiviteter/hittaut/skelleftea/
from os import makedirs
from math import radians, sin, cos, atan2, sqrt
from time import sleep

import requests
import yaml

home_address = 'Kågevägen 24, 93137 Skellefteå'
near_threshold = 1.0  # in kilometers


# as the crow flies distance in kilometers between two coordinates
def haversine(lat1, lon1, lat2, lon2):
    r = 6371  # radius of the earth in kilometers
    phi1, lambda1 = radians(lat1), radians(lon1)
    phi2, lambda2 = radians(lat2), radians(lon2)
    delta_phi = phi2 - phi1
    delta_lambda = lambda2 - lambda1
    a = sin(delta_phi / 2) ** 2 + cos(phi1) * cos(phi2) * sin(delta_lambda / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return r * c


def fetch_easy_locations():
    resp = requests.get('https://koncept.orientering.se/api/v1/locations/104/checkpoints/?format=json')
    resp.encoding = 'utf-8'
    locations = resp.json()
    easy_locs = sorted([loc for loc in locations
                        if loc['level'] == 10
                        and loc['accessibility_adjusted']],
                       key=lambda loc: loc['number'])
    return easy_locs


def get_lat_long(address):
    data = requests.get(f'https://nominatim.openstreetmap.org/search?q={address}&format=json').json()
    coord = dict(lat=float(data[0]['lat']), lng=float(data[0]['lon'])) if data else None
    print(f'Fetched coordinates {coord} for address "{address}"')
    return coord


def get_walking_distance(start_lat, start_lon, end_lat, end_lon):
    data = requests.get(f"http://router.project-osrm.org/route/v1/walking/{start_lon},{start_lat};{end_lon},{end_lat}?overview=false").json()
    if data["code"] == "Ok":
        dist = data["routes"][0]["distance"]  # in meters
        print(f'Distance from ({start_lat}, {start_lon}) to ({end_lat}, {end_lon}) is {dist}m')
        sleep(0.3)
        return dist
    else:
        return None


def main():
    # my_home = dict(lat=64.75587868955067, lng=20.965543282936686)
    my_home = get_lat_long(home_address)

    def near(loc):
        return haversine(my_home['lat'], my_home['lng'], loc['lat'], loc['lng']) <= near_threshold

    easy_locs = fetch_easy_locations()
    near_easy_locs = [loc for loc in easy_locs if near(loc)]
    print(len(near_easy_locs))

    distances = [
        [loc1["number"], loc2["number"], get_walking_distance(loc1['lat'], loc1['lng'], loc2['lat'], loc2['lng'])]
        for loc1 in near_easy_locs
        for loc2 in near_easy_locs
        if loc1 != loc2]

    obj = dict(locations=[loc['number'] for loc in near_easy_locs],
               distances=distances,
               descriptions=[[loc['number'], loc['short_description']] for loc in near_easy_locs],
               coordinates=[[loc['number'], loc['lat'], loc['lng']] for loc in near_easy_locs])

    makedirs('data', exist_ok=True)
    with open('data/data.yaml', 'w', encoding='utf-8') as fp:
        yaml.dump(obj, fp, default_flow_style=False, allow_unicode=True)


if __name__ == '__main__':
    main()
