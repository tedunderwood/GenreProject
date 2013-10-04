Build Instructions:

In addition to placing both the backend and gui directories into your source directory,
you'll need to include the two external jar's referenced by the browser's classes in
your build path. Derby.jar and commons-compress-1.5.jar should be here on the project
repo, but if not they're both from Apache projects. 

I'm not very familiar with MAVEN, but since Boris has previously suggested it I put together a very basic definition file in Eclipse that makes note of the derby.jar and commons-compress-1.5.jar dependencies and identifies src/ as the source directory.

Change log:

10/3/13 - borice
Updated pom.xml and directory structure to adhere to maven best practices
Added ability to generate deployment jar with dependencies via 'mvn package'
Updated code to be Java 1.6 compatible

8/16/13 - mikeb
Updated browser executed jar
Added documentation to all classes
Added a very basic MAVEN definition (pom.xml) with derby/compress dependencies noted

8/9/13 - mikeb
NEW: PageMapper integrated into PrimaryWindow
NEW: Test version uploaded, see instructions for basic installation/user in zip
Backend classes have rough draft comments

8/6/13 - mikeb
NEW: VolumeReader class will loads processed volumes into memory, acts as interface
NEW: PageMapper class lets users assign genre codes to pages
TODO: PageMapper is not currently integrated into the browser GUI
TODO: Integrate VolumeReader & PageMapper into preferences to locate volume data and allowable genre codes file

7/12/13 - mikeb
MOVED: Migrated browser classes to "gui" package
NEW: RecordViewer class lets users see the complete metadata entry for a search result
NEW: Preferences class handles basic loading/saving of past sessions
NEW: PredictionTableModel class for handling display of prediction records
NEW: ResultsTableModel class for handling display of search results
NEW: "Load Source Records" button will add all predictions from source ARFF to target ARFF
NEW: New Derby database can be generated at start if none is found (or no previous session)
NEW: All tables created from predictions are dropped at program close

6/20/13 - mikeb
NEW: Initial browser commit
MOVED: Backend code has been updated and moved into the browser structure
Sparse comments for the time being.  Will write more documentation as code is revised.

6/5/13 - mikeb
NEW: Added a very basic ARFF class
DerbyDB: Fixed exception handling so errors will be thrown to GUI.
DerbyDB: Added indexing by author/title for faster retrieval.
DerbyDB: Added a return record method in anticipation of GUI.

6/3/13 - mikeb
For the time being, I'm going to store all of the classes I write to handle the data sources available to users of the browser tool in this folder.  Right now there is just the DerbyDB interface (and its dependency).  I will eventually setup Eclipse to handle git commits, so this folder will eventually be assimilated into the organization it prefers.
