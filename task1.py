import json

data = [ { "name": "Alice", "scores": [80, 90, 100] }, { "name": "Bob", "scores": [60, 70, 75] }]


for i in data:
    _average = 0
    _sum = 0
    arr = i.get("scores")
    for j in arr:
        _sum += j
        
    _average = _sum / len(arr)
    
    i.pop("scores", None)
    i["average"] = _average
    print(_sum)


jsonD = json.dumps(data)
jsonD.data
print(jsonD)