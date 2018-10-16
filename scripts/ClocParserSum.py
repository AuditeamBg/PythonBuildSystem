
import os
import sys


total = dict()
root_folder = sys.argv[-1]

headers = list()


if not os.path.isdir(root_folder):
    raise Exception('Directory does not exist:', root_folder)



def search_dir(folder):
    for f in os.listdir(folder):
        if os.path.isdir(folder + '/' + f):
            for _ in search_dir(folder + '/' + f): yield _
        elif os.path.isfile(folder + '/' + f):
            if 'readme.txt' in f:
                yield folder + '/' + f
                
    
for f in search_dir(root_folder):
    with open(f, 'r') as readme_file:
        readme_content = readme_file.read()

    if 'LOC' not in readme_content:
        continue

    loc_contents = readme_content.split('\nLOC\n\n')[1].split('\n')

    headers = loc_contents[0].split(',')[:-2]

    for lines in loc_contents[1:]:
        if lines:
            n_files, language, blank, comment, code = lines.split(',')

            if language in total.keys():
                n_files = int(n_files) + int(total[language]['files'])
                blank = int(blank) + int(total[language]['blank'])
                comment = int(comment) + int(total[language]['comment'])
                code = int(code) + int(total[language]['code'])

            total[language] = {'files': n_files, 'blank': blank, 'comment': comment, 'code': code}

print ','.join(headers)

for k in reversed(sorted(total.keys(), key=lambda y: (int(total[y]['code'])))):
    print ','.join([str(x) for x in [total[k]['files'],
                                     k,
                                     total[k]['blank'],
                                     total[k]['comment'],
                                     total[k]['code']]])