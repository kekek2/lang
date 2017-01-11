#!/usr/local/bin/python

def get_record(handle):
    rec1 = {'msgid': [], 'msgstr': [], 'comments': []}
    item = 'msgid'

    while True:
        line = handle.readline()
        if line == '':
            return {'eof': True, 'result': rec1}

        split = line.split()
        length = len(split)

        if length == 0:
            if len(rec1['msgid']) == 0:
                continue

            return {'eof': False, 'result': rec1}

        keyword = split[0]
        if keyword == 'msgid':
            rec1['msgid'].append(line.partition('msgid')[2].strip())
        elif keyword == 'msgstr':
            rec1['msgstr'].append(line.partition('msgstr')[2].strip())
            item = 'msgstr'
        elif line[0] == '#':
            rec1['comments'].append(line.strip())
        else:
            rec1[item].append(line.strip())


ting_array = []
# inp = os.popen('git show origin/lang:ru_RU.po')
inp = open('ru_RU.po')

while True:
    record = get_record(inp)
    ting_array.append(record['result'])
    if record['eof']:
        break
inp.close()

# inp = os.popen('git show github/master:ru_RU.po')
inp = open('ru_RU.po.old')
while True:
    record = get_record(inp)

    for rec in ting_array:
        if rec['msgid'] == record['result']['msgid']:
            ting_array.remove(rec)
            break

    if record['eof']:
        break
inp.close()

for record in ting_array:
    for comment in record['comments']:
        print comment
    if len(record['msgid']) == 0:
        continue
    print "msgid", record['msgid'][0]
    for msgid in record['msgid'][1:]:
        print msgid
    print "msgstr", record['msgstr'][0]
    for msgstr in record['msgstr'][1:]:
        print msgstr
    print
