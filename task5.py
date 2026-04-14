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
    
    def sortDesc(data: json, param: str) -> json:
        lst = json.loads(data)
        lst.sort(key=lambda x: x.get(param, 0), reverse=True)
        return json.dumps(lst)

    def paginate(data: json, page: int, size: int = 2) -> json:
        lst = json.loads(data)
        start = (page - 1) * size
        end = start + size
        return json.dumps(lst[start:end])

# --- end of class ---


class Controller:

    def minAverage(dummy: any, num: float) -> json:
        temp = Service.getNreplace_average(Service.get_users())
        return Service.delByAverage(temp, num)
    
    



# --- end of class ---

# main class
def GET(path: str):
        studentPath = "/students/top?"
        validOperations = { 
            "minAverage": {"func": Controller.minAverage, "type": float, "priority": 1}, 
            "sortDesc": {"func": Service.sortDesc, "type": str, "priority": 0}, 
            "pageLimit": {"func": Service.paginate, "type": int, "priority": -1}, 
            "page": {"func": Service.paginate, "type": int, "priority": -2}
        }
        
        if not path.startswith(studentPath):
            print("HTTP 400: Path not found")
            return None
            
        try:
            _, path = path.split("?", 1)
            
            # Если параметров вообще нет
            if  path == "":
                return Service.get_users()

            # params = path.split("&")
            params = dict(p.split("=") for p in path.split("&") if "=" in p)
            sorted_params = sorted(
                params.items(), 
                key=lambda item: validOperations.get(item[0], {}).get("priority", -100), 
                reverse=True
            )

            current_json = json.dumps({"test": "test"})

            for key, value in sorted_params:
                if key in validOperations:
                    config = validOperations[key]
                    
                    try:
                        clean_value = config["type"](value)
                    except ValueError:
                        print(f"Ошибка: параметр {key}")
                        continue
                    
                    current_json = config["func"](current_json, clean_value)
            
            return current_json
            
        except Exception as e:
            print("HTTP 400: Ошибка при обработке запроса:", e)
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
print(GET("/students/top?minAverage=60&sortDesc=average"))
print(GET("/students/top?minAverage=60&sortDesc=average&page=1"))
print("--- end of hardcoded tests ---")

request = input("Print GET request (with full URL)\n Type 'q' to exit\n")
while request != 'q':
    print(GET(request))
    request = input("Print GET request (with full URL)\n Type 'q' to exit\n")
