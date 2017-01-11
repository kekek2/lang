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


def print_record(record):
    if record['msgstr'] != ['""']:
        return
    for comment in record['comments']:
        print comment
    if len(record['msgid']) == 0:
        return
    print "msgid", record['msgid'][0]
    for msgid in record['msgid'][1:]:
        print msgid
    print "msgstr", record['msgstr'][0]
    for msgstr in record['msgstr'][1:]:
        print msgstr
    print

# inp = os.popen('git show origin/lang:ru_RU.po')
inp = open('ru_RU.po')

while True:
    record = get_record(inp)
    print_record(record['result'])
    if record['eof']:
        break
inp.close()
