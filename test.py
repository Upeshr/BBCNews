dictionary = {"berlin": "germany",
               "tokyo": "japan",
                 "rome": "italy"}
value = dictionary.keys()
print(value)
for key, value in dictionary.items():
    print(f"{key:10}{value}")