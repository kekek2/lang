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

        if length == 1:
            continue

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


new_array = []
inp = open('2016.12.12.diff.ru_RU.po')

while True:
    record = get_record(inp)
    new_array.append(record['result'])
    if record['eof']:
        break
inp.close()

inp = open('ru_RU.po')

while True:
    record = get_record(inp)
    for rec in new_array:
        if rec['msgid'] == record['result']['msgid']:
            record['result']['msgstr'] = rec['msgstr']
            new_array.remove(rec)
            break
    if record['eof']:
        break
    for comment in record['result']['comments']:
        print comment
    if len(record['result']['msgid']) == 0:
        continue
    print "msgid", record['result']['msgid'][0]
    for msgid in record['result']['msgid'][1:]:
        print msgid
    print "msgstr", record['result']['msgstr'][0]
    for msgstr in record['result']['msgstr'][1:]:
        print msgstr
    print
inp.close()

