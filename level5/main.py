import json
import datetime

#Get the price for a rental (current), base on input (data) and with the time in days of the rental (timeRental)
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
    price += data["cars"][current["car_id"] - 1]["price_per_km"] * current["distance"]
    return price

#Get the dime in days between 2 dates
def getTime(dateStart,dateEnd):
    return ((datetime.datetime.strptime(dateEnd, '%Y-%m-%d') - (datetime.datetime.strptime(dateStart, '%Y-%m-%d'))).days + 1)

#Update ammount et set options on the json output
def setOptions(data,output):
    #Dictionnaire => type (price,number in action)
    dicoOptions={"gps":[500,1],"baby_seat":[200,1],"additional_insurance":[1000,4]}
    #I assume rental_id in options (input) correspon to rentals[retals_id-1] (output)
    for k in data["options"]:
        output["rentals"][k["rental_id"] - 1]["options"].append(k["type"])
        numberDays = getTime(data["rentals"][k["rental_id"]-1]["start_date"],data["rentals"][k["rental_id"]-1]["end_date"])
        actionCurrent =  output["rentals"][k["rental_id"] - 1]["actions"]
        #updatePrice driver
        actionCurrent[0]["amount"] = dicoOptions[k["type"]][0]*numberDays+actionCurrent[0]["amount"]
        actionCurrent[dicoOptions[k["type"]][1]]["amount"] = dicoOptions[k["type"]][0]*numberDays+actionCurrent[dicoOptions[k["type"]][1]]["amount"]

#Main programm
with open('data/input.json') as input:
    data = json.load(input)
    output = {}
    output['rentals'] = []
    for i  in data['rentals']:
        #Table with elements of actions
        actors = [["driver", "debit"], ["owner", "credit"], ["insurance", "credit"], ["assistance", "credit"],["drivy", "credit"]]
        # I assume that the car id correspond to the [id-1] cars in my json
        timeRental = getTime(i["start_date"],i["end_date"])
        #prices
        price = getPrice(data,i,timeRental)
        commission = price * 0.3
        #update table with prices for each actors => driver(0)/owner(1)/insurrance(2)/assistance(3)/drivy(4)
        actors[0].append(round(price))
        actors[1].append(round(price-commission))
        actors[2].append(round(commission/2))
        actors[3].append(round(100*timeRental))
        actors[4].append(round((commission/2)-100*timeRental))
        #insertions of empty options and empty actions
        output["rentals"].append({
            "id": i["id"],
            "options": [],
            "actions":[]
        })
        #insertion for each actors based on the table actors
        for k in actors:
            output["rentals"][i["id"]-1]["actions"].append({
                "who":k[0],
                "type": k[1],
                "amount":k[2]
            })
    #set options
    setOptions(data,output)
    #writting output
    with open('data/output.json','w') as outputFile:
        json.dump(output,outputFile)
