SUFFIXES = {1000:['KB','MB','GB','TB','PB','ZB','YB'],
            1024:['KiB','MiB','GiB','TiB','PiB','ZiB','YiB']}

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

print ('Start...')

import os

def print_all (path):
    global files_all,size_all,path_list,path_dict,files_list,files_dict,extentions_list,extentions_dict,superpath_list,superpath_dict
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
            print_all (dirs[d])


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
#print_all('F:\# Hudba')
#print_all("D:\\# Izotope")
print_all("D:\\")

from operator import itemgetter

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
print ('Seřaď podle velikosti:')
temp_p.sort(key=itemgetter(3), reverse = True)
with open ("export.txt", mode = "w", encoding = "utf-8") as f:
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
