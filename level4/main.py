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
    # Add the distancea
    price += data["cars"][current["car_id"] - 1]["price_per_km"] * current["distance"]
    return price

with open('data/input.json') as input:
    data = json.load(input)
    output = {}
    output['rentals'] = []
    for i  in data['rentals']:
        #Creation new rentals
        actors = [["driver", "debit"], ["owner", "credit"], ["insurance", "credit"], ["assistance", "credit"],["drivy", "credit"]]
        # I assume that the car id correspond to the [id-1] cars in my json
        timeRental = ((datetime.datetime.strptime(i["end_date"], '%Y-%m-%d') - (datetime.datetime.strptime(i["start_date"], '%Y-%m-%d'))).days + 1)
        price = getPrice(data,i,timeRental)
        #update table with prices
        actors[0].append(round(price))
        commission = price*0.3
        actors[1].append(round(price-commission))
        actors[2].append(round(commission/2))
        actors[3].append(round(100*timeRental))
        actors[4].append(round((commission/2)-100*timeRental))
        output["rentals"].append({
            "id": i["id"],
            "actions":[]
        })
        print(actors[0])
        for k in actors:
            output["rentals"][i["id"]-1]["actions"].append({
                "who":k[0],
                "type": k[1],
                "amount":k[2]
            })
    with open('data/output.json','w') as outputFile:
        json.dump(output,outputFile)
