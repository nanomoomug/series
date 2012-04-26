series
======

A small program to ease the viewing of ordered series of videos.

This program is a quick and dirty python script, but it should work in
UNIX like environments.

To install it you just have to put it into your $PATH environment.

On the first run the program will install itself into your home
directory. For this it will ask you which program you want to use to
view the video.

You configure it by giving it a directory where the chapters of the
series are. Then every time the program is called, it will look for the
next chapter and play it with the specified program.

For more options call it with '-h'.