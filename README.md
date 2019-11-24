# arena_log_parser
MTG Arena Log Parser

Python MTG Arena log parser.

Use at own risk; no warranty of any kind provided.

Since all the code does is read some text files and writes other ones, you really would need to
take a lot of effort to break things.

See "process_log.py" for instructions...

Initial test described in aggregate30.py

# What's Changed

- Mulligan tracking fixed.
- Archive script.
- Initial stab at Brawl/Singleton test. (Works for Singleton, not sure whether Brawl can be 
detected.)

# TODO

- Bo3 modes.
- More information on game: event type, opponent, gameplay time stamp.
- Aggregation for other tests (Brawl, ...)
- Card database: map the card code to card data, most importantly, land/nonland status.
- Automation. (Current project does not touch anything outside local directories.)
- Script to aggregate individual summaries.
- Script to rebuild draws.txt from archive.
- For somebody else: can data be aggregated automatically on some central point?
