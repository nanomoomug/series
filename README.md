series
======

A small program to ease the viewing of ordered series of videos.

This program is a quick and dirty python script, but it should work in
UNIX like environments.

To install it you just have to put it into your $PATH
environment. E.g., if you are using Ubuntu: Assume you have downloaded
and unpacked the program to <unpacked-program>. Then you can do the
following:

> cd /usr/bin

> sudo ln -sv <unpacked-program>/series.py series

Now the program can be called with the command 'series'. 

On the first run the program will install itself into your home
directory. For this it will ask you which program you want to use to
view the video.

You configure it by giving it a directory where the chapters of the
series are. The program assumes that correct order of the chapters is
the same as the lexicographical order of video files. Then every time
the program is called, it will look for the next chapter and play it
with the specified program. E.g.: Assume that the chapters of the
series you want to watch are contained in the directory
<chapter-of-series>. Then you can either do:

> series -d \<chapter-of-series\>

or

> cd <chapter-of-series>

> series -d .

which I find more comfortable. Then by using the command 

> series

in any directory, the next episode will be played.

For more options call it with '-h'.
