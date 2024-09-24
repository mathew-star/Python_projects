def _load_data():
        try:
            with open('passwords.json', 'r') as f:
                data = f.read()
                print("###", data)
                print(f"-,{data}-")
                print(type(data))
                print(len(data))
                if len(data)!=0:
                    print("**",data)  
                    return data
                else:
                    return {}
        except FileNotFoundError:
            return {}