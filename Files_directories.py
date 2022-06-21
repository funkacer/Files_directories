import os
import _ctypes
import time
import datetime
import sys

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


def di(obj_id):
    """ Inverse of id() function. """
    return _ctypes.PyObj_FromPtr(obj_id)

'''
if __name__ == '__main__':
    a = 42
    b = 'answer'
    print(di(id(a)))  # -> 42
    print(di(id(b)))  # -> answer
'''

class Element():

    def get_path(self):
        return self._path

    def get_elements(self):
        return self._elements

    def get_name(self):
        return self._name

    def get_count(self):
        return self._count

    def get_size(self):
        return self._size

    def get_extension(self):
        return self._extension

    def get_subdirs(self):
        return self._subdirs

    def get_files(self):
        return self._files


class File(Element):

    def __init__(self, name):
        self._name = name
        self._count = 1 # file is 1
        self._elements = [] #file has no elements

    def compute_stats(self, max = 0, i = 0):
        self._path = os.path.realpath(self._name)
        metadata = os.stat(self._name)
        self._size = metadata.st_size
        self._extention = os.path.splitext(self._name)[1]
        return max, i

    def print_all_elements(self):
        if isinstance(self, Directory):
            print("DIR", self.get_name(), id(self), di(id(self)))
        else:
            print("FILE", self.get_name(), id(self), di(id(self)))

    def get_all_elements(self):
        return [self]


class Directory(Element):

    def __init__(self, name):
        self._name = name
        self._count = None  #must be computet
        self._size = None  #must be computet
        self._all_subdirs = None
        self._subdirs = None
        self._files = None
        self._elements = []

    def toolbar(self, max, i):
        if i % int(max/100+1) == 0:
            #time.sleep(.1)
            sys.stdout.write(u"\u001b[1000D" +  "Processed: " + str(i) + "/" + str(max) + " (" + str(int(i/max*100)) + "%)" )
            sys.stdout.flush()
        elif i == max:
            sys.stdout.write(u"\u001b[1000D" +  "Processed: " + str(i) + "/" + str(max) + " (" + str(int(i/max*100)) + "%)" )
            sys.stdout.flush()
            time.sleep(1)
            print()

    def add_element(self, element):
        self._elements.append(element)

    def get_elements(self):
        elements = self._elements
        return elements

    def print_all_elements(self):
        if isinstance(self, Directory):
            print("DIR", self.get_name(), id(self), di(id(self)))
        else:
            print("FILE", self.get_name(), id(self), di(id(self)))
        for e in self.get_elements():
            e.print_all_elements()

    def get_all_elements(self):
        e = []
        e.append(self)
        for el in self.get_elements():
            for ell in el.get_all_elements():
                e.append(ell)
        return e

    def get_all_directories_by_name(self):
        e = []
        if isinstance(self, Directory): e.append(self)
        for el in self.get_elements():
            for ell in el.get_all_elements():
                if isinstance(ell, Directory): e.append(ell)
        d = {}
        for e in e:
            d[e.get_name()] = e
        e = [d[e] for e in sorted(d.keys())]
        return e

    def compute_stats(self, max = 0, i = 0):
        if i == 0: max = self.get_count()
        for e in self.get_elements():
            max, i = e.compute_stats(max, i)
            if isinstance(e, File):
                i += e.get_count()
                self.toolbar(max, i)
        return max, i

    def get_count(self):
        if self._count is None:
            count = 0
            for e in self._elements:
                count += e.get_count()
            self._count = count
        return self._count

    def get_size(self):
        if self._size is None:
            size = 0
            for e in self._elements:
                size += e.get_size()
            self._size = size
        return self._size

    def get_all_subdirs(self):
        if self._all_subdirs is None:
            count = 0
            for el in self._elements:
                for ell in el.get_all_elements():
                    if isinstance(ell, Directory): count += 1
            self._all_subdirs = count
        return self._all_subdirs

    def get_subdirs(self):
        if self._subdirs is None:
            count = 0
            for el in self._elements:
                if isinstance(el, Directory): count += 1
            self._subdir = count
        return self._subdir

    def get_files(self):
        if self._files is None:
            count = 0
            for el in self._elements:
                if isinstance(el, File): count += 1
            self._files = count
        return self._files


def scan_all (path, previous_directory, max = 0):
    #dirs = [(os.path.realpath(entry.name)) for entry in os.scandir(path) if not entry.name.startswith('.') and entry.is_dir()]
    if not "D:\\$RECYCLE.BIN" in path and not "D:\\System Volume Information" in path:

        files = [(entry.path) for entry in os.scandir(path) if entry.is_file()]
        for f in files:
            file = File(f)
            previous_directory.add_element(file)

        max += len(files)
        sys.stdout.write(u"\u001b[1000D" +  "Files: " + str(max))
        sys.stdout.flush()

        dirs = [(entry.path) for entry in os.scandir(path) if entry.is_dir()]

        for d in dirs:
            directory = Directory(d)
            previous_directory.add_element(directory)
            max = scan_all (d, directory, max)

        return max

def main():

    path = os.getcwd()
    parent_directory = Directory(path)
    print ('Start...')
    start = time.perf_counter()
    max = scan_all(path, parent_directory)
    sys.stdout.write(u"\u001b[1000D" +  "Files: " + str(max))
    sys.stdout.flush()
    print()
    end = time.perf_counter()
    print("Elapsed time scan_all: " + str(datetime.timedelta(seconds=end-start)))

    start = time.perf_counter()
    max, i = parent_directory.compute_stats()
    assert max == i, "Not all astats computed"
    end = time.perf_counter()
    print("Elapsed time compute_stats: " + str(datetime.timedelta(seconds=end-start)))

    print("Files:", parent_directory.get_count())
    print("Size:", parent_directory.get_size())


    temp = [[e.get_name(), str(e.get_count()), str(e.get_size()), approximate_size(e.get_size()), str(e.get_all_subdirs()), str(e.get_files()), str(e.get_subdirs())] for e in parent_directory.get_all_directories_by_name()]

    end = time.perf_counter()
    print("Elapsed time get_all_directories_by_name: " + str(datetime.timedelta(seconds=end-start)))

    filename = path.split(os.sep)[-1] + ".txtx"
    print(f'Filename to create: {filename}')
    #temp_p.sort(key=itemgetter(2), reverse = True)
    with open (filename, mode = "w", encoding = "utf-8") as f:
        a = ""
        columns = ["Directory", "Total files", "Total size", "Approximate size", "Total subdirs", "Files in folder", "Dirs in folder"]
        a += "\t".join([c for c in columns]) + "\n"
        for element in temp:
            #print (e[0],path_dict[e[0]][0],approximate_size(path_dict[e[0]][1],False),path_dict[e[0]][2])
            a += "\t".join([e for e in element]) + "\n"
        f.write(a)

if __name__ == "__main__":
    main()
