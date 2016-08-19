# -*- coding: utf-8 -*-

from os import walk, makedirs, path, getcwd
from os.path import join, splitext, relpath, isfile, dirname, exists
from pickle import dump, load
import argparse

EXTENSION = '.properties'
LANG_EXT = 'fr'
NOT_BLANK = 'not blank'
MAX_VALUE_LENGTH = 200
CSV_SEPARATOR = "~"

# Get arguments for paths
parser = argparse.ArgumentParser(description='This is a script by Magenta')
parser.add_argument('-s','--share', help='Share source path',required=True)
parser.add_argument('-a','--aikau', help='Aikau source path',required=True)
parser.add_argument('-t', '--translate', action='store_true')
parser.add_argument('-i', '--inject', action='store_true')
parser.add_argument('-e', '--extract', action='store_true')
args = parser.parse_args()


# Find path for script
rootDir = getcwd()
fileDir = path.dirname(path.abspath(__file__))

# Set paths for sources
share_source = path.join(rootDir, args.share + 'share/src/main/resources')
aikau_source = path.join(rootDir, args.aikau + 'aikau/src/main/resources')
share_translations = path.join(fileDir, 'share/src/main/amp/config')
aikau_translations = path.join(fileDir, 'share/src/main/amp/web/js/aikau/LATEST')

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
    with open(fileDir + '/' + filename, 'r') as f:
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
def generate_csv(prefix, sorted_filenames, da_dictionary, separator = CSV_SEPARATOR):
    lines = []
    for tup in sorted_filenames:
        danish_str = ''
        if tup[5] in da_dictionary:
            danish_str = da_dictionary[tup[5]][:MAX_VALUE_LENGTH]
        lines.append(tup[0] + separator+ tup[1][:MAX_VALUE_LENGTH] + separator + danish_str + separator + tup[5] + '\n')

    with open(fileDir + '/' + prefix + '_properties.csv', 'w') as f:
        f.writelines(lines)

def generate_new_danish_dictionary(en_dict, da_dict, csv_dict, da_dict_add = {}, translation_mistakes_uid = []):
    print len(en_dict.keys())
    print len(da_dict.keys())
    print len(da_dict_add.keys())
    print len(translation_mistakes_uid)
    for uid in en_dict.keys():
        print uid
        if uid not in da_dict.keys() and uid not in da_dict_add.keys() and en_dict[uid] != '' and csv_dict[uid] != '':
            print 50*'-'
            print uid
            print en_dict[uid]
            print csv_dict[uid]
            q = raw_input('Use danish value above (Y/n)? ')
            if q in ('Y', 'y', ''):
                da_dict_add[uid] = csv_dict[uid]
            elif q == 'n':
                translation_mistakes_uid.append(uid)
                replacement = raw_input('Enter alternative danish translation: ')
                da_dict_add[uid] = replacement
            else:
                return da_dict_add, translation_mistakes_uid
    return da_dict_add, translation_mistakes_uid

def update_properties_files_da(da_dict_add, path_prefix):
    for uid in da_dict_add.keys():
        print 'uid:' + uid
        path, label = uid.split('}')
        path = path[1:]
        full_path = join(path_prefix, path)
        full_path = full_path.replace(EXTENSION, '_da' + EXTENSION)
        print uid
        if isfile(full_path):
            print 'File already exists'
            with open(full_path, 'a') as f:
                f.write('\n' + label + '=' + da_dict_add[uid] + '\n')
        else:
            print 'Creating new file'
            if not exists(dirname(full_path)):
                makedirs(dirname(full_path))
            with open(full_path, 'w') as f:
                f.write(label + '=' + da_dict_add[uid] + '\n')

def extract(prefix, filenames, da_dictionary):
    sorted_filenames = sorted(filenames, key = lambda filename: filename[0])
    generate_csv(prefix, sorted_filenames, da_dictionary)

def inject(prefix, translation, en_dictionary, da_dictionary):
    csv = read_properties_from_csv(prefix + '_properties.csv', CSV_SEPARATOR)
    csv_dictionary = dict((x[3], x[2]) for x in csv)
    da_dict_add, mistakes = generate_new_danish_dictionary(en_dictionary, da_dictionary, csv_dictionary)
    if(args.translate):
        for key in da_dict_add.keys():
            da_dict_add[key] = da_dict_add[key].replace('æ', '\\u00E6')
            da_dict_add[key] = da_dict_add[key].replace('ø', '\\u00F8')
            da_dict_add[key] = da_dict_add[key].replace('å', '\\u00E5')
            da_dict_add[key] = da_dict_add[key].replace('Æ', '\\u00C6')
            da_dict_add[key] = da_dict_add[key].replace('Ø', '\\u00D8')
            da_dict_add[key] = da_dict_add[key].replace('Å', '\\u00C5')
    update_properties_files_da(da_dict_add, translation)

def init(prefix, source, translation):
    filenames = find_files(source, LANG_EXT)
    filenames_da = find_files(translation, 'da')
    en_dictionary = dict((x[5], x[1]) for x in filenames)
    da_dictionary = dict((x[5], x[1]) for x in filenames_da)
    if(args.extract):
        extract(prefix, filenames, da_dictionary)
    if(args.inject):
        inject(prefix, translation, en_dictionary, da_dictionary)

init('share', share_source, share_translations)
init('aikau', aikau_source, aikau_translations)

