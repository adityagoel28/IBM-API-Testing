import re

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
                  {'PUT': '/v2/pet'}, {'DELETE': '/v2/pet/'}, {'GET': '/v2/pet/'}, {'GET': '/v2/user/'}, {'put': '/v2/user/'}, {'DELETE': '/v2/user/'}, {'POST': '/v2/user'}, {'POST': '/v2/pet/'}]

print('Number of endpoints: ', len(all_endpoints))

# open the text file and read its contents into a string
with open('./restler_fuzzer/network.testing.txt','r', encoding="utf8") as file:
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

analysis = []

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
                # check if the method, endpoint and status code are already present in the analysis list
                if({'method': method, 'endpoint': endpointt, 'statusCode': statusCode} not in analysis):
                    analysis.append({'method': method, 'endpoint': endpointt, 'statusCode': statusCode})
                break
        if k == 1:
            break

print(analysis)
print('Length of analysis is: ' + str(len(analysis)))

with open("./restler_fuzzer/scraped.txt", "w") as output:
    output.write(str(final_result))