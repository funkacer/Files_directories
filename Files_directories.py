import os
from operator import itemgetter

files_all=0
size_all=0
path_list=[]
path_dict={}
files_list=[]
files_dict={}
extentions_list=[]
extentions_dict={}
superpath_list=[]
superpath_dict={}

SUFFIXES = {1000:['KB','MB','GB','TB','PB','ZB','YB'],
            1024:['KiB','MiB','GiB','TiB','PiB','ZiB','YiB']}

class Element():

    def get_path(self):
        return self._path

    def get_name(self):
        return self._name

    def get_names(self):
        return [self._name]

    def get_elements(self):
        return self

    def get_tree(self):
        return self._name

    def get_count(self):
        return 1

    def get_size(self):
        return self._size

    def get_extension(self):
        return self._extension

    def get_isFile(self):
        return self._isFile

    def get_isDirectory(self):
        return self._isDirectory

class File(Element):

    def __init__(self, name):
        self._name = name
        self._isFile = True
        self._isDirectory = False

    def compute_stats(self):
        self._path = os.path.realpath(self._name)
        metadata = os.stat(self._name)
        self._size = metadata.st_size
        self._extention = os.path.splitext(self._name)[1]


class Directory(Element):

    def __init__(self, name):
        self._name = name
        self._elements = []
        self._isFile = False
        self._isDirectory = True

    def add_element(self, element):
        self._elements.append(element)

    def compute_stats(self):
        for e in self._elements:
            e.compute_stats()

    def get_count(self):
        count = 0
        for e in self._elements:
            count += e.get_count()
        return count

    def get_size(self):
        size = 0
        for e in self._elements:
            size += e.get_size()
        return size

    def get_names(self):
        names = set()
        for e in self._elements:
            if e.get_isDirectory:
                for name in e.get_names():
                    names.add((e.get_name(), name))
            #tree += e.get_tree() + "\n"
        return names

    def get_dict_count(self):
        tree = {}
        for e in self._elements:
            #print(e.get_name(), e.get_names(), e.get_isDirectory())
            if e.get_isDirectory():
                if tree.get(e.get_name()) is None:
                    tree[e.get_name()] = e.get_count()
                else:
                    tree[e.get_name()] += e.get_count()
        return tree

    def get_dict_size(self):
        tree = {}
        for e in self._elements:
            tree[e.get_name()] = e.get_size()
        return tree

def approximate_size(size, a_kilobite_is_1024_bytes=True):
    '''Convert

    Returns: string
    '''
    if size < 0:
        raise ValueError('nubmer must be non-negative')

    multiple = 1024 if a_kilobite_is_1024_bytes else 1000
    for suffix in SUFFIXES[multiple]:
        size /= multiple
        if size < multiple:
            return '{0:.1f} {1}'.format(size, suffix)

    raise ValueError('nubmer too large')

def scan_all (path, previous_directory):
    global files_all,size_all,path_list,path_dict,files_list,files_dict,extentions_list,extentions_dict,superpath_list,superpath_dict, tree
    #dirs = [(os.path.realpath(entry.name)) for entry in os.scandir(path) if not entry.name.startswith('.') and entry.is_dir()]
    if not "D:\\$RECYCLE.BIN" in path and not "D:\\System Volume Information" in path:
        dirs = [(entry.path) for entry in os.scandir(path) if not entry.name.startswith('.') and entry.is_dir()]
        #print (dirs)
        # print(path, len(dirs)) '''vypíše cestu a počet podadresářů; pokud > 0 tak má podadresáře => zapíše se jako superpath'''
        if len (dirs) > 0:
            superpath_list.append(path)
            superpath_dict[path] = [0,0,-1] #jinak by to i aktuální adresář napočítalo jako +1

        size_path = 0

        #files = [(os.path.realpath(entry.name)) for entry in os.scandir(path) if not entry.name.startswith('.') and entry.is_file()]
        files = [(entry.path) for entry in os.scandir(path) if not entry.name.startswith('.') and entry.is_file()]
        #print (files)

        metadata_dict = {os.path.realpath(f):os.stat(f) for f in files}

        for f in range(len(files)):
            #print (files[f],approximate_size(metadata_dict[files[f]].st_size,False))
            files_list.append(os.path.split(files[f]))
            files_dict[os.path.realpath(files[f])]=metadata_dict[files[f]]
            size = metadata_dict[files[f]].st_size
            size_path += size
            extention = os.path.splitext(files[f])[1]
            i=0
            for e in extentions_list:
                if extention == e: i = 1
            if i == 0:
                extentions_list.append(extention)
                extentions_dict[extention] = [0,0]
            extentions_dict[extention][0] += 1
            extentions_dict[extention][1] += size
            file = File(files[f])
            previous_directory.add_element(file)

        #print (len (files), approximate_size(size,False)) - toto se vypisuje
        files_all += len (files)
        size_all += size_path
        path_list.append(path)
        path_dict[path]=[len(files),size_path, len(dirs)]
        for sp in superpath_list:
            if sp == path[0:len(sp)]:
                superpath_dict[sp][0] += len (files)
                superpath_dict[sp][1] += size_path
                superpath_dict[sp][2] += 1
                '''toto napočítá i podpodadresáře!!!'''
        for d in range(len (dirs)):
            directory = Directory(dirs[d])
            previous_directory.add_element(directory)
            #tree[level].append([])  # append branch to level
            scan_all (dirs[d], directory)

def main():
    global tree
    #scan_all('F:\# Hudba')
    #scan_all("D:\\# Izotope")
    path = os.getcwd()
    parent_directory = Directory(path)
    print(parent_directory.get_name())
    print ('Start...')
    scan_all(path, parent_directory)

    parent_directory.compute_stats()
    print("get_count", parent_directory.get_count())
    print("get_size", parent_directory.get_size())
    print("get_names", parent_directory.get_names())
    #rint("get_dict_count", parent_directory.get_dict_count())
    #print("get_dict_size", parent_directory.get_dict_size())

    temp_p = []
    for e in path_dict:
        temp_p.append([e,str.lower(e),path_dict[e][0],path_dict[e][1],path_dict[e][2]])
    '''print ()
    temp_p.sort(key=itemgetter(1))
    for e in range(len(temp_p)):
        print (temp_p[e][0],temp_p[e][1],temp_p[e][2],temp_p[e][3])'''
    '''
    print ()
    print ('Seřaď podle názvu:')
    temp_p.sort(key=itemgetter(1))
    for e in temp_p:
        print (e[0],path_dict[e[0]][0],approximate_size(path_dict[e[0]][1],False),path_dict[e[0]][2])
    print ()
    print ('Seřaď podle počtu souborů:')
    temp_p.sort(key=itemgetter(2))
    for e in temp_p:
        print (e[0],path_dict[e[0]][0],approximate_size(path_dict[e[0]][1],False),path_dict[e[0]][2])
    print ()
    '''
    print('Order by size.')
    filename = path.split(os.sep)[-1] + ".txt"
    print(f'Filename: {filename}')
    temp_p.sort(key=itemgetter(3), reverse = True)
    with open (filename, mode = "w", encoding = "utf-8") as f:
        a = ""
        for e in temp_p:
            #print (e[0],path_dict[e[0]][0],approximate_size(path_dict[e[0]][1],False),path_dict[e[0]][2])
            a += e[0] + "\t" + str(path_dict[e[0]][0]) + "\t" + approximate_size(path_dict[e[0]][1],False) + "\t" + str(path_dict[e[0]][2]) + "\n"
        f.write(a)

    '''
    print ()
    print ('Seřaď podle počtu adresářů:')
    temp_p.sort(key=itemgetter(4))
    for e in temp_p:
        print (e[0],path_dict[e[0]][0],approximate_size(path_dict[e[0]][1],False),path_dict[e[0]][2])

    print ()
    for sp in sorted(superpath_list,key=str.lower):
        print (sp,superpath_dict[sp][0],approximate_size(superpath_dict[sp][1],False),superpath_dict[sp][2])

    temp_e = []
    for e in extentions_dict:
        temp_e.append([e,str.lower(e),extentions_dict[e][0],extentions_dict[e][1]])
    '''

    '''print ()
    temp_e.sort(key=itemgetter(1))
    for e in range(len(temp_e)):
        print (temp_e[e][0],temp_e[e][1],temp_e[e][2],temp_e[e][3])'''

    '''
    print ()
    temp_e.sort(key=itemgetter(1))
    for e in temp_e:
        print (e[0],extentions_dict[e[0]][0],approximate_size(extentions_dict[e[0]][1],False))
    print ()
    temp_e.sort(key=itemgetter(2))
    for e in temp_e:
        print (e[0],extentions_dict[e[0]][0],approximate_size(extentions_dict[e[0]][1],False))
    print ()
    temp_e.sort(key=itemgetter(3))
    for e in temp_e:
        print (e[0],extentions_dict[e[0]][0],approximate_size(extentions_dict[e[0]][1],False))
    '''

    '''for e in sorted(extentions_dict,key=itemgetter(2)):
        print (e,extentions_dict[e][0],extentions_dict[e][1])
        #print (e,extentions_dict[e][0],approximate_size(extentions_dict[e][1],False))'''

    print ()
    print ('Konec...',files_all,approximate_size(size_all,False))
    #print ('Konec...',files_all,approximate_size(size_all,False),approximate_size(size_all/files_all,False)) - vypíše i průměr

if __name__ == "__main__":
    main()
