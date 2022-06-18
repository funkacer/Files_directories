
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
#print (os.pardir)

#import D047
#print (D047.approximate_size(1000))

#print(glob.glob('*'))
#print([os.path.split(os.path.realpath(f)) for f in glob.glob('*')])

#(dirname,filename) = [os.path.split(os.path.realpath(f)) for f in glob.glob('*')]
#filename = [os.path.split(os.path.realpath(f)) for f in glob.glob('*')]
#print (filename)
''' vypíše seznam cest a názvů'''

#(sortname,extention)= os.path.splitext(path)
#extention = [os.path.splitext(os.path.realpath(f)) for f in glob.glob('*')]
#print (extention)
''' vypíše seznam souborů a přípon'''

#print('Tady:')

def print_all (path):
    global files_all,size_all,path_list,path_dict,files_list,files_dict,extentions_list,extentions_dict,superpath_list,superpath_dict
    #dirs = [(os.path.realpath(entry.name)) for entry in os.scandir(path) if not entry.name.startswith('.') and entry.is_dir()]
    dirs = [(entry.path) for entry in os.scandir(path) if not entry.name.startswith('.') and entry.is_dir()]
    #print (dirs)
    # print(path, len(dirs)) '''vypíše cestu a počet podadresářů; pokud > 0 tak má podadresáře => zapíše se jako superpath'''
    if len (dirs) > 0:
        superpath_list.append(path)
        superpath_dict[path] = [0,0,-1] #jinak by to i aktuální adresář napočítalo jako +1

    #print () - toto se vypisuje
    #if len(dirs)>0:print (dirs[0])
    #print(path) - toto se vypisuje
    
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
        #print(files_all,approximate_size(size_all,False)) - toto se vypisuje
        print_all (dirs[d])
        #print()
        #print (dirs[d])
    
    #entries = [(entry) for entry in os.scandir(os.getcwd()) if not entry.name.startswith('.')]
    #print (entries)

    #metadata = [(f, os.stat(f)) for f in glob.glob('*')]
    #metadata = [(os.path.realpath(f), os.stat(f)) for f in glob.glob('*')]

    #print (metadata[0])
    #print (metadata[-1][0],'s atributy'.upper(), metadata[-1][1])

    #metadata_dict = {os.path.realpath(f):os.stat(f) for f in glob.glob('*')}
    #metadata_dict = {os.path.realpath(f):os.stat(f) for f in files}

    #print(list(metadata_dict.keys()))
    #print(metadata_dict[metadata[-1][0]].st_size)
    #print(metadata_dict[files[-1]].st_size)

    #for f in range(len (files)):
        #print (files[f],approximate_size(metadata_dict[files[f]].st_size,False))

    #print(metadata_dict['C:\\Users\\cerny\\OneDrive\\Favorites\\Python\\aaa'])

    #print (files_all, (approximate_size(size_all,False)))

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
#print_all ('D:\cerny\music')
#print_all('D:\\aaa')
#print_all('D:\\')
print_all('F:\# Hudba')

#for p in range(len (path_list)):
#    print (path_list[p],path_dict[path_list[p]][0],approximate_size(path_dict[path_list[p]][1],False))

from operator import itemgetter

temp_p = []
for e in path_dict:
    temp_p.append([e,str.lower(e),path_dict[e][0],path_dict[e][1],path_dict[e][2]])
'''print ()
temp_p.sort(key=itemgetter(1))
for e in range(len(temp_p)):
    print (temp_p[e][0],temp_p[e][1],temp_p[e][2],temp_p[e][3])'''
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
print ('Seřaď podle velikosti:')
temp_p.sort(key=itemgetter(3))
for e in temp_p:
    print (e[0],path_dict[e[0]][0],approximate_size(path_dict[e[0]][1],False),path_dict[e[0]][2])
print ()
print ('Seřaď podle počtu adresářů:')
temp_p.sort(key=itemgetter(4))
for e in temp_p:
    print (e[0],path_dict[e[0]][0],approximate_size(path_dict[e[0]][1],False),path_dict[e[0]][2])

'''
for p in sorted(path_list,key=str.lower):
    print (p,path_dict[p][0],approximate_size(path_dict[p][1],False),path_dict[p][2])
    #vypíše cestu, počet souborů, součet jejich velikostí

#print (path_dict)
#files[f]

for p in path_list:
    extention = os.path.splitext(p)[1]
    #print (extention)

for p in path_list:
    #print (p)
    for f in files_list:
        name = f[1]
        name = os.path.splitext(f[1])[0]
        #name = os.path.splitext(os.path.join(f[0],f[1]))[0]
        extention = os.path.splitext(f[1])[1]
        #extention = os.path.splitext(os.path.join(f[0],f[1]))[1]
        size = files_dict[os.path.join(f[0],f[1])].st_size
        if p == f[0]:
            #print (name,extention,approximate_size(size,False))
            a=1
        i=0
        for e in extentions_list:
            if extention == e: i = 1
        if i == 0:
            extentions_list.append(extention)
            extentions_dict[extention] = [0,0]

for f in files_list:
        name = f[1]
        name = os.path.splitext(f[1])[0]
        #name = os.path.splitext(os.path.join(f[0],f[1]))[0]
        extention = os.path.splitext(f[1])[1]
        #extention = os.path.splitext(os.path.join(f[0],f[1]))[1]
        size = files_dict[os.path.join(f[0],f[1])].st_size
        extentions_dict[extention][0] += 1
        extentions_dict[extention][1] += size
'''  

print ()
for sp in sorted(superpath_list,key=str.lower):
    print (sp,superpath_dict[sp][0],approximate_size(superpath_dict[sp][1],False),superpath_dict[sp][2])

temp_e = []
for e in extentions_dict:
    temp_e.append([e,str.lower(e),extentions_dict[e][0],extentions_dict[e][1]])
'''print ()
temp_e.sort(key=itemgetter(1))
for e in range(len(temp_e)):
    print (temp_e[e][0],temp_e[e][1],temp_e[e][2],temp_e[e][3])'''
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
'''for e in sorted(extentions_dict,key=itemgetter(2)):
    print (e,extentions_dict[e][0],extentions_dict[e][1])
    #print (e,extentions_dict[e][0],approximate_size(extentions_dict[e][1],False))'''

print ()
print ('Konec...',files_all,approximate_size(size_all,False))
#print ('Konec...',files_all,approximate_size(size_all,False),approximate_size(size_all/files_all,False)) - vypíše i průměr

a = ""

while a.strip(" ").lower()!="n":
    a = input("Vložte cestu (N/n=konec):").strip(" ")
    pattern = "^M?M?M?(CM|CD|D?C?C?C?)(XC|XL|L?X?X?X?)(IX|IV|V?I?I?I?)$"
    if not(re.search(pattern,a)) or a=="":
        if a.lower()!="n": print("Toto není platné římské číslo")
        if a.lower()=="n": print("Konec")
    else:
        print_all("D:\\")
