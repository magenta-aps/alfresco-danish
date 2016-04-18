# -*- coding: utf-8 -*-

from os import walk, makedirs
from os.path import join, splitext, relpath, isfile, dirname, exists
from pickle import dump, load
from sys import argv


EXTENSION = '.properties'
LANG_EXT = 'fr'
NOT_BLANK = 'not blank'
MAX_VALUE_LENGTH = 200
CSV_SEPARATOR = ";"

# alfresco_source = '/home/andreas/alfresco-source/share/share/src/main/resources'
# alfresco_source = 'home/andreas/alfresco-5.1.e/tomcat/webapps/share/WEB-INF/classes'
# translations_source = '/home/andreas/alfresco-danish/share/src/main/amp/config'

### Aikau ###
alfresco_source = '/home/andreas/alfresco-source/Aikau/aikau/src/main/resources'
translations_source = '/home/andreas/alfresco-danish/share/src/main/amp/web/js/aikau/LATEST'


# alfresco_source = '/mnt/sdb1/magenta/alfresco-source/share/share/src/main/resources'
# translations_source = '/mnt/sdb1/magenta/alfresco-danish/share/src/main/amp/config'

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


def read_properties_from_csv(filename, csv_sep):
    with open(filename, 'r') as f:
        lines = f.readlines()
    # content = tuple([x.strip() for x in [line.split(';')[:4] for line in lines]])
    content = [line.split(csv_sep)[:4] for line in lines]
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
def generate_csv(sorted_filenames, separator = CSV_SEPARATOR):
    separator += ' '
    lines = []
    for tup in sorted_filenames:
        if tup[5] in danish_dictionary:
            pass
            lines.append(tup[0] + separator+ tup[1][:MAX_VALUE_LENGTH] + separator + danish_dictionary[tup[5]][:MAX_VALUE_LENGTH] + separator + tup[5] + '\n')
        else:
            lines.append(tup[0] + separator+ tup[1][:MAX_VALUE_LENGTH] + separator + tup[5] + '\n')

    with open('properties.csv', 'w') as f:
        f.writelines(lines)

def generate_new_danish_dictionary(english_dict, danish_dict, csv_dict, danish_dict_additions = {}, translation_mistakes_uid = []):
    print len(english_dict.keys())
    print len(danish_dict.keys())
    print len(danish_dict_additions.keys())
    print len(translation_mistakes_uid)
    for uid in english_dict.keys():
        print uid
        if uid not in danish_dict.keys() and uid not in danish_dict_additions.keys() and english_dict[uid] != '' and csv_dict[uid] != '':
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
                danish_dict_additions[uid] = replacement
            else:
                return danish_dict_additions, translation_mistakes_uid
    return danish_dict_additions, translation_mistakes_uid

def load_dict(filename):
    with open(filename, 'r') as f:
        return load(f)

def dump_dict(filename, dictionary, mistakes):
    with open(filename, 'w') as f:
        dump((dictionary, mistakes), f)

filenames = find_files(alfresco_source, LANG_EXT)
filenames_da = find_files(translations_source, 'da')

e = english_dictionary = dict((x[5], x[1]) for x in filenames)
d = danish_dictionary = dict((x[5], x[1]) for x in filenames_da)

# csv = read_properties_from_csv('properties_corrected2.csv', CSV_SEPARATOR)
# c = csv_dictionary = dict((x[3], x[2]) for x in csv)

sorted_filenames = sorted(filenames, key = lambda filename: filename[0])
generate_csv(sorted_filenames)

# da_dict_add, mistakes = load_dict('da_dict_add_final.dat')
# da_dict_add, mistakes = generate_new_danish_dictionary(english_dictionary, danish_dictionary, csv_dictionary, da_dict_add, mistakes)
# 
# dump_dict('da_dict_add.dat', da_dict_add, mistakes)



# lines = []
# for tup in sorted_filenames:
#     if tup[5] in da_dict_add.keys() and da_dict_add[tup[5]] == 'TODO':
#         lines.append(tup[0] + CSV_SEPARATOR + tup[1][:MAX_VALUE_LENGTH] + CSV_SEPARATOR + ' ' + CSV_SEPARATOR + tup[5] + '\n')
# 
# with open('properties.csv', 'w') as f:
#     f.writelines(lines)

### Add corrections 2 ###

# for tup in csv:
#     uid = tup[-1]
#     print 50*'-'
#     print uid
#     print english_dictionary[uid]
#     print tup[2]
#     q = raw_input('Use danish value above (Y/n)? ')
#     if q in ('Y', 'y', ''):
#         da_dict_add[uid] = tup[2]
#     elif q == 'n':
#         replacement = raw_input('Enter alternative danish translation: ')
#         da_dict_add[uid] = replacement
#     else:
#         raise
# 
# dump_dict('da_dict_add_final.dat', da_dict_add, [])


# for key in da_dict_add.keys():
#     da_dict_add[key] = da_dict_add[key].replace('æ', '\\u00E6')
#     da_dict_add[key] = da_dict_add[key].replace('ø', '\\u00F8')
#     da_dict_add[key] = da_dict_add[key].replace('å', '\\u00E5')
#     da_dict_add[key] = da_dict_add[key].replace('Æ', '\\u00C6')
#     da_dict_add[key] = da_dict_add[key].replace('Ø', '\\u00D8')
#     da_dict_add[key] = da_dict_add[key].replace('Å', '\\u00C5')


def update_properties_files_with_new_danish_values(danish_dict_additions, path_prefix):
    for uid in danish_dict_additions.keys():
        path, label = uid.split('}')
        path = path[1:]
        full_path = join(path_prefix, path)
        full_path = full_path.replace(EXTENSION, '_da' + EXTENSION)
        # print full_path
        
        print uid
        if isfile(full_path):
            print 'File already exists'
            with open(full_path, 'a') as f:
                f.write('\n' + label + '=' + danish_dict_additions[uid] + '\n')
        else:
            print 'Creating new file'
            if not exists(dirname(full_path)):
                makedirs(dirname(full_path))
            with open(full_path, 'w') as f:
                f.write(label + '=' + danish_dict_additions[uid] + '\n')
            # raw_input('tryk')

# update_properties_files_with_new_danish_values(da_dict_add, translations_source)

