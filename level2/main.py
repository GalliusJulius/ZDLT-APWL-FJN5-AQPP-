import json
import datetime

with open('data/input.json') as input:
    data = json.load(input)
    output = {}
    output['rentals'] = []
    for i  in data['rentals']:
        # I assume that the car id correspond to the [id-1] cars in my json
        timeRental = ((datetime.datetime.strptime(i["end_date"], '%Y-%m-%d')-(datetime.datetime.strptime(i["start_date"], '%Y-%m-%d'))).days+1)
        #Calcule the prize per days with the discount
        perDay = data['cars'][i["car_id"]-1]["price_per_day"]
        price = perDay
        if (timeRental > 10):
            price += (perDay * 0.5 ) * (timeRental-10)
            timeRental =10
        if (timeRental > 4):
             price += (perDay * 0.7) * (timeRental - 4)
             timeRental = 4
        if (timeRental > 1):
            price += (perDay * 0.9) * (timeRental - 1)
        #Add the distance
        price += data['cars'][i["car_id"]-1]["price_per_km"]*i['distance']
        output["rentals"].append({
            'id':i['id'],
            'price':price
        })
    with open('data/output.json','w') as outputFile:
        json.dump(output,outputFile)
