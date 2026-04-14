import json

data = [ { "name": "Alice", "scores": [80, 90, 100] }, { "name": "Bob", "scores": [60, 70, 75] }]

def getNreplace_average(data: json) -> json:
    data = json.loads(data)
    for i in data:
        _average = 0
        _sum = 0
        arr = i.get("scores")
        for j in arr:
            _sum += j
            
        _average = _sum / len(arr)
        
        i.pop("scores", None)
        i["average"] = _average
        
    return json.dumps(data)


def delByAverage(data: json, num: float) -> json:
    data = json.loads(data)
    temp = []
    
    for i in data:
        if i["average"] > num:
            temp.append(i)
    
    return json.dumps(temp)
    

jsonD = json.dumps(data)
print(type(jsonD))

users_avg = getNreplace_average(jsonD)
print(users_avg)
print(type(users_avg))

filteredData = delByAverage(users_avg, 75.0)
print(filteredData)

# print(jsonD)