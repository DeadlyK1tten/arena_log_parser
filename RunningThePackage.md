# Running The Parser

## Get Python!

The first thing is that you need a fairly up to date Python installation. https://www.python.org/

If you follow the default steps, you should be able to double-click a Python script (.py) and it runs.

Other ways of running a script
- On the command line. Go to the script directory (where this file is), and then type 
python scriptname.py (You may need to supply the full path to python.exe)
- Right-click the script, and select "edit with Idle" (a Python editor that is installed by 
default.) You can run from inside Idle, and see the output.
- Install a integrated development environment (IDE). Although more complex, probably
easier to integrate with GitHub.

## Get The Code Repository

You need to get a copy of *all* the files in the repository, and preserve the structure. The
working directory is the base directory where this file is placed.

You can get the files by downloading a zip file from GitHub, or learn how to use the git
source control system. (There is some kind of app for GitHub which may be enough.)

The code is found in the base directory, and the "parsercode" subdirectory. If there are any
updates, all the files in those directories need to be updated.

## Operating Steps

Detailed logging has to be turned on in the client settings. (Also needed for trackers.)

You then need to find the Arena log file file: output_log.txt. For me, it was under
c:\users\<name>\AppData\LocalLow\Wizards Of The Coast\MTGA\

Copy the log file to the base directory. (I have a bat file that does this; I keep this
package self-contained and not mucking around in external directories, so I leave that to 
you.)

Then, if you execute "process_log.py", the log file should be parsed.

- There will be a console window dumping a load of stuff.
- It will look for testing decks, and write draw information into "draws.txt." This file
is your draw database. 
- There is a log file "log.txt" which says what the script did.

You can then look at draws.txt, and see whether it picked up your data. Each row corresponds 
to a parsed draw. If you just run one or two tests in a session, you should sort-of figure
out what is happening.

(If you want to run the parsing without touching draws.txt, run process_log_debug.py. It 
writes to "draws_debug.txt" (which is overwritten each time). This allows you to see what is
parsed from a single output_log.txt.)

Once you are done with a file, run "archive.py". It will copy output_log.txt to the "archive"
directory, attaching a number to it. The process_archive.py script blasts through all those
files and writes the results to draws_debug.txt. So long as you keep your archive, all your game
logs can be re-processed (if there is a bug, or new feature).

# Troubleshooting

Pretty much anything can go wrong. Right now, I am just guessing.

- Scripts will do nothing if not using detailed Arena logs; see the Arena settings screen. 
- The python code files (such as decks.py, utils.py) have to be in the "parsercode" 
subdirectory.
- The file output_log.txt has to be in the same directory as process_log.py.
- Log file formats can vary, and I have not tested best-of-3 ("Traditional") at all.


If there is something wrong when parsing data, the scripts crash. That is because a crash
is better than writing corrupted data to draws.txt, or doing nothing (since trials will 
be lost, and nobody noticing).
