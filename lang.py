class Lang:
    def __init__(self, file_name):
        self.handle = open(file_name)
        self.data = []

        while True:
            record = self.__get_record()
            self.data.append(record['result'])
            if record['eof']:
                break
        self.handle.close()

    def __get_record(self):
        rec1 = {'msgid': [], 'msgstr': [], 'comments': []}
        item = 'msgid'

        while True:
            line = self.handle.readline()
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

    def print_records(self, empty=False):
        for record in self.data:
            if empty and record['msgstr'] != ['""']:
                continue
            for comment in record['comments']:
                print(comment)
            if len(record['msgid']) == 0:
                continue
            print("msgid", record['msgid'][0])
            for msgid in record['msgid'][1:]:
                print(msgid)
            print("msgstr", record['msgstr'][0])
            for msgstr in record['msgstr'][1:]:
                print(msgstr)
            print()

    def merge(self, merge):
        for base in self.data:
            for rec in merge.data:
                if rec['msgid'] == base['msgid']:
                    base['msgstr'] = rec['msgstr']
                    break