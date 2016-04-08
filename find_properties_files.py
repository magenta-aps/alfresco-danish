from os import walk
from sys import argv
from os.path import join, splitext, relpath

EXTENSION = '.properties'
LANG_EXT = 'fr'

alfresco_source = '/home/andreas/alfresco-source/share/share/src/main/resources'
translations_source = '/home/andreas/alfresco-danish/share/src/main/amp/config'

def find_files(path, lang_ext):
    filenames = []
    full_paths = []
    for tup in walk(path):
        for f in tup[2]:
            base, ext = splitext(f)
            if ext == EXTENSION and base.split('_')[-1] == lang_ext:
                f = base[:-3] + ext
                if f in filenames:
                    print 'Oops... a property file with this name already exists:' + f
                filenames.append(f)
                full_paths.append(join(tup[0], f))
    return filenames, full_paths
    
def relative_path(paths, relative_to):
    return [relpath(f, relative_to) for f in paths]

filenames, full_paths = find_files(alfresco_source, LANG_EXT)
filenames_da, full_paths_da = find_files(translations_source, 'da')

relative_paths = relative_path(full_paths, alfresco_source)
relative_paths_da = relative_path(full_paths_da, translations_source)

alf_list = []
trans_list = []
for i in range(len(filenames)):
    try:
        idx = filenames_da.index(filenames[i])
        # print relative_paths[i], relative_paths_da[idx]
        alf_list.append(relative_paths[i] + '\n')
        trans_list.append(relative_paths_da[idx] + '\n')
    except:
        print filenames[i] + 'was not found'

with open('/tmp/alfresco_source.txt', 'w') as f:
    f.writelines(alf_list)

with open('/tmp/translations_source.txt', 'w') as f:
    f.writelines(trans_list)

"""
for path in relative_paths:
    if path in relative_paths_da:
        print 'Hurra: ' + path
    else:
        print 'Oops: ' + path
"""
