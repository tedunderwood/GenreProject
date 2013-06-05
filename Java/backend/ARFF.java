package backend;

import java.util.ArrayList;

public class ARFF {
	/**
	 * Goal of this class is to read an ARFF into memory, provide simple access to searching as a table.
	 * 
	 * Data is stored in flexible lists rather than fixed length arrays to allow for editing (adding entries from metadata database).
	 * 
	 * Data can be accessed as Strings (for reading/writing) via public methods.
	 * 
	 * TODO: 
	 * - Adjust constructors for creating new ARFFs from DerbyDB entries
	 * - Use a sparse matrix?  Check with Ted to see how big these might get
	 * - Interface methods that will return whole entries or specific values from specific entries
	 */
	
	private String [] header;
	private String relation;
	private ArrayList<String> attributes;
	private ArrayList<String []> data;
	
	public ARFF (String[] file) {
		read(file);
	}
	
	public ARFF() {
	}
	
	public void read(String[] file) {
		/**
	 	* This method accepts an ARFF as an array of strings (each is a line from a file).  File operations should he handled by data loader in GUI
	 	* 
	 	* When defining relation and attribute labels, this splits the line at the first space and puts all remaining characters as the label.
	 	*/
		
		String[] parts;
		ArrayList<String> temphead = new ArrayList<String>();
		attributes = new ArrayList<String>();
		data = new ArrayList<String[]>();
		
		for (int i=0;i<file.length;i++){
			if (file[i].startsWith("%")) {
				temphead.add(file[i].trim());
			}
			else if (file[i].toLowerCase().startsWith("@relation")) {
				relation = file[i].trim().split("\\s")[1];
			}
			else if (file[i].toLowerCase().startsWith("@attribute")) {
				attributes.add(file[i].trim().split("\\s")[1]);
			}
			else if (file[i].trim().length() > 0) {
				// If there are characters left after removing whitespace and no matching declarations, then it must be a line of data!
				parts = file[i].trim().split(",");
				data.add(parts.clone());
			}
		}
		
		header = temphead.toArray(new String[temphead.size()]);
		
	}
	
	public void add(String htid) {
		/**
		 * Temporary add method.  Will need to change as more are used.
		 */
		// If the predictions generated here are 100%, then only page values would need to be set...
		// For now just use this one for "whole" volumes and clone with additional values passed in for page-level predictions.
		String[] temp = new String[data.get(0).length];
		for (int i=0;i<temp.length;i++) {
			if (i==0) {
				temp[i] = htid;
			}
			else if (i==temp.length-1) {
				temp[i] = "1.0";
			}
			else {
				temp[i] = "0";
			}
		}
		data.add(temp);
	}
	
	public String[] getString() {
		/**
		 * Returns an array of Strings where each value is a line of text.  Does not include new line characters
		 */
		String[] output = new String[header.length + 1 + attributes.size() + data.size()];
		int bigi = 0;
		String dataline;
		
		for (int i=0;i<header.length;i++){
			output[i] = header[i];
			bigi = i;
		}
		
		bigi++;
		output[bigi] = "@relation " + relation;
		
		for(int i=0;i<attributes.size();i++) {
			bigi++;
			output[bigi] = "@attribute " + attributes.get(i);
		}
		
		for(int i=0;i<data.size();i++) {
			bigi++;
			dataline = new String();
			for(int subs=0;subs<data.get(i).length;subs++){
				if (subs > 0){
					dataline += ',';
				}
				dataline += data.get(i)[subs];
			}
			output[bigi] = dataline;
		}
		
		return output;
	}
	
	public String [] getItems () {
		/**
		 * Returns a list of item identifiers (first value, should be HTid).  Useful for calling up complete metadata listings from DerbyDB.
		 */
		
		String[] items = new String[data.size()];
		for (int i=0;i<data.size();i++){
			items[i] = data.get(i)[0];
		}
		return items;
	}

}
