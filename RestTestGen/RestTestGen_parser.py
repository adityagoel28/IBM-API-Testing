import json

path = r"C:\Users\adity\Documents\GitHub\IBM-API-Testing\RestTestGen\statuscodecoverage.json"
api_data = {}

with open(path) as f:
    data = json.load(f)

all_endpoints = [{'GET': '/v2/pet/findByStatus'}, {'GET': '/v2/pet/findByTags'}, {'POST': '/v2/store/order'}, {'GET': '/v2/store/inventory'}, {'GET': '/v2/store/order/'},
                  {'DELETE': '/v2/store/order/'}, {'POST': '/v2/user/createWithArray'}, {'POST': '/v2/user/createWithList'}, {'GET': '/v2/user/login'}, {'GET': '/v2/user/logout'}, {'POST': '/v2/pet'},
                  {'PUT': '/v2/pet'}, {'DELETE': '/v2/pet/'}, {'GET': '/v2/pet/'}, {'GET': '/v2/user/'}, {'PUT': '/v2/user/'}, {'DELETE': '/v2/user/'}, {'POST': '/v2/user'}, {'POST': '/v2/pet/'}]

# all_endpoints = [{'GET': '/api/v1/Activities'}, {'POST': '/api/v1/Activities'}, {'POST': '/api/v1/Users'}, {'PUT': '/api/v1/Activities/'}, {'DELETE': '/api/v1/Activities/'},
#                   {'GET': '/api/v1/Authors'}, {'POST': '/api/v1/Authors'}, {'GET': '/api/v1/Authors/authors/books/'}, {'GET': '/api/v1/Users'}, {'PUT': '/api/v1/Authors/'}, 
#                   {'DELETE': '/api/v1/Authors/'}, {'PUT': '/api/v1/Users'}, {'DELETE': '/api/v1/Users'},
#                   {'GET': '/api/v1/Books'}, {'POST': '/api/v1/Books'}, {'GET': '/api/v1/Books/'}, {'PUT': '/api/v1/Books/'}, {'DELETE': '/api/v1/Books/'},
#                   {'GET': '/api/v1/CoverPhotos'}, {'POST': '/api/v1/CoverPhotos'}, {'PUT': '/api/v1/CoverPhotos'}, {'DELETE': '/api/v1/CoverPhotos'}, 
#                   {'GET': '/api/v1/CoverPhotos/books/covers/'}]

all_endpoints = [{'GET': '/api/Book/GetCategoriesList'}, {'DELETE': '/api/Book/GetSimilarBooks/'}, {'POST': '/api/CheckOut/'}, {'POST': '/api/Login'}, {'GET': '/api/Order/'}, 
                 {'GET': '/api/ShoppingCart/SetShoppingCart/'}, {'POST': '/api/ShoppingCart/AddToCart'}, {'GET': '/api/ShoppingCart'}, {'DELETE': '/api/ShoppingCart'},  
                 {'PUT': '/api/ShoppingCart'}, {'DELETE': '/api/ShoppingCart'}, {'GET': '/api/Book'}, {'POST': '/api/Book'}, {'PUT': '/api/Book'},  {'DELETE': '/api/Book'}, 
                 {'GET': '/api/User/validateUserName'}, {'POST': '/api/User'}, {'GET': '/api/User'}, {'POST': '/api/Wishlist/ToggleWishlist'}, {'GET': '/api/Wishlist'}, {'DELETE': '/api/Wishlist'}]

all_endpoints = [{'POST': '/api/auth/login'}, {'GET': '/api/bodies'}, {'GET': '/api/engines'}, {'GET': '/api/exterior-colors'}, {'GET': '/api/interior-colors'}, 
                 {'GET': '/api/makes'}, {'GET': '/api/mileages'}, {'GET': '/api/models'}, {'GET': '/api/trims'}, {'GET': '/api/trims/{id}'}, {'GET': '/api/vehicle-attributes'}, 
                 {'GET': '/api/vin/{vin}'}, {'GET': '/api/years'}]

all_endpoints = [{'POST': '/check'}, {'GET': '/languages'}, {'GET': '/words'}, {'POST': '/words/add'}, {'POST': '/words/delete'}]

all_endpoints = [{'GET': '/info.0.json'}, {'GET': '/{comicId}/info.0.json'}]

# Iterate over the documented, documentedTested, and notDocumentedTested sections
for section in ['documented', 'documentedTested', 'notDocumentedTested', 'notTested']:
    # Iterate over the API endpoints and their response codes
    for endpoint, status_codes in data[section].items():
        # Iterate over the response codes
        # breaking the endpoint into method and path on the basis of space
        method, path = endpoint.split(' ')
        for status_code in status_codes:
            # Add the API endpoint and status code to the dictionary
            if endpoint not in api_data.keys():
                api_data[endpoint] = [status_code]
            if status_code not in api_data[endpoint]:
                api_data[endpoint].append(status_code)

# print(api_data)

total_analysis, unique_analysis = [], []

for key, value in api_data.items():
    method, path = key.split(' ')
    for i in range(len(value)):
        total_analysis.append({'method': method, 'endpoint': path, 'statusCode': value[i]})
        if({'method': method, 'endpoint': path, 'statusCode': value[i]} not in unique_analysis):
            unique_analysis.append({'method': method, 'endpoint': path, 'statusCode': value[i]})

print(total_analysis)
print('Length of unique analysis is: ' + str(len(unique_analysis)))
print('Length of total analysis is: ' + str(len(total_analysis)))

success_unique_analysis = []
success_unique_analysis_count = 0

for i in unique_analysis:
    method = i['method']
    endpoint = i['endpoint']
    statusCode = i['statusCode']
    if(statusCode[0] == '2' or statusCode[0] == '5'):
        for j in success_unique_analysis:
            j_method = j['method']
            j_endpoint = j['endpoint']
            j_statusCode = j['statusCode']
            if(method == j_method and endpoint == j_endpoint):
                break
        else:
            success_unique_analysis_count += 1
            success_unique_analysis.append({'method': method, 'endpoint': endpoint, 'statusCode': statusCode})


unique_responses_2xx, unique_responses_3xx, unique_responses_4xx, unique_responses_5xx = 0, 0, 0, 0
total_responses_2xx, total_responses_3xx, total_responses_4xx, total_responses_5xx = 0, 0, 0, 0

for i in unique_analysis:
    # check whether analysis['statusCode'] starts with 2 or 3 or 4 or 5
    if(i['statusCode'][0] == '2'):
        unique_responses_2xx += 1
    elif(i['statusCode'][0] == '3'):
        unique_responses_3xx += 1
    elif(i['statusCode'][0] == '4'):
        unique_responses_4xx += 1
    elif(i['statusCode'][0] == '5'):
        unique_responses_5xx += 1

for i in total_analysis:
    # check whether analysis['statusCode'] starts with 2 or 3 or 4 or 5
    if(i['statusCode'][0] == '2'):
        total_responses_2xx += 1
    elif(i['statusCode'][0] == '3'):
        total_responses_3xx += 1
    elif(i['statusCode'][0] == '4'):
        total_responses_4xx += 1
    elif(i['statusCode'][0] == '5'):
        total_responses_5xx += 1

total_responses = total_responses_2xx + total_responses_3xx + total_responses_4xx + total_responses_5xx

print('Number of unique 2xx responses: ' + str(unique_responses_2xx))
print('Number of unique 3xx responses: ' + str(unique_responses_3xx))
print('Number of unique 4xx responses: ' + str(unique_responses_4xx))
print('Number of unique 5xx responses: ' + str(unique_responses_5xx))
print()
print('Number of total 2xx responses: ' + str(total_responses_2xx))
print('Number of total 3xx responses: ' + str(total_responses_3xx))
print('Number of total 4xx responses: ' + str(total_responses_4xx))
print('Number of total 5xx responses: ' + str(total_responses_5xx))
print()
print('Operation Coverage (Op_cov) numerator: ' + str(success_unique_analysis_count))
print('Operation Coverage (Op_cov) denominator: ' + str(len(all_endpoints)))
print('Operation Coverage (Op_cov): ' + str((success_unique_analysis_count/len(all_endpoints))))
print()
print('5xx_operation_coverage (5xx_op_cov) numerator: ' + str(total_responses_5xx))
print('5xx_operation_coverage (5xx_op_cov) denominator: ' + str(total_responses))
print('5xx_operation_coverage (5xx_op_cov): ' + str(total_responses_5xx/total_responses))