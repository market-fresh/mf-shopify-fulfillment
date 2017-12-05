import datetime
import pandas as pd
import math

from order_extraction import simulate_extract_orders
from order_extraction import extract_orders
from order_email import sendemail

import settings

#Clean up data frame to include only today orders and sorted according to delivery_time
def cleanup_data_frame(df, timings, timeIndex):
    now = datetime.datetime.now()
    today = now.strftime("%d-%m-%Y")
    tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
    df = df.loc[df['delivery_day'] == today]
    return df

#Function to generate the fulfillment route
def generate_fulfillment_map(df, origin, destination):
    data = list()
    while( len(destination)>0 ):
        nearest_destination = get_nearest_destination(origin, destination)
        data_tmp = df.loc[df['order_number'] == nearest_destination['order']].values.flatten().tolist()
        if data_tmp:
            data.append(data_tmp[0:8])
            if(math.isnan(data_tmp[7])):
                origin = origin
            elif(math.isnan(data_tmp[6])):
                origin = origin
            else:
                origin = {'lat': data_tmp[7], 'lng': data_tmp[6]}
        destination[:] = [d for d in destination if d.get('order') != nearest_destination['order']]
    return data

#Function to generate the distances of origin to each nearest destination
def get_nearest_destination(origin, destination):
    destination_distances = list()
    for place in destination:
        distance_lat = abs(origin['lat'] - place['lat'])
        distance_lng = abs(origin['lng'] - place['lng'])
        distance = math.sqrt(pow(distance_lat, 2) + pow(distance_lng, 2))
        destination_distances.append({'order':place['order'], 'distance': distance})
    distance_sorted_index = get_closest(destination_distances)
    return distance_sorted_index

#Function that returns the nearest destination
def get_closest(destination_distances):
    closest = {'order': 0, 'distance': 10000}
    for destination in destination_distances:
        closest = destination if destination['distance'] <= closest['distance'] else closest
    closest = destination if math.isnan(destination['distance']) else closest
    return closest


def main():
    timings = ['9am-12nn', '12nn-3pm', '3pm-6pm', '6pm-8pm', 'Anytime (9am-6pm)']
    timeIndex = dict(zip(timings,range(len(timings))))

    columns, data = simulate_extract_orders() if settings.simulate else extract_orders()
    df = pd.DataFrame(data, columns=columns)
    df = cleanup_data_frame(df, timings, timeIndex)
    route_map = list()
    for timing in timings:
        cur_df = df.loc[df['delivery_time'] == timing]
        if not cur_df.empty:
            origin = {'lat': 1.2847359, 'lng': 103.8302216} #Tiong Bahru Wet Market
            destination = list()
            coordinates = list(zip(cur_df['latitude'], cur_df['longitude'], cur_df['order_number']))

            for coordinate in coordinates:
                destination.append({'lat': coordinate[0], 'lng': coordinate[1], 'order': coordinate[2]})

            result = generate_fulfillment_map(cur_df, origin, destination)
            if result:
                route_map = route_map + result

    new_df = pd.DataFrame(route_map, columns=columns)
    sendemail(new_df)

main()
