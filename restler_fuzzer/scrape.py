import re
import json

count = 0
final_result = []
received = 0
result = {}

# all_endpoints = [{'post': '/pet/{petId}/uploadImage'}, {'get': '/pet/findByStatus'}, {'put': '/pet'}, {'delete': '/pet/{petId}'}, {'get': '/pet/findByTags'}, 
#                   {'get': '/pet/{petId}'}, {'post': '/pet'}, {'post': '/store/order'}, {'get': '/store/inventory'}, {'get': '/store/order/{orderId}'},
#                   {'delete': '/store/order/{orderId}'}, {'post': '/user/createWithArray'}, {'post': '/user/createWithList'}, {'get': '/user/login'}, {'get': '/user/logout'}, 
#                   {'get': '/user/{username}'}, {'put': '/user/{username}'}, {'delete': '/user/{username}'}, {'post': '/user'}, {'post': '/pet/{petId}'}]

all_endpoints = [{'GET': '/v2/pet/findByStatus'}, {'GET': '/v2/pet/findByTags'}, {'POST': '/v2/store/order'}, {'GET': '/v2/store/inventory'}, {'GET': '/v2/store/order/'},
                  {'DELETE': '/v2/store/order/'}, {'POST': '/v2/user/createWithArray'}, {'POST': '/v2/user/createWithList'}, {'GET': '/v2/user/login'}, {'GET': '/v2/user/logout'}, {'POST': '/v2/pet'},
                  {'PUT': '/v2/pet'}, {'DELETE': '/v2/pet/'}, {'GET': '/v2/pet/'}, {'GET': '/v2/user/'}, {'PUT': '/v2/user/'}, {'DELETE': '/v2/user/'}, {'POST': '/v2/user'}, {'POST': '/v2/pet/'}]

all_endpoints = [{'GET': '/api/v1/Activities'}, {'POST': '/api/v1/Activities'}, {'POST': '/api/v1/Users'}, {'PUT': '/api/v1/Activities/'}, {'DELETE': '/api/v1/Activities/'},
                  {'GET': '/api/v1/Authors'}, {'POST': '/api/v1/Authors'}, {'GET': '/api/v1/Authors/authors/books/'}, {'GET': '/api/v1/Users'}, {'PUT': '/api/v1/Authors/'}, 
                  {'DELETE': '/api/v1/Authors/'}, {'PUT': '/api/v1/Users'}, {'DELETE': '/api/v1/Users'},
                  {'GET': '/api/v1/Books'}, {'POST': '/api/v1/Books'}, {'GET': '/api/v1/Books/'}, {'PUT': '/api/v1/Books/'}, {'DELETE': '/api/v1/Books/'},
                  {'GET': '/api/v1/CoverPhotos'}, {'POST': '/api/v1/CoverPhotos'}, {'PUT': '/api/v1/CoverPhotos'}, {'DELETE': '/api/v1/CoverPhotos'}, 
                  {'GET': '/api/v1/CoverPhotos/books/covers/'}]

all_endpoints = [{'GET': '/api/Book/GetCategoriesList'}, {'DELETE': '/api/Book/GetSimilarBooks/'}, {'POST': '/api/CheckOut/'}, {'POST': '/api/Login'}, {'GET': '/api/Order/'}, 
                 {'GET': '/api/ShoppingCart/SetShoppingCart/'}, {'POST': '/api/ShoppingCart/AddToCart'}, {'GET': '/api/ShoppingCart'}, {'DELETE': '/api/ShoppingCart'},  
                 {'PUT': '/api/ShoppingCart'}, {'DELETE': '/api/ShoppingCart'}, {'GET': '/api/Book'}, {'POST': '/api/Book'}, {'PUT': '/api/Book'},  {'DELETE': '/api/Book'}, 
                 {'GET': '/api/User/validateUserName'}, {'POST': '/api/User'}, {'GET': '/api/User'}, {'POST': '/api/Wishlist/ToggleWishlist'}, {'GET': '/api/Wishlist'}, {'DELETE': '/api/Wishlist'}]

all_endpoints = [{'GET': '/info.0.json'}, {'GET': '/{comicId}/info.0.json'}]

all_endpoints = [{'POST': '/check'}, {'GET': '/languages'}, {'GET': '/words'}, {'POST': '/words/add'}, {'POST': '/words/delete'}]

all_endpoints = [{'GET': '/v2/pet/findByStatus'}, {'GET': '/v2/pet/findByTags'}, {'POST': '/v2/store/order'}, {'GET': '/v2/store/inventory'}, {'GET': '/v2/store/order/'},
                  {'DELETE': '/v2/store/order/'}, {'POST': '/v2/user/createWithArray'}, {'POST': '/v2/user/createWithList'}, {'GET': '/v2/user/login'}, {'GET': '/v2/user/logout'}, {'POST': '/v2/pet'},
                  {'PUT': '/v2/pet'}, {'DELETE': '/v2/pet/'}, {'GET': '/v2/pet/'}, {'GET': '/v2/user/'}, {'PUT': '/v2/user/'}, {'DELETE': '/v2/user/'}, {'POST': '/v2/user'}, {'POST': '/v2/pet/'}]

print('Number of endpoints: ', len(all_endpoints))

with open('./demo-server-test/swagger.json', 'r') as file:
    data = json.load(file)

endpoints = list(data['paths'].keys())
all_operations = []

for i in range(len(endpoints)):
    methods = list(data['paths'][endpoints[i]])
    print(methods, endpoints[i])
    for j in range(len(methods)):
        methods[j] = methods[j].upper()
        all_operations.append({methods[j]: endpoints[i]})

print('All operations: ', all_operations)

# open the text file and read its contents into a string
with open('./output.txt','r', encoding="utf8") as file:
    text = file.read()

# use a regular expression to find all lines containing the pattern "Received: 'HTTP/1.1 500"
pattern1 = re.compile(r"Received: 'HTTP/1\.1 500")
# use above and count the number of lines that match the pattern
pattern2 = re.compile(r'"code":(\d+),"type":"\w+","message":"([^"]+)"')
# pattern3 = re.compile(r"Sending: (\'|\")(\S+ \S+)")
pattern3 = re.compile(r"Sending: ([\'\"])(\S+ \S+)")
pattern4 = re.compile(r"Received: '(\S+ \S+)")
pattern5 = re.compile(r"Received: None")

# loop through the lines in the text and print out any that match the pattern
for line in text.split('\n'):
    match3 = pattern3.search(line)
    match4 = pattern4.search(line)
    match5 = pattern5.search(line)
    if match3:
        result['endpoint'] = match3.group(2)
        count += 1
    elif match4:
        received = 1
        result['statusCode'] = match4.group(1)[9:]
        final_result.append(result)
        count += 1
    elif match5:
        received = 1
        result['statusCode'] = 'None'
        # final_result.append(result)
        count += 1
        
    if received == 1:
        received = 0
        result = {}

print(count)
print(final_result)
print(len(final_result))
print()

total_analysis, unique_analysis = [], []

for my_dict in final_result:
    k = 0
    splitted = my_dict['endpoint'].split()
    method = splitted[0]
    endpoint = splitted[1]
    statusCode = my_dict['statusCode']
    for j in all_endpoints:
        for key, val in j.items():
            endpointt = ''
            for i in endpoint:
                endpointt += i
                if(endpointt == val):
                    break
                
            if(key == method and val == endpointt):
                k = 1
                total_analysis.append({'method': method, 'endpoint': endpointt, 'statusCode': statusCode})
                # check if the method, endpoint and status code are already present in the unique_analysis list
                if({'method': method, 'endpoint': endpointt, 'statusCode': statusCode} not in unique_analysis):
                    unique_analysis.append({'method': method, 'endpoint': endpointt, 'statusCode': statusCode})
                break
        if k == 1:
            break

print(unique_analysis)
print('Length of unique analysis is: ' + str(len(unique_analysis)))
print('Length of total analysis is: ' + str(len(total_analysis)))


with open("./file.txt", "w") as output:
    output.write(str(final_result))

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