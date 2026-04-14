import json



class Service:
    def get_users() -> json:
        try:
            with open('data.json', 'r') as file:
                data = json.load(file)
                return json.dumps(data)
        except FileNotFoundError:
            print("The file was not found.")
        except json.JSONDecodeError:
            print("Failed to decode JSON")
    
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
    
# --- end of class ---


class Controller:

    def minAverage(num: float) -> json:
        temp = Service.getNreplace_average(Service.get_users())
        return Service.delByAverage(temp, num)
    
    



# --- end of class ---

# main class
def GET(path: str):
        studentPath = "/students/top?"
        validOperations = { 
            "minAverage": {"func": Controller.minAverage, "type": float} 
        }
        
        if not path.startswith(studentPath):
            print("HTTP 400: Path not found")
            return None
            
        try:
            _, path = path.split("?", 1)
            
            # Если параметров вообще нет
            if  path == "":
                return Service.get_users()

            params = path.split("&")

            for param in params:
                if "=" not in param:
                    print("key have no value")
                    continue
                
                key, value = param.split("=", 1)
                
                if key in validOperations:
                    config = validOperations[key]
                    
                    try:
                        clean_value = config["type"](value)
                    except ValueError:
                        print(f"Ошибка: параметр {key} должен быть числом")
                        continue
                    
                    current_json = config["func"](clean_value)
            
            return current_json
            
        except Exception as e:
            print("Ошибка при обработке запроса:", e)
            return None


print(Service.get_users())

jsonD = Service.get_users()
# print(type(jsonD))

users_avg = Service.getNreplace_average(jsonD)
print(users_avg)
# print(type(users_avg))

# filteredData = delByAverage(users_avg, 75.0)
# print(filteredData)

print(GET("/students/top?minAverage=80"))