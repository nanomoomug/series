#!/usr/bin/env python
import os
import sys
import dircache

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

if len(sys.argv) > 1:
    if ( sys.argv[1] == '-r' or sys.argv[1] == '--restart' ) and os.path.exists( './lastchapter.txt' ):
        if len(sys.argv) > 2:
            print 'Too many arguments. Use \'--help\' for help.'
            exit()
        os.remove(lastchaptertxt)
    elif sys.argv[1] == '-i' or sys.argv[1] == '--install':
        if len(sys.argv) > 2:
            print 'Too many arguments. Use \'--help\' for help.'
            exit()
        install()
        exit()
    elif sys.argv[1] == '-s' or sys.argv[1] == '--set':
        if len(sys.argv) != 3:
            print 'Wrong use of \'-s\' or \'--set\'. Use \'--help\' to see correct use.'
        else:
            newFile =  open(lastchaptertxt, 'w' )
            try:
                chapter = int(sys.argv[2]) - 1
            except:
                print 'The Argument must be a number. Use \'--help\' for help.'
                exit()
            newFile.write( str(chapter) )
            newFile.close()
        exit()
    elif sys.argv[1] == '-b' or sys.argv[1] == '--back':
        if len(sys.argv) > 2:
            print 'Too many arguments. Use \'--help\' for help.'
        else:
            lastchapter = file( lastchaptertxt )
            chapter = lastchapter.readline()
            lastchapter.close()
            chapter = int(chapter)
            if  chapter > 0:
                newFile =  open(lastchaptertxt, 'w' )
                newFile.write( str(chapter - 1) )
                newFile.close()
        exit()
    elif sys.argv[1] == '-d' or sys.argv[1] == '--directory':
        if len(sys.argv) != 3:
            print 'Wrong use of \'' + sys.argv[1] + '\'. Use \'--help\' to see correct use.'
        elif not os.path.exists( sys.argv[2] ):
            print 'The given path(\'' + sys.argv[2] + '\') with the videos does not seem to exist. Aborting.'
        else:
            HOME = os.environ['HOME']
            INSTALLATION_FOLDER = HOME + '/.series'
            DIRECTORY_FILE = INSTALLATION_FOLDER + '/directory.txt'
            DIRECTORY_FILE = open(DIRECTORY_FILE, 'w')
            DIRECTORY_FILE.write( os.path.abspath(sys.argv[2]) )
        exit()
    elif sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print 'This is the \'series\' program to view the chapters of a serie automatically in order v1.0'
        print 'Options:'
	print '-d --directory [path]    Sets the directory where the chapters to be played are.'
        print '-r --restart      \t Makes the program to start showing the chapters from the beginning again.'
        print '-i --install      \t (Re)Installs the program, i.e. lets you choose the program to view videos and creates \'$HOME/.series/program.txt\'.'
        print '-s --set [number] \t Sets the next chapter to be viewed to [number] and exits.'
        print '-b --back         \t Sets the next chapter to be viewed to the last viewed and exits.'
        print '-h --help         \t Prints this message.'
        exit()

if __name__ == '__main__':
    HOME = os.environ['HOME']
    INSTALLATION_FOLDER = HOME + '/.series'
    DIRECTORY_FILE = INSTALLATION_FOLDER + '/directory.txt'
    
    if not os.path.exists(INSTALLATION_FOLDER) or (len(sys.argv) > 1 and (sys.argv[1] == '-i' or sys.argv[1] == '--install')):
        if len(sys.argv) > 2:
            print 'Too many arguments. Use \'--help\' for help.'
            exit()
        install()
        exit()

    if not os.path.exists(DIRECTORY_FILE):
        videosDirectory = raw_input( 'No directory with videos given. Type directory with the videos:' )
        DIRECTORY_FILE = open(DIRECTORY_FILE, 'w')
        DIRECTORY_FILE.write( os.path.abspath(videosDirectory))

    DIRECTORY_FILE = open(DIRECTORY_FILE, 'r')
    directory = DIRECTORY_FILE.readline().strip()
    lastchaptertxt = directory + '/lastchapter.txt'
    
    print "Searching for Next Chapter..."

    # Try to load the program that is to be used. First it looks for a
    # 'program.txt' file in the folder where series was called, if not
    # found is searches for '$HOME/.series/program.txt'.  If the
    # configuration file '$HOME/.series/program.txt' does not exist it
    # asks the user what program he wants to use and creates this file.
    if os.path.exists( './program.txt' ):
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

    def suffix( extension ):
        def f(x): return x.endswith(extension)
        return f

    extensions = ['.avi','.mpg','.mpeg','.ogg','.ogm','.mkv']

    videos = []
    for i in extensions:
        videos.extend( filter( suffix(i) , content ) )

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


    
