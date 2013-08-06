package backend;

import java.io.*;
import java.nio.charset.Charset;
import java.util.ArrayList;
import org.apache.commons.compress.compressors.bzip2.BZip2CompressorInputStream;

public class VolumeReader {
	/**
	 * This class retrieves volumes stored in bzip2 or text files and returns them as String arrays.  Initializing a new VolumeReader will retrieve and load the volume into memory, allowing the reader to act as an interface.
	 */
	
	private String rootPath="/Users/mike/Desktop/sample_data/"; //For testing purposes. When working, load from Preferences
	private String path, prefix, postfix, htid;
	private ArrayList<String[]> volumePages;
	private File volumeFile;
	
	public VolumeReader (String id, String root) {
		//rootPath = root;
		htid = id;
		parseVolumePath(htid);
		//TODO: Do a bz2 check?
		volumeFile = new File(path + postfix + "/" + postfix + ".txt");
		if(!volumeFile.exists()) {
			System.out.println("File not found.");
		}
		readTXTFile();
	}
	
	private void parseVolumePath(String htid) {
		/**
		 * This function takes a given htid and parses it out to a file location.
		 * 
		 * The complete version of this algorithm should return the bzip2 as a File.  For now just the path as a String.
		 */
		int period = htid.indexOf(".");
		prefix = htid.substring(0,period);
		postfix = htid.substring(period+1);
		System.out.println(htid);
		if(postfix.indexOf(":") != -1) {
			postfix = postfix.replaceAll(":","+");
			postfix = postfix.replaceAll("/","=");
		}
		path = rootPath + prefix + "/pairtree_root/";
		if (postfix.length() % 2 == 0) {
			for(int i=0;i<postfix.length();i+=2) {
				path += postfix.substring(i,i+2) + "/";
			}
		} else {
			for(int i=0;i<postfix.length()-2;i+=2) {
				path += postfix.substring(i,i+2) + "/";
			}
			path += postfix.substring(postfix.length()-1) + "/";
		}
		System.out.println(path);
	}
	
	private void readBZ2File() {

		String line;
		volumePages = new ArrayList<String[]>();
		ArrayList<String> currentPage = new ArrayList<String>();

		try {
			BZip2CompressorInputStream bzipIn = new BZip2CompressorInputStream(new FileInputStream(volumeFile));
			BufferedReader inLines = new BufferedReader(new InputStreamReader(bzipIn,Charset.forName("UTF-8")));
			while ((line = inLines.readLine()) != null) {
				if(line.startsWith("<div") || line.startsWith("</div")) {
					continue;
				} else if (line.startsWith("<pb>")) {
					volumePages.add(currentPage.toArray(new String[currentPage.size()]));
					currentPage = new ArrayList<String>();
				} else {
					currentPage.add(line.trim());
				}
			}
			inLines.close();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} 
		
	}
	
	private void readTXTFile() {
		String line;
		volumePages = new ArrayList<String[]>();
		ArrayList<String> currentPage = new ArrayList<String>();
		System.out.println("Reading volume...");
		try {
			InputStream volumeIn = new FileInputStream(volumeFile);
			BufferedReader inLines = new BufferedReader(new InputStreamReader(volumeIn,Charset.forName("UTF-8")));
			while ((line = inLines.readLine()) != null) {
				if(line.startsWith("<div") || line.startsWith("</div")) {
					continue;
				} else if (line.startsWith("<pb>")) {
					volumePages.add(currentPage.toArray(new String[currentPage.size()]));
					currentPage = new ArrayList<String>();
				} else {
					currentPage.add(line.trim());
				}
			}
			inLines.close();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} 

	}
	
	public int getLength() {
		return volumePages.size();
	}
	
	public String[] getPage(int p) {
		return volumePages.get(p);
	}
	
	public String getFileID() {
		return prefix + "." + postfix;
	}
	
	public String getHTID() {
		return htid;
	}
	
}
