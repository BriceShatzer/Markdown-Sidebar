import os
from os.path import join
def checkForWikiPage(file):
    # insure that the file being passed in is a markdown file that isn't an include/subpage
    page = file[file.rfind('/')+1:]
    if page[-3:] != '.md' or page.startswith('_'):
        return False
    else: 
        return True 

def displayString(filePathString):
    # return a pretty page title by adding back spaces and removing the path & extension from a passed in file path
    str = filePathString    
    if '/' in str: 
        str = str[str.rfind('/')+1 : -3]
    return str.replace('-',' ')

def createIndexFile(startpath, indexFile):
    for root, dirs, files in os.walk(startpath):
        files = [join(root,f) for f in files if not f[0] == '.']
        #dirs[:] = [d for d in dirs if not d[0] == '.'] #dirs values aren't used
        level = root.replace(startpath, '').count(os.sep) - 1
        indent = ' ' * 2 * (level)

        directory = os.path.basename(root)
        if directory == '.':
            # if pages exists in the root, create links to them with no idention
            for f in files:
                if checkForWikiPage(f):                               
                    path = '/' + os.getcwd().split(os.sep)[-1] + f[1:-3]
                    indexFile.write('- [{}]({})\n'.format( displayString(f), path) )
        else:
            # otherwise, write directories add indention based on the nested depth
            indexFile.write('{}- {}\n'.format( indent, displayString(os.path.basename(root)) ) )
            subindent = ' ' * 2 * (level + 1)            

            for f in files:
                if checkForWikiPage(f):
                    path = '/' + os.getcwd().split(os.sep)[-1] + f[1:-3]

                    if displayString(f).lower() == "home":
                        # if a 'Home' page exists in a directory, rewrite that list item to link to that page
                        
                        # close the file & make it's contents editable
                        indexFile.close()                        
                        indexFile = open('_Sidebar.md', 'r')
                        filedata = indexFile.read()
                        indexFile.close()
                        # make the edit
                        parentDirName = displayString(os.path.basename(root))
                        parentDirHomeLink = '- ['+parentDirName+']('+path+')'                     
                        filedata = filedata.replace('- '+parentDirName, parentDirHomeLink)
                        # rewrite the file with the edit
                        indexFile = open('_Sidebar.md','w')
                        indexFile.write(filedata)                                                
                    else:
                        #otherwise, create a link to the page
                        indexFile.write('{}- [{}]({})\n'.format( subindent, displayString(f), path) )

indexFile = open('_Sidebar.md', 'w')

createIndexFile('.', indexFile)
indexFile.close();