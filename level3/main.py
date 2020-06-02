import json
import datetime

def getPrice(data,current,timeRental):
    # Calcule the prize per days with the discount
    perDay = data['cars'][current["car_id"] - 1]["price_per_day"]
    price = perDay
    if (timeRental > 10):
        price += (perDay * 0.5) * (timeRental - 10)
        timeRental = 10
    if (timeRental > 4):
        price += (perDay * 0.7) * (timeRental - 4)
        timeRental = 4
    if (timeRental > 1):
        price += (perDay * 0.9) * (timeRental - 1)
    # Add the distance
    price += data['cars'][current["car_id"] - 1]["price_per_km"] * current['distance']
    return price

with open('data/input.json') as input:
    data = json.load(input)
    output = {}
    output['rentals'] = []
    for i  in data['rentals']:
        # I assume that the car id correspond to the [id-1] cars in my json
        timeRental = ((datetime.datetime.strptime(i["end_date"], '%Y-%m-%d') - (datetime.datetime.strptime(i["start_date"], '%Y-%m-%d'))).days + 1)
        price = getPrice(data,i,timeRental)
        commission = price*0.3
        output["rentals"].append({
            'id':i['id'],
            'price':round(price),
            'commission':{
                'insurance_fee': round(commission/2),
                'assistance_fee':round(100*timeRental),
                'drivy_fee':round((commission/2)-100*timeRental)
            }
        })

    with open('data/output.json','w') as outputFile:
        json.dump(output,outputFile)
