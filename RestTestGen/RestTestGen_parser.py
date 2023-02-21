import json

path = r"C:\Users\adity\Documents\GitHub\IBM-API-Testing\RestTestGen\statuscodecoverage.json"
api_data = {}

with open(path) as f:
    data = json.load(f)


# Iterate over the documented, documentedTested, and notDocumentedTested sections
for section in ['documented', 'documentedTested', 'notDocumentedTested']:
    # Iterate over the API endpoints and their response codes
    for endpoint, status_codes in data[section].items():
        # Iterate over the response codes
        for status_code in status_codes:
            # Add the API endpoint and status code to the dictionary
            if endpoint not in api_data.keys():
                api_data[endpoint] = []
            if status_code not in api_data[endpoint]:
                api_data[endpoint].append(status_code)

# Iterate over the notTested section
for endpoint, status_codes in data['notTested'].items():
    # Iterate over the response codes
    for status_code in status_codes:
        if endpoint not in api_data.keys():
            api_data[endpoint] = []
        if status_code not in api_data[endpoint]:
            api_data[endpoint].append(status_code)

print(api_data)

api_data_2xx = {}
api_data_3xx = {}
api_data_4xx = {}
api_data_5xx = {}

# Iterate over the API endpoints and their response codes and add those APIs and their endpoints whose endpoints are like 2xx
for endpoint, status_codes in api_data.items():
    for status_code in status_codes:
        if status_code.startswith('2'):
            if endpoint not in api_data_2xx.keys():
                api_data_2xx[endpoint] = []
            if status_code not in api_data_2xx[endpoint]:
                api_data_2xx[endpoint].append(status_code)
                
        elif status_code.startswith('3'):
            if endpoint not in api_data_3xx.keys():
                api_data_3xx[endpoint] = []
            if status_code not in api_data_3xx[endpoint]:
                api_data_3xx[endpoint].append(status_code)

        elif status_code.startswith('4'):
            if endpoint not in api_data_4xx.keys():
                api_data_4xx[endpoint] = []
            if status_code not in api_data_4xx[endpoint]:
                api_data_4xx[endpoint].append(status_code)

        elif status_code.startswith('5'):
            if endpoint not in api_data_5xx.keys():
                api_data_5xx[endpoint] = []
            if status_code not in api_data_5xx[endpoint]:
                api_data_5xx[endpoint].append(status_code)


# Print the dictionary of API endpoints and status codes
print()
print('2xx: ', api_data_2xx)
print('3xx: ', api_data_3xx)
print('4xx: ', api_data_4xx)
print('5xx: ', api_data_5xx)

print()
# print the number of APIs with 2xx, 3xx, 4xx, and 5xx response codes
print('Number of APIs endpoints with 2xx response codes: ', len(api_data_2xx))
print('Number of APIs endpoints with 3xx response codes: ', len(api_data_3xx))
print('Number of APIs endpoints with 4xx response codes: ', len(api_data_4xx))
print('Number of APIs endpoints with 5xx response codes: ', len(api_data_5xx))

all_2xx, all_3xx, all_4xx, all_5xx = 0, 0, 0, 0


for key, value in api_data_2xx.items():
    all_2xx += len(value)

for key, value in api_data_3xx.items():
    all_3xx += len(value)

for key, value in api_data_4xx.items():
    all_4xx += len(value)

for key, value in api_data_5xx.items():
    all_5xx += len(value)


print()
print('Including 2xx duplicates also: ', all_2xx)
print('Including 3xx duplicates also: ', all_3xx)
print('Including 4xx duplicates also: ', all_4xx)
print('Including 5xx duplicates also: ', all_5xx)