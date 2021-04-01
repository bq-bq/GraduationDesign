import os, json

with open('答案.json') as fp:
    data = json.load(fp)

u = {}
for row in data['rows']:
    user = row[1]
    if user not in u:
        u[user] = {'field_names':data['field_names'],
                    'field_types':data['field_types'],
                    "table_name": "答案",
                    "table_name": "答案",
                    "foreign_keys":{},
                    "primary_keys":[],
                    "rows":[]}
    u[user]['rows'].append(row)

for user, d in u.items():
    with open(os.path.join('clients', user, '答案.json'), 'w') as fp:
        json.dump(d, fp, indent=4, sort_keys=True, ensure_ascii=False)
