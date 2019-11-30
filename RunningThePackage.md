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

Note that the scripts in the base directory are divided between "debug_*.py" and "run_*.py"
scripts. The debug versions are for development use.

The recommended way to work with this package is via the "UTC Logs". (The original version
used the log file "output_log.txt".)

- **run_1_fetch_UTC_logs.py** Copies the "UTC logs" to the "UTC_logs" sub-directory. You may 
need to patch the directory used if different, or work around read/write permissions.

- **run_2_parse_UTC_logs.py** Once the UTC logs are copies into the UTC_logs sub-directory,
they are parsed, and the draw database ("draw_database.txt"). Analysis tools work on this
text database (";"-delimited file).

- **run_3_create_summary.py** Builds a summary of the various statistical tests based on
the draw database.

There are other scripts, but for more advanced operations. For example, a land draw database
can be created (but currently no statistical tests developed).

The parsing script is most likely to fail due to log file format changes. However, once the
parsing is complete, the remaining code should work with the draw database, which should 
have a more stable format.

If users are unable to access the "UTC logs", will need to add back support for output_log.txt.


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
