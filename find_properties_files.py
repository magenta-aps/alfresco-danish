from os import walk
from sys import argv
from os.path import join, splitext, relpath
from pickle import dump

EXTENSION = '.properties'
LANG_EXT = 'fr'
NOT_BLANK = 'not blank'
MAX_VALUE_LENGTH = 100

# alfresco_source = '/home/andreas/alfresco-source/share/share/src/main/resources'
alfresco_source = '/mnt/sdb1/magenta/alfresco-source/share/share/src/main/resources'
# translations_source = '/home/andreas/magenta/alfresco-danish/share/src/main/amp/config'
translations_source = '/mnt/sdb1/magenta/alfresco-danish/share/src/main/amp/config'

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

### Generate CSV file ###
def generate_csv(sorted_filenames):
    lines = []
    for tup in sorted_filenames:
        if tup[5] in danish_dictionary:
            pass
            lines.append(tup[0] + '; '+ tup[1][:MAX_VALUE_LENGTH] + '; ' + danish_dictionary[tup[5]][:MAX_VALUE_LENGTH] + '; ' + tup[5] + '\n')
        else:
            lines.append(tup[0] + '; '+ tup[1][:MAX_VALUE_LENGTH] + '; ; ' + tup[5] + '\n')

    with open('properties.csv', 'w') as f:
        f.writelines(lines)

def generate_new_danish_dictionary(english_dict, danish_dict, csv_dict):
    danish_dict_additions = {}
    translation_mistakes_uid = []
    for uid in english_dict.keys():
        if uid not in danish_dict.keys() and english_dict[uid] != '' and csv_dict[uid] != '':
            print 50*'-'
            print uid
            print english_dict[uid]
            print csv_dict[uid]
            q = raw_input('Use danish value above (Y/n)? ')
            if q in ('Y', 'y', ''):
                danish_dict_additions[uid] = csv_dict[uid]
            elif q == 'n':
                translation_mistakes_uid.append(uid)
                replacement = raw_input('Enter alternative danish translation: ')
                if replacement != 'stop':
                    danish_dict_additions[uid] = replacement
                else:
                    return danish_dict_additions, translation_mistakes_uid
            else:
                return danish_dict_additions, translation_mistakes_uid

filenames = find_files(alfresco_source, LANG_EXT)
filenames_da = find_files(translations_source, 'da')

e = english_dictionary = dict((x[5], x[1]) for x in filenames)
d = danish_dictionary = dict((x[5], x[1]) for x in filenames_da)

csv = read_properties_from_csv('properties_corrected.csv')
c = csv_dictionary = dict((x[3], x[2]) for x in csv)

sorted_filenames = sorted(filenames, key = lambda filename: filename[0])
generate_csv(sorted_filenames)

da_dict_add, mistakes = generate_new_danish_dictionary(english_dictionary, danish_dictionary, csv_dictionary)
with open('xxxda_dict_add.dat', 'w') as f:
    dump((da_dict_add, mistakes), f)



