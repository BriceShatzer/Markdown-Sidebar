import os
from os.path import join
def checkForWikiPage(file):
    page = file[file.rfind('/')+1:]
    if page[-3:] != '.md' or page.startswith('_'):
        return False
    else: 
        return True 


def createIndexFile(startpath, indexFile):
    for root, dirs, files in os.walk(startpath):
        files = [join(root,f) for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']
        level = root.replace(startpath, '').count(os.sep) - 1
        indent = ' ' * 2 * (level)

        directory = os.path.basename(root)
        if directory == '.':
            for f in files:
                if checkForWikiPage(f):                               
                    path = '/' + os.getcwd().split(os.sep)[-1] + f[1:-3]
                    indexFile.write('- [{}]({})\n'.format( f[f.rfind('/')+1 : -3].replace('-',' ') , path) )
        else:
            indexFile.write('{}- {}\n'.format(indent, os.path.basename(root)))
            subindent = ' ' * 2 * (level + 1)
            for f in files:
                if checkForWikiPage(f):
                    path = '/' + os.getcwd().split(os.sep)[-1] + f[1:-3]
                    indexFile.write('{}- [{}]({})\n'.format(subindent, f[f.rfind('/')+1 : -3].replace('-',' ') , path) )


indexFile = open('_Sidebar.md', 'w')

createIndexFile('.', indexFile)
indexFile.close();
