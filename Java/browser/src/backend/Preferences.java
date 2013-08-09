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
	 * 
	 * For now, it just stores the location of the active DerbyDB directory.
	 * 
	 * pageMapDir will default to "pagemaps/" and users will not be prompted from within
	 * the program to edit this value.  However, if a pagemapsdir= line is added to the ini
	 * file, then Preferences will override the default.
	 * 
	 * TODO:
	 * Add codes.ini (and possibly pagemap file?)
	 */
	
	private File prefsFile;
	private final String DEFAULT_PREF_FILE = "genrebrowser.ini";
	private String derbyDir = null, genreCodes = null, pageMapDir = "pagemaps/"; 
	private String source;
	private String[][] generalCodes, pageCodes;
	
	public Preferences () {
		prefsFile = new File(DEFAULT_PREF_FILE);
		while(derbyDir == null) {		
			if (prefsFile.exists()) {
				try {
					readPrefs();
				} catch (IOException e) {
					JOptionPane.showMessageDialog(null, "Problem reading file. Please try again.\nExiting.","Loading Error",JOptionPane.ERROR_MESSAGE);
				}
			} else {
				System.out.println("No preferences found. Creating new workspace.");
				chooseMetadata();
			}
		}
	}
	
	public Preferences(String filename) {
		/**
		 * This constructor is for testing purposes. Allows for alternate preference profiles.
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
				System.out.println(filename + " does not exist. Creating new workspace.");
				chooseMetadata();
			}
		}
	}
	
	private void readPrefs() throws IOException {
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
				}

			}
		}
		System.out.println("Preferences loaded.");
		if(genreCodes != null) {
			System.out.println("Trying to load genre codes file.");
			readCodes();
		}
	}
	
	private void chooseMetadata() {
		//Pop-up asking for select source file
		JOptionPane.showMessageDialog(null, "Please specify a seed file for the browser's database.","First Time Configuration",JOptionPane.OK_OPTION);
		JFileChooser seed = new JFileChooser(System.getProperty("user.dir"));
		seed.showOpenDialog(null);
		source = seed.getSelectedFile().getAbsolutePath();
		derbyDir = (String)JOptionPane.showInputDialog(null,"Choose a name for the browser's database:","First Time Configuration",JOptionPane.PLAIN_MESSAGE,null,null,null);
		derbyDir = new File(derbyDir).getAbsolutePath();
		
	}
	
	public void writePrefs() {
		try {
			BufferedWriter output = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(prefsFile.getAbsolutePath()),"UTF-8"));
			output.write("#PREFS\n");
			output.write("databasedir=" + derbyDir + "\n");
			output.write("sourcefile=" + source + "\n");
			if (!pageMapDir.equals("pagemaps/")) {
				output.write("pagemapdir=" + pageMapDir + "\n");
			}
			if (genreCodes != null) {
				output.write("genrecodes=" + genreCodes + "\n");
			}
			output.close();
			System.out.println("Preferences written to disk.");
		} catch (IOException e) {
			JOptionPane.showMessageDialog(null, "Problem writing file. Please ensure you have the necessary privledges.","Write Error",JOptionPane.ERROR_MESSAGE);
		}
	}
	
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
		 * If user 
		 */
		genreCodes = filename;
		readCodes();
	}
	
	private void readCodes () {
		///TODO: Transfer to Preferences after prototype is functional
		String line;
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
		if (genreCodes == null) {
			return false;
		} else {
			return true;
		}
	}
	
}
