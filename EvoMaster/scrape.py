import re

count = 0
final_result = []
received = 0
result = {}

# all_endpoints = [{'post': '/pet/{petId}/uploadImage'}, {'get': '/pet/findByStatus'}, {'put': '/pet'}, {'delete': '/pet/{petId}'}, {'get': '/pet/findByTags'}, 
#                   {'get': '/pet/{petId}'}, {'post': '/pet'}, {'post': '/store/order'}, {'get': '/store/inventory'}, {'get': '/store/order/{orderId}'},
#                   {'delete': '/store/order/{orderId}'}, {'post': '/user/createWithArray'}, {'post': '/user/createWithList'}, {'get': '/user/login'}, {'get': '/user/logout'}, 
#                   {'get': '/user/{username}'}, {'put': '/user/{username}'}, {'delete': '/user/{username}'}, {'post': '/user'}, {'post': '/pet/{petId}'}]

all_endpoints = [{'get': '/v2/pet/findByStatus'}, {'get': '/v2/pet/findByTags'}, {'post': '/v2/store/order'}, {'get': '/v2/store/inventory'}, {'get': '/v2/store/order/'},
                  {'delete': '/v2/store/order/'}, {'post': '/v2/user/createWithArray'}, {'post': '/v2/user/createWithList'}, {'get': '/v2/user/login'}, {'get': '/v2/user/logout'}, {'post': '/v2/pet'},
                  {'put': '/v2/pet'}, {'delete': '/v2/pet/'}, {'get': '/v2/pet/'}, {'get': '/v2/user/'}, {'put': '/v2/user/'}, {'delete': '/v2/user/'}, {'post': '/v2/user'}, {'post': '/v2/pet/'}]

print('Number of endpoints: ', len(all_endpoints))

# open the text file and read its contents into a string
with open('./evo.java','r', encoding="utf8") as file:
    text = file.read()

# use a regular expression to find all lines containing the pattern
pattern1 = re.compile(r"\.(get|post|put|patch|delete)\((\S+ \S+ \S+)")
pattern2 = re.compile(r"\.statusCode\((\d+)\)")

# loop through the lines in the text and print out any that match the pattern
for line in text.split('\n'):
    match1 = pattern1.search(line)
    match2 = pattern2.search(line)
    # print(line)
    if match1:
        result['method'] = match1.group(1)
        result['endpoint'] = match1.group(2)[16:][:-2]
        count += 1
    elif match2:
        received = 1
        result['statusCode'] = match2.group(1)
        count += 1
        final_result.append(result)
    if received == 1:
        received = 0
        result = {}

print(final_result)
print(len(final_result))

total_analysis, unique_analysis = [], []

for my_dict in final_result:
    k = 0
    method = my_dict['method']
    endpoint = my_dict['endpoint']
    statusCode = my_dict['statusCode']
    # print(method, endpoint, statusCode)
    # print()
    for j in all_endpoints:
        for key, val in j.items():
            # print(key, method)
            # print(val, endpoint)
            # print()
            endpointt = ''
            for i in endpoint:
                endpointt += i
                if(endpointt == val):
                    # print(3)
                    break
                
            if(key == method and val == endpointt):
                k = 1
                total_analysis.append({'method': method, 'endpoint': endpointt, 'statusCode': statusCode})
                # check if the method, endpoint and status code are already present in the analysis list
                if({'method': method, 'endpoint': endpointt, 'statusCode': statusCode} not in unique_analysis):
                    # print(2)
                    unique_analysis.append({'method': method, 'endpoint': endpointt, 'statusCode': statusCode})
                break
        if k == 1:
            break
    # print(1111111111111111111111111)

print(unique_analysis)
print('Length of analysis is: ' + str(len(unique_analysis)))
print('Length of total analysis is: ' + str(len(total_analysis)))

with open("./file1.txt", "w") as output:
    output.write(str(final_result))

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
    
print('Number of unique 2xx responses: ' + str(unique_responses_2xx))
print('Number of unique 3xx responses: ' + str(unique_responses_3xx))
print('Number of unique 4xx responses: ' + str(unique_responses_4xx))
print('Number of unique 5xx responses: ' + str(unique_responses_5xx))
print()
print('Number of total 2xx responses: ' + str(total_responses_2xx))
print('Number of total 3xx responses: ' + str(total_responses_3xx))
print('Number of total 4xx responses: ' + str(total_responses_4xx))
print('Number of total 5xx responses: ' + str(total_responses_5xx))