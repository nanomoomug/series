#!/usr/bin/env python
import os
import sys
import dircache
import getopt

def install():
    print 'Generating configuration file...'
    HOME = os.environ['HOME']
    INSTALLATION_FOLDER = HOME + '/.series'
    programtxt = INSTALLATION_FOLDER + '/program.txt'
    if not os.path.exists( INSTALLATION_FOLDER ):
        os.mkdir( INSTALLATION_FOLDER )
    programtxt = open( programtxt, 'w' )
    program = raw_input( 'What program should be used to view videos? (Give the name which you call the program with):' )
    programtxt.write( program.strip() )
    print 'Preference saved'
    return

def print_help():
    print '\'series\' program to view the chapters of a series in order v1.0\n' + \
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
          '-h --help                Prints this message.'

if __name__ == '__main__':
    HOME = os.environ['HOME']
    INSTALLATION_FOLDER = HOME + '/.series'
    DIRECTORY_FILE = INSTALLATION_FOLDER + '/directory.txt'

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'd:ris:bch', ['directory=',
                                                               'restart',
                                                               'install','set=',
                                                               'back','current',
                                                               'help'])
    except getopt.GetoptError as err:
        print(err)
        print_help()
        sys.exit(2)

    # This program will only accept two arguments max in any case.
    if len(sys.argv[1:]) > 2:
        print 'Error, too many Arguments!'
        print 'Try option \'-h\' for more information.'
        sys.exit(2)

    DIRECTORY_FILE = open(DIRECTORY_FILE, 'r')
    directory = DIRECTORY_FILE.readline().strip()
    lastchaptertxt = directory + '/lastchapter.txt'

    for o, a in opts:
        if o in ("-h", "--help"):
            print_help()
            sys.exit()
        elif o in ("-d", "directory"):
            if not os.path.exists( sys.argv[2] ):
                print 'The given path(\'' + sys.argv[2] + '\') with the videos does not seem to exist. Aborting.'
            else:
                HOME = os.environ['HOME']
                INSTALLATION_FOLDER = HOME + '/.series'
                DIRECTORY_FILE = INSTALLATION_FOLDER + '/directory.txt'
                DIRECTORY_FILE = open(DIRECTORY_FILE, 'w')
                DIRECTORY_FILE.write( os.path.abspath(sys.argv[2]) )
            exit()
        elif o in ("-r", "restart"):
            # This will force the program to restart.
            os.remove(lastchaptertxt)
        elif o in ("-i", "install"):
            install()
            exit()
        elif o in ("-s", "set"):
            newFile =  open(lastchaptertxt, 'w' )
            try:
                chapter = int(sys.argv[2]) - 1
            except:
                print 'The Argument must be a number. Use \'--help\' for help.'
                exit()
            newFile.write( str(chapter) )
            newFile.close()
            exit()
        elif o in ("-b", "back"):
            lastchapter = file( lastchaptertxt )
            chapter = lastchapter.readline()
            lastchapter.close()
            chapter = int(chapter)
            if  chapter > 0:
                newFile =  open(lastchaptertxt, 'w' )
                newFile.write( str(chapter - 1) )
                newFile.close()
            exit()
        elif o in ("-c", "current"):
            print 'Currently playing directory: ' + directory
            exit()
        else:
            assert False, "unhandled option"

    # Play the next chapter.
    if not os.path.exists(directory):
        videosDirectory = raw_input( 'No directory with videos given. Type directory with the videos:' )
        DIRECTORY_FILE = open(DIRECTORY_FILE, 'w')
        DIRECTORY_FILE.write( os.path.abspath(videosDirectory))

    print 'Loading next chapter in folder \'' + directory + '\'...'

    # Try to load the program that is to be used. First it looks for a
    # 'program.txt' file in the folder where series was called, if not
    # found is searches for '$HOME/.series/program.txt'.  If the
    # configuration file '$HOME/.series/program.txt' does not exist it
    # asks the user what program he wants to use and creates this file.
    if os.path.exists( directory + '/program.txt' ):
        program = file( './program.txt' )
    else:
        program = os.environ['HOME'] + '/.series/program.txt'
        if not os.path.exists( program ):
            install()
        program = file( program )
    program = program.readline().strip()

    if not os.path.exists( directory + '/lastchapter.txt' ):
        newFile =  open(directory + '/lastchapter.txt', 'w' )
        newFile.write( '0' )
        newFile.close()


    content = dircache.listdir(directory)

    extensions = ['.avi','.mpg','.mpeg','.ogg','.ogm','.mkv']

    videos = []
    for extension in extensions:
        videos.extend(filter(lambda x: x.endswith(extension), content))

    videos = sorted(videos)

    lastchapter = file( directory + '/lastchapter.txt' )
    chapter = lastchapter.readline()

    chapter = int(chapter)
    if chapter < len(videos):
        newFile =  open(directory + '/lastchapter.txt', 'w' )
        newFile.write( str(chapter + 1) )
        newFile.close()

        print program + ' \"' + directory + '/' + videos[chapter] + '\"'
        os.system(program + ' \"' + directory + '/' + videos[chapter] + '\"')
    else:
        print "No more chapters left :("
