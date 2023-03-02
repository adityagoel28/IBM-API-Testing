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

analysis = []

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
                # check if the method, endpoint and status code are already present in the analysis list
                if({'method': method, 'endpoint': endpointt, 'statusCode': statusCode} not in analysis):
                    # print(2)
                    analysis.append({'method': method, 'endpoint': endpointt, 'statusCode': statusCode})
                break
        if k == 1:
            break
    # print(1111111111111111111111111)

print(analysis)
print('Length of analysis is: ' + str(len(analysis)))

with open("./scraped.txt", "w") as output:
    output.write(str(final_result))

