from os import walk
from sys import argv
from os.path import join, splitext, relpath

EXTENSION = '.properties'
LANG_EXT = 'fr'
NOT_BLANK = 'not blank'
MAX_VALUE_LENGTH = 100

alfresco_source = '/home/andreas/alfresco-source/share/share/src/main/resources'
translations_source = '/home/andreas/alfresco-danish/share/src/main/amp/config'

def not_blank(line):
    if line == '':
        line = NOT_BLANK
    return line

def get_properties(properties_file):
    # print properties_file
    properties = {}
    with open(properties_file, 'r') as f:
        lines = f.readlines()
    previous_line = NOT_BLANK
    key = ''
    for line in lines:
        line = line.strip()
        if previous_line[-1] == '\\':
            properties[key] += line
            previous_line = line
            continue
        if line and line[0] != '#' and '=' in line:
            try:
                key, value = (x.strip() for x in line.split('=', 1))
                properties[key] = value
            except:
                print properties_file
        previous_line = not_blank(line)
    return properties

def find_files(path, lang_ext):
    filenames = []
    # full_paths = []
    for tup in walk(path):
        for filename in tup[2]:
            base, ext = splitext(filename)
            if ext == EXTENSION and base.split('_')[-1] == lang_ext:
                filename = base[:-3] + ext
                # if filename in filenames:
                    # print 'Oops... a property file with this name already exists:' + filename
                full_path = join(tup[0], filename)
                if lang_ext == LANG_EXT:
                    properties = get_properties(join(tup[0], filename))
                else:
                    properties = get_properties(join(tup[0], base + ext))
                for key in properties:
                    relative_path = relpath(full_path, path)
                    uid = '{' + relative_path + '}' + key
                    filenames.append((key, properties[key], filename, relative_path, full_path, uid))
    return filenames

def unique_properties(tuples):
    d = {}
    for t in tuples:
        if not t[0] in d:
            d[t[0]] = [t[1]]
        else:
            if not d[t[0]] == t[1]:
                print t[0],'\t', d[t[0]], '\t',t[1]
    return d

filenames = find_files(alfresco_source, LANG_EXT)
filenames_da = find_files(translations_source, 'da')

# d = unique_properties(filenames)

sorted_filenames = sorted(filenames, key = lambda filename: filename[0])
danish_dictionary = dict((x[5], x[1]) for x in filenames_da)

lines = []
for tup in sorted_filenames:
    if tup[5] in danish_dictionary:
        lines.append(tup[0] + '; '+ tup[1][:MAX_VALUE_LENGTH] + '; ' + danish_dictionary[tup[5]][:MAX_VALUE_LENGTH] + '; ' + tup[5] + '\n')
    else:
        lines.append(tup[0] + '; '+ tup[1][:MAX_VALUE_LENGTH] + '; ; ' + tup[5] + '\n')

with open('properties.csv', 'w') as f:
    f.writelines(lines)

exit(0)

"""
count = 0
count_not = 0
for key in properties_en:
    if key in properties_da: 
        print key, properties_en[key], properties_da[key]
        count += 1
    else:
         print key, properties_en[key]
         count_not += 1
    # raw_input()
"""


raise

# d = dict((x[3], (x[0], x[1], x[2], x[4])) for x in filenames)

# relative_paths = relative_path(full_paths, alfresco_source)
# relative_paths_da = relative_path(full_paths_da, translations_source)

### Sort the filename tuples
sorted_filenames = sorted(filenames, key = lambda filename: filename[3])
sorted_filenames_da = sorted(filenames_da, key = lambda filename: filename[0])

labels = [x[0] for x in sorted_filenames]
relative_paths = [x[3] for x in sorted_filenames]

for tup in sorted_filenames:
    print tup[0], tup[1], tup[2]

"""
labels = [x[0] for x in sorted_filenames]
for l in labels:
    # print type(l)
    # print l
    labels.remove(l)
    if l in labels:
        print l
"""


alf_list = [f[0] + ' ' + f[3]  + '\n' for f in sorted_filenames]
trans_list = [f[0] + ' ' + f[3]  + '\n' for f in sorted_filenames_da]

"""
for i in range(len(sorted_filenames)):
    try:
        idx = filenames_da.index(filenames[i])
        # print relative_paths[i], relative_paths_da[idx]
        alf_list.append(relative_paths[i] + '\n')
        trans_list.append(relative_paths_da[idx] + '\n')
    except:
        print filenames[i] + 'was not found'
"""

with open('/tmp/alfresco_source.txt', 'w') as f:
    f.writelines(alf_list)

with open('/tmp/translations_source.txt', 'w') as f:
    f.writelines(trans_list)

