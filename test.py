# import pretty
lst = [
    ['王', '1'],
    ['李', '1'],
    ['李', '3'],
    ['王', '2'],
    ['王', '3'],
]
dataLst = {}
for i in lst:
    data = {}
    for x in dataLst:
        if not i[0] == x['name']:
    #         x['name'] = i[0]
            x['files'] = []
    #     x['files'].append(i[1])
    # print(data)
    # dataLst.append(data)

for i in dataLst:
    print(i)

