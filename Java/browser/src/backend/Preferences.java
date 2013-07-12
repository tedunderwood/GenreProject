package backend;

import java.io.*;
import java.util.ArrayList;
import javax.swing.JFileChooser;
import javax.swing.JOptionPane;

public class Preferences {
	/**
	 * The purposes of this class is to read, write, and hold application preferences.
	 * 
	 * For now, it just stores the location of the active DerbyDB directory.
	 */
	
	private File preffile;
	private final String DEFAULT_PREF_FILE = "genrebrowser.ini";
	private String derbydir = null; 
	private String source;
	
	public Preferences () {
		preffile = new File(DEFAULT_PREF_FILE);
		while(derbydir == null) {		
			if (preffile.exists()) {
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
		preffile = new File(filename);
		while(derbydir == null) {
			if (preffile.exists()) {
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
		BufferedReader lines = new BufferedReader(new FileReader(preffile));
		while((line = lines.readLine()) != null){
			rawtext.add(line.trim());
		}
		lines.close();
		for (int i=0;i<rawtext.size();i++) {
			if(rawtext.get(i) == "#PREFS") {
				continue;
			} else {
				if (rawtext.get(i).startsWith("databasedir=")) {
					derbydir = rawtext.get(i).substring(12);
				} else if (rawtext.get(i).startsWith("sourcefile=")) {
					source = rawtext.get(i).substring(11);
				}
			}
		}
		System.out.println("Preferences loaded.");
	}
	
	private void chooseMetadata() {
		System.out.println("Chooser...");
		JFileChooser fdialog = new JFileChooser("./");
		System.out.println("Created...");
		fdialog.showOpenDialog(null);
		System.out.println("Displayed...");
		source = fdialog.getSelectedFile().getAbsolutePath();
		source = source.replace("./", "");
		derbydir = (String)JOptionPane.showInputDialog(null,"Choose a name for new database:","New Database",JOptionPane.PLAIN_MESSAGE,null,null,null);
		derbydir = new File(derbydir).getAbsolutePath();
		derbydir = derbydir.replace("./","");
	}
	
	public void writePrefs() {
		try {
			BufferedWriter output = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(preffile.getAbsolutePath()),"UTF-8"));
			output.write("#PREFS\n");
			output.write("databasedir=" + derbydir + "\n");
			output.write("sourcefile=" + source + "\n");
			output.close();
			System.out.println("Preferences written to disk.");
		} catch (IOException e) {
			JOptionPane.showMessageDialog(null, "Problem writing file. Please ensure you have the necessary privledges.","Write Error",JOptionPane.ERROR_MESSAGE);
		}
	}
	
	public String getDerbyDir() {
		return derbydir;
	}
	
	public String getSource() {
		return source;
	}
	
	public boolean exists() {
		return new File(derbydir).isDirectory();
	}
	
}
