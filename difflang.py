#!/usr/local/bin/python

import os

def get_record(handle):
    record = {'msgid': [], 'msgstr': [], 'comments': []}
    item = 'msgid'

    while True:
        line = handle.readline()
        if line == '':
            return {'eof': True, 'result': record}
        
        split = line.split()
        length = len(split)
    
        if length == 0:
            if len(record['msgid']) == 0:
                continue
            
            ret = record
            record = {'msgid': [], 'msgstr': [], 'comments': []}
            item = 'msgid'
            return {'eof': False, 'result': ret}
    
        if length == 1:
            continue

        keyword = split[0]
        if keyword == 'msgid':
            record['msgid'].append(line.partition('msgid')[2][:-1])
        elif keyword == 'msgstr':
            record['msgstr'].append(line.partition('msgstr')[2][:-1])
            item = 'msgstr'
        elif line[0] == '#':
            record['comments'].append(line[:-1])
        else:
            record[item].append(line[:-1])

ting_array = []
#inp = os.popen('git show origin/lang:ru_RU.po')
inp = open('ru_RU.po')

while True:
    record = get_record(inp)
    ting_array.append(record['result'])
    if record['eof']:
        break
inp.close()    

#inp = os.popen('git show github/master:ru_RU.po')
inp = open('ru_RU.po.opnsense')
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
    print "msgid ", record['msgid'][0]
    for msgid in record['msgid'][1:]:
        print msgid
    print "msgstr ", record['msgstr'][0]
    for msgstr in record['msgstr'][1:]:
        print msgstr
    print
