import os, shutil, sys
from config import main_folder

def pwf():
    global current_directory
    print('/'+'/'.join(current_directory[1:]))


def path_reader(path, mode = True):
    global current_directory
    path = [item  for el in path.split('\\') for item in el.split('/')]
    if path[0] == '.':
        path = list(current_directory + path[1:])
    elif path[0] == '..':
        if len(current_directory) > 1:
            path = list(current_directory[:-1] + path[1:])
        else:
            path = list(current_directory + path[1:])
    elif path[0] == '':
        path[0] = main_folder
    else:
        path = list(current_directory + path)
    secondary = '/'+'/'.join(path[1:]) if mode else path
    return os.path.join(*path), secondary


def mkfld(*names, recursive = False):
    for name in names:
        path = path_reader(name)
        try:
            os.makedirs(path[0]) if recursive else os.mkdir(path[0]) 
        except FileExistsError:
            print(f'Directory has already exist: {path[1]}')
        except FileNotFoundError:
            print(f'Invalid path: {path[1]}')


def mkflds(*names):
    mkfld(*names, recursive = True)


def rmfld(*names, recursive = False):
    for name in names:
        path = path_reader(name)
        try:
            if recursive:
                tree = list(os.walk(path[0]))[::-1]
                for objects in tree:
                    for item in objects[1]:
                        os.rmdir(os.path.join(objects[0],item))
                    for item in objects[2]:
                        os.remove(os.path.join(objects[0],item))
                os.rmdir(objects[0])
            else:
                os.rmdir(path[0])
        except FileNotFoundError:
            print(f'Invlid path {path[1]}')
        except OSError:
            print(f'Folder isn\'n empty {path[1]} (use rmflds)')


def rmflds(*names):
    rmfld(*names, recursive = True)


def gtf(name):
    global current_directory
    path = path_reader(name, mode = False)
    if os.path.exists(path[0]):
        current_directory = list(path[1])
    else:
        print('No such file or directory')


def crtfl(*names):
    for name in names:
        path = path_reader(name)
        try:
            with open(path[0], 'x'):
                pass
        except FileExistsError:
            pass


def wrtfl(name):
    path = path_reader(name)
    print("Ctrl-Z (Windows) or Ctrl-D (Unix) for close")
    try:
        with open(path[0], 'a') as file:
            while True:
                try:
                    file.write(input()+'\n')
                except EOFError:
                    break
    except FileExistsError:
        print(f'File doesn\'t exist {path[1]}')


def rdfl(*names):
    for name in names:
        path = path_reader(name)
        try:
            with open(path[0], 'r') as file:
                    for line in file.readlines():
                        print(line, end = '')
        except FileExistsError:
            print(f'File doesn\'t exist {path[1]}')


def rmfl(*names):
    for name in names:
        path = path_reader(name)
        try:
            os.remove(path[0])
        except FileNotFoundError:
            print(f'Invlid path {path[1]}')


def cpflfd(from_,to_):
    from_ = path_reader(from_)
    to_ = path_reader(to_)
    if sys.platform == 'win32':
        os.system(f'copy "{from_[0]}" "{to_[0]}"')
    else:
        os.system(f'cp -r {from_[0]} {to_[0]}')

def rpls(from_, to_):
    from_ = path_reader(from_)
    to_ = path_reader(to_)
    try:
        os.replace(from_[0], to_[0])
    except FileNotFoundError:
        print(f'Invlid path {from_[1], to_[1]}')


def rnm(name, new_name):
    name = path_reader(name)
    new_name = path_reader(new_name)
    try:
        os.rename(name[0], new_name[0])
    except FileNotFoundError:
        print(f'Invlid path {name[1], new_name[1]}')


def print_help_string():
    help_string = r''''pwf' -- Print work folder
'mkfld [folder_name] [folder_name] ..' -- Make folders
'mkflds [folder_name] [folder_name] ..' -- Make folders recursive
'rmfld [folders_name] [folder_name] ..' -- Remove folders
'rmflds [folder_name] [folder_name] ..' -- Remove folders recursive
'gtf [folder_name]' -- go to folder, changes current folder
'crtfl [file_name] [file_name] ..' -- create files
'wrtfl [file_name]' -- write to file, stream string input
'rdfl [file_name] [file_name] ..' -- displays files
'rmfl [file_name] [file_name] ..' -- remove files
'cpflfd [file_from] [file_to]' -- copy file_name to folder/new_file
'rpls [file_folder] [file_folder]' -- replace file/folder to other file/folder
'rnm [file_folder]' -- rename file or folder
'exit' -- to exit
'help' -- to get command list'''
    print(help_string)

def command_prompt():
    global current_directory
    commands = {
        'pwf':pwf,
        'mkfld':mkfld,
        'mkflds':mkflds,
        'rmfld':rmfld,
        'rmflds':rmflds,
        'gtf':gtf,
        'crtfl':crtfl,
        'wrtfl':wrtfl,
        'rdfl':rdfl,
        'rmfl':rmfl,
        'cpflfd':cpflfd,
        'rpls':rpls,
        'rnm':rnm,
        'help':print_help_string
    }

    while True:
        command = input('CommandPrompt:/'+'/'.join(current_directory[1:])+'$ ').split()
        if command[0] == 'exit':
            break
        try:
            commands[command[0]](*command[1:])
        except KeyError:
            print('Invalid command. Use "help" to see command list')
        except PermissionError:
            print('Permission denied')


current_directory = [main_folder]
command_prompt()