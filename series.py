#!/usr/bin/env python
import os
import sys
import dircache
import getopt

__author__ = "Fernando Sanchez Villaamil"
__copyright__ = "Copyright 2012, Fernando Sanchez Villaamil"
__credits__ = ["Fernando Sanchez Villaamil"]
__license__ = "MIT"
__version__ = "1.1"
__maintainer__ = "Fernando Sanchez Villaamil"
__email__ = "nano@moomug.com"
__status__ = "Completed the desired functionality."

EXTENSIONS = ['.avi','.mpg','.mpeg','.ogg','.ogm','.mkv']
HOME = os.environ['HOME']
INSTALLATION_FOLDER = HOME + '/.series'
DIRECTORY_FILE = INSTALLATION_FOLDER + '/directory.txt'
GLOBAL_PROGRAM = INSTALLATION_FOLDER + '/program.txt'
MORE_INFO_MSG = 'Try option \'-h\' for more information.'

def install():
    print 'Generating configuration file...'
    HOME = os.environ['HOME']
    INSTALLATION_FOLDER = HOME + '/.series'
    programtxt = INSTALLATION_FOLDER + '/program.txt'
    if not os.path.exists( INSTALLATION_FOLDER ):
        os.mkdir( INSTALLATION_FOLDER )
    programtxt = open( programtxt, 'w' )
    program = raw_input('What program should be used to view videos? (Give ' + \
                        'the name which you call the program with):')
    programtxt.write( program.strip() )
    print 'Preference saved'
    return

def print_help():
    print '\'series\' program to view the chapters of a series in order\n' + \
          'Options:\n' + \
          '-d --directory [path]    Sets the directory where the chapters to be \n' + \
          '                         played are.\n' + \
          '-r --restart             Makes the program to start showing the \n' + \
          '                         chapters from the beginning again.\n' + \
          '-i --install             (Re)Installs the program, i.e. lets you \n' + \
          '                         choose the program to view videos and creates\n' + \
          '                         \'$HOME/.series/program.txt\'.\n' + \
          '-s --set [number]        Sets the next chapter to be viewed to \n' + \
          '                         [number] and exits.\n' + \
          '-b --back                Sets the next chapter to be viewed to the \n' + \
          '                         last viewed and exits.\n' + \
          '-c --current             Show current directory from which the chapters \n' + \
          '                         are currently loaded.\n' + \
          '-e --episode             Print the last played episode and the total number of \n' + \
          '                         episodes\n' + \
          '-v --version             Print the version and the copyright notice.\n' + \
          '-h --help                Prints this message.'

if __name__ == '__main__':
    # Process arguments. This will produce an error already on wrongly
    # formated arguments even though the arguments are not actually
    # used until after the whole internal state of the program was
    # initialized.
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'd:ris:bcevh', ['directory=',
                                                                'restart',
                                                                'install',
                                                                'set=',
                                                                'back',
                                                                'current',
                                                                'episode',
                                                                'version',
                                                                'help'])
    except getopt.GetoptError as err:
        print(err)
        print MORE_INFO_MSG
        sys.exit(2)

    # This program will only accept two arguments max in any case.
    if len(sys.argv[1:]) > 2:
        print 'Error, too many Arguments!'
        print MORE_INFO_MSG
        sys.exit(2)

    # If the program was called with one of the arguments that don't
    # require state, check now and do that.
    for o, a in opts:
        if o in ("-h", "--help"):
            print_help()
            exit()
        elif o in ("-v", "--version"):
            print 'series v' + __version__
            print 'Copyright (C) Fernando Sanchez Villaamil 2012'
            exit()

    # Check if already installed, if not, start installation.
    if not os.path.exists(INSTALLATION_FOLDER) or \
       not os.path.exists(GLOBAL_PROGRAM):
        install()
        exit()

    for o, a in opts:
        if o in ("-d", "--directory"):
            if not os.path.exists( sys.argv[2] ):
                print 'The given path(\'' + sys.argv[2] + '\') with the ' + \
                      'videos does not exist. Aborting.'
            else:
                directory_file = open(DIRECTORY_FILE, 'w')
                directory_file.write( os.path.abspath(sys.argv[2]) )
            exit()

    # Check if a directory was provided.
    if not os.path.exists(DIRECTORY_FILE):
        print 'Error: No directory containing episodes was provided.'
        print 'Call the program with option \'-d\' to provide one.'
        print MORE_INFO_MSG
        exit()

    directory_file = open(DIRECTORY_FILE, 'r')
    directory = directory_file.readline().strip()

    lastchaptertxt = directory + '/lastchapter.txt'

    # Initialize program's internal state.
    
    # Try to load the program that is to be used. First it looks for a
    # 'program.txt' file in the folder where series was called. If not
    # found, it searches for '$HOME/.series/program.txt'.
    if os.path.exists(directory + '/program.txt'):
        program = file(directory + '/program.txt')
    else:
        program = file(GLOBAL_PROGRAM)
    program = program.readline().strip()

    if not os.path.exists( directory + '/lastchapter.txt' ):
        newFile =  open(directory + '/lastchapter.txt', 'w' )
        newFile.write('0')
        newFile.close()

    content = dircache.listdir(directory)

    videos = []
    for extension in EXTENSIONS:
        videos.extend(filter(lambda x: x.endswith(extension), content))
    videos = sorted(videos)

    lastchapter = file( directory + '/lastchapter.txt' )
    chapter = int(lastchapter.readline())

    for o, a in opts:
        if o in ("-r", "--restart"):
            newFile =  open(lastchaptertxt, 'w' )
            newFile.write('0')
            newFile.close()
            chapter = 0
        elif o in ("-i", "--install"):
            install()
            exit()
        elif o in ("-s", "--set"):
            try:
                chapter = int(sys.argv[2]) - 1
            except:
                print 'The Argument of \'' + o +'\' must be a number.'
                print MORE_INFO_MSG
                exit()
            newFile =  open(lastchaptertxt, 'w' )
            newFile.write( str(chapter) )
            newFile.close()
            exit()
        elif o in ("-b", "--back"):
            lastchapter = file( lastchaptertxt )
            chapter = lastchapter.readline()
            lastchapter.close()
            chapter = int(chapter)
            if  chapter > 0:
                newFile =  open(lastchaptertxt, 'w' )
                newFile.write( str(chapter - 1) )
                newFile.close()
            exit()
        elif o in ("-c", "--current"):
            print 'Currently playing directory: ' + directory
            exit()
        elif o in ("-e", "--episode"):
            print 'Last episode played: ' + \
                  str(chapter) + '/' + str(len(videos))
            exit()
        else:
            assert False, "unhandled option"

    if chapter >= len(videos):
        print 'No more chapters left in \'' + directory +'\' :('
        exit()
    
    chapter_out_of = str(chapter) + '/' + str(len(videos))
    print 'Loading chapter ' + chapter_out_of + ' in folder \'' + directory + \
          '\'...'
    
    newFile =  open(lastchaptertxt, 'w' )
    newFile.write( str(chapter + 1) )
    newFile.close()

    print program + ' \'' + directory + '/' + videos[chapter] + '\''
    os.system(program + ' \'' + directory + '/' + videos[chapter] + '\'')

