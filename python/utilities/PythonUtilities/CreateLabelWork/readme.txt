Tool for distributing labeling work to humans.

usage: create_work.py [-h] --tsv TSV --vols VOLS

Assigns a set of volumes to different workers for tagging

arguments:
  -h, --help   show this help message and exit
  --tsv TSV    The master TSV file
  --vols VOLS  The ZIP file containing the volumes referenced by the TSV file

Example invocation:
   > create_work.py --tsv master1.tsv --vols volumes1.zip

The tool uses 2 configuration files:
config.ini
	- lives in the same folder as the create_work.py script 
	- contains general config parameters in the [config] section
	- see config.ini.sample in this folder for details

~/.genreproject.ini
	- lives in the user's HOME folder
	- contains private configuration parameters for the [remote] config section
	- see genreproject.ini.sample in this folder for required parameters

The arff.template file is also required to be present in the same folder where the python script and config.ini files are found.
