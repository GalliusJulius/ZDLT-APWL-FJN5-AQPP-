import json
import datetime

with open('data/input.json') as input:
    data = json.load(input)
    output = {}
    output['rentals'] = []
    for i  in data['rentals']:
        # I assume that the car id correspond to the [id-1] cars in my json
        timeRental = ((datetime.datetime.strptime(i["end_date"], '%Y-%m-%d')-(datetime.datetime.strptime(i["start_date"], '%Y-%m-%d'))).days+1)
        price = data['cars'][i["car_id"]-1]["price_per_day"] * timeRental + data['cars'][i["car_id"]-1]["price_per_km"]*i['distance']
        output["rentals"].append({
            'id':i['id'],
            'price':price
        })
    with open('data/output.json','w') as outputFile:
        json.dump(output,outputFile)
