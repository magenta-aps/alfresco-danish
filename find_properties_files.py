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


def read_properties_from_csv(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    # content = tuple([x.strip() for x in [line.split(';')[:4] for line in lines]])
    content = [line.split(';')[:4] for line in lines]
    content = [tuple([y.strip() for y in x]) for x in content]
    return content

def unique_properties(tuples):
    d = {}
    for t in tuples:
        if not t[0] in d:
            d[t[0]] = [t[1]]
        else:
            if not d[t[0]] == t[1]:
                print t[0],'\t', d[t[0]], '\t',t[1]
    return d

def generate_new_danish_dictionary()

"""
### Generate new danish dict
loop over uid
  if uid not in danish_dict
    if not value for uid is empty in english_dict
      if value not empty in csv_dict
        print englist value
        print danish value
        ask: update danish value?
        if ok
          update danish_dict
        else
          ask for replacement
          if not stop
            update danish_dict
          else
            add uid to list
        write new danish_dict to file
        write uid list of mistakes 
"""

filenames = find_files(alfresco_source, LANG_EXT)
filenames_da = find_files(translations_source, 'da')

english_dictionary = dict((x[5], x[1]) for x in filenames)
danish_dictionary = dict((x[5], x[1]) for x in filenames_da)

csv = read_properties_from_csv('properties_corrected.csv')
csv_dictionary = dict((x[3], x[2]) for x in csv)

sorted_filenames = sorted(filenames, key = lambda filename: filename[0])

### Generate CSV file ###
lines = []
for tup in sorted_filenames:
    if tup[5] in danish_dictionary:
        pass
        lines.append(tup[0] + '; '+ tup[1][:MAX_VALUE_LENGTH] + '; ' + danish_dictionary[tup[5]][:MAX_VALUE_LENGTH] + '; ' + tup[5] + '\n')
    else:
        lines.append(tup[0] + '; '+ tup[1][:MAX_VALUE_LENGTH] + '; ; ' + tup[5] + '\n')

with open('properties.csv', 'w') as f:
    f.writelines(lines)

### Find the maximum length of the values
# values_lengths = [len(x[1]) for x in sorted_filenames]
# print max(values_lengths) 



"""
for tup in csv:
    uid = tup[-1]
    try:
        if tup[1] != english_dictionary[uid]:
            print uid
    except:
        print tup
"""
