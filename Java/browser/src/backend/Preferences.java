package backend;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.nio.charset.Charset;
import java.util.ArrayList;

import javax.swing.JFileChooser;
import javax.swing.JOptionPane;

public class Preferences {
	/**
	 * The purposes of this class is to read, write, and hold application preferences.
	 * Essentially, anything that needs to be loaded from disk at runtime and passed 
	 * into any of the core components for configuration purposes is done by this class.
	 * Currently, it's primary tasks include:
	 * - providing the location of the derby database
	 * - keeping track of which seed file was used to create the derby database
	 * - remembering which genre codes file users selected (optional)
	 * 
	 * NOTE: Although not explicitly supported within the program, you can bypass the
	 * default pagemaps/ directory by editing the configuration file that Preferences
	 * loads and adding a pagemapdir= field.  Otherwise, Preferences will stick with
	 * the internal default (defined here, NOT IN PAGEMAPPER).
	 */
	
	private File prefsFile;
	public final static String DEFAULT_PREF_FILE = "genrebrowser.ini";
	private String derbyDir = null, genreCodes = null, pageMapDir = "pagemaps/"; 
	private String source;
	private String[][] generalCodes, pageCodes;
		
	public Preferences(String filename) {
		/**
		 * This constructor allows for alternate preference profiles. To use just the 
		 * default file (as PrimaryWindow does), call it as: 
		 * Preferences p = new Preferences(Preferences.DEFAULT_PREF_FILE).
		 * 
		 */
		prefsFile = new File(filename);
		while(derbyDir == null) {
			if (prefsFile.exists()) {
				try {
					readPrefs();
				} catch (IOException e) {
					JOptionPane.showMessageDialog(null, "Problem reading file. Please try again.\nExiting.","Loading Error",JOptionPane.ERROR_MESSAGE);
				}
			} else {
				// If the filename passed into the constructor isn't found, assume that 
				// this is a first-time run and run configuration sequence.
				System.out.println(filename + " does not exist. Creating new workspace.");
				firstTimeConfig();
			}
		}
	}
	
	private void readPrefs() throws IOException {
		/**
		 * Reads the selected preferences file from disk and parses its contents, setting
		 * the internal configuration variables to match the fields it finds.  Line input
		 * is parsed using a simple regex split and a String switch.
		 */
		ArrayList<String> rawtext = new ArrayList<String>();
		String line;
		BufferedReader lines = new BufferedReader(new FileReader(prefsFile));
		while((line = lines.readLine()) != null){
			rawtext.add(line.trim());
		}
		lines.close();
		for (int i=0;i<rawtext.size();i++) {
			if(rawtext.get(i) == "#PREFS") {
				continue;
			} else if (rawtext.get(i).length() > 1 && rawtext.get(i).indexOf("=") > 0) {
				String[] parts = rawtext.get(i).split("=");
				// Right now there are only four possible fields, but you could add more
				// by expanding this switch statement.
				switch(parts[0]) {
					case "databasedir":
						derbyDir = parts[1];
						break;
					case "sourcefile":
						source = parts[1];
						break;
					case "genrecodes":
						genreCodes = parts[1];
						break;
					case "pagemapdir":
						pageMapDir = parts[1];
						break;
				}

			}
		}
		System.out.println("Preferences loaded.");
		if(genreCodes != null) {
			// If users selected a genre codes file during a past session, retrieve it!
			System.out.println("Trying to load genre codes file.");
			readCodes();
		}
	}
	
	private void firstTimeConfig() {
		/**
		 * This method is a series of pop-up dialogs that ask users to configure the
		 * browser.  Right now, it only asks for a seed file and for a directory name
		 * for the local derby database.
		 */
		JOptionPane.showMessageDialog(null, "Please specify a seed file for the browser's database.","First Time Configuration",JOptionPane.OK_OPTION);
		JFileChooser seed = new JFileChooser(System.getProperty("user.dir"));
		seed.showOpenDialog(null);
		source = seed.getSelectedFile().getAbsolutePath();
		derbyDir = (String)JOptionPane.showInputDialog(null,"Choose a name for the browser's database:","First Time Configuration",JOptionPane.PLAIN_MESSAGE,null,null,null);
		derbyDir = new File(derbyDir).getAbsolutePath();
		
	}
	
	public void writePrefs() {
		/**
		 * Writes configuration settings to disk.  It will write to the same file that it
		 * read from initially, or in the case of a first-run to the filename passed into
		 * the constructor at creation.
		 */
		try {
			BufferedWriter output = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(prefsFile.getAbsolutePath()),"UTF-8"));
			output.write("#PREFS\n");
			output.write("databasedir=" + derbyDir + "\n");
			output.write("sourcefile=" + source + "\n");
			// If the pagemapdir was overrided by the current configuration file, remember it.
			if (!pageMapDir.equals("pagemaps/")) {
				output.write("pagemapdir=" + pageMapDir + "\n");
			}
			// If users selected a genre codes file, remember it.
			if (genreCodes != null) {
				output.write("genrecodes=" + genreCodes + "\n");
			}
			output.close();
			System.out.println("Preferences written to disk.");
		} catch (IOException e) {
			JOptionPane.showMessageDialog(null, "Problem writing file. Please ensure you have the necessary privledges.","Write Error",JOptionPane.ERROR_MESSAGE);
		}
	}
	
	// The following block of codes are just private variables that require public
	// request methods so that they are effectively read only outside of this class.
	// This is standard OOP practice.
	
	public String getDerbyDir() {
		return derbyDir;
	}
	
	public String getSource() {
		return source;
	}
	
	public boolean exists() {
		return new File(derbyDir).isDirectory();
	}
	
	public String[][] getGeneralCodes() {
		return generalCodes;
	}
	
	public String[][] getPageCodes() {
		return pageCodes;
	}
	
	public String getMapDir() {
		return pageMapDir;
	}
	
	public void setGenreCodes(String filename) {
		/**
		 * Public interface method for genre code files.  The code reader is private and
		 * internal.  This sets the internal filename and then loads the internal code reader.
		 */
		genreCodes = filename;
		readCodes();
	}
	
	private void readCodes () {
		/**
		 * Reads the genre codes file from disk and parses codes into two categories:
		 * general codes that reflect volume and page level data and those that could 
		 * reflect only page level data.  There's no real reason to keep them separate right
		 * now other than to display them as distinct categories to users.
		 */
		String line;
		// ArrayLists are used for their Python-like functionally.  They are converted to
		// fixed length arrays at the end of this method.
		ArrayList<String[]> all, page;
		all = new ArrayList<String[]>();
		page = new ArrayList<String[]>();
		boolean both = true;
		try {
			InputStream codesIn = new FileInputStream(new File(genreCodes));
			BufferedReader inLines = new BufferedReader(new InputStreamReader(codesIn,Charset.forName("UTF-8")));
			while ((line = inLines.readLine()) != null) {
				if (line.trim().length() > 0) {
					if(line.contains("#GENERAL")) {
						both = true;
					} else if (line.contains("#PAGES")) {
						both = false;
					} else {
						if (both) {
							all.add(line.trim().split("\\t",2));
						} else {
							page.add(line.trim().split("\\t",2));
						}
					}
				}
			}
			inLines.close();
			generalCodes = all.toArray(new String[all.size()][2]);
			pageCodes = page.toArray(new String[page.size()][2]);
		} catch (IOException e) {
			JOptionPane.showMessageDialog(null, "Could not load Genre Codes from " + genreCodes + ".\nPlease ensure file exists.","Load Error.",JOptionPane.ERROR_MESSAGE);
			genreCodes = null;
		}	
	}
	
	public boolean hasGenreCodes() {
		/**
		 * Simple check to see if a genre code file has been selected (either at load-time
		 * from the configuration file or during run-time by the user when starting the
		 * PageMapper).
		 */
		if (genreCodes == null) {
			return false;
		} else {
			return true;
		}
	}
	
}
