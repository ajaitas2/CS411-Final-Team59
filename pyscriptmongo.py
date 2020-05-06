from pymongo import MongoClient
client = MongoClient("localhost", 27017)

with open("graduated.csv") as f:
	entries = f.readlines()
	del entries[0]
	for entry in entries:
		values_raw = entry.strip().split(",")

		values = []

		for value in values_raw:
			if value == "n/a":
				values.append(None)
			elif "%" in value:
				values.append(float(value[:-1]))
			else:
				values.append(value)

		document = {
			"department": values[0],
			"ALL_percent": values[1],
			"AIAN": values[2],
			"Asian": values[3],
			"Black_AfricanAmerican": values[4],
			"Hispanic": values[5],
			"NHPI": values[6],
			"White": values[7],
			"Multirace": values[8],
			"NoRes": values[9],
			"Unknown": values[10],
			"Male": values[11],
			"Female": values[12]
		}		
		
		print(client.enrollment.gradrates.insert_one(document))