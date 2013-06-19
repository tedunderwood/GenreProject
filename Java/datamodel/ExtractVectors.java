/**
 * 
 */
package datamodel;
import java.util.Arrays;
import java.util.ArrayList;
import java.util.HashMap;

/**
 * @author tunderwood
 * Accepts a text file containing a sparse table in the format described under
 * Plans/MainDatabase.pdf. Reads that stream of lines, first, to establish a
 * subset of the vocabulary that will be used to create standardized vectors.
 * This could be one map-reduce pass.
 * 
 * Then we go back to the sparse table and divide it into groups of lines
 * associated with different data objects (which could be either pages or 
 * volumes). In this example I've grouped lines by volume, but the class
 * BlockReader also contains a method to group lines by page. This is a second
 * "mapping" phase producing lines grouped by a "key" (aka "label").
 * 
 * Once we have lines grouped by key (represented here as a class called GroupedSequence),
 * we can convert those groups of lines into actual DataPoints to be passed to a
 * clustering or classification algorithm. This is accomplished by a static method
 * of the Vocabulary class, which knows the appropriate mapping of words to
 * positions in a vector. That method (makeDataPoints) would probably be implemented
 * as a reducer in Hadoop.
 *
 */
public class ExtractVectors {

	/**
	 * @param args
	 * @param argument1: 	a string containing a path to a data source
	 * @param argument2:	an integer value defining vocabulary size
	 * @param argument3:	either p (cluster by page) or v (by volume, default)	
	 */
	
	public static void main(String[] args) {
		// Haven't yet implemented parsing of command-line arguments.
		// String dataSource = args[0];
		// int vocabSize = Integer.parseInt(args[1])
		// String pageCode = args[2]
		
		String dataSource = "/Users/tunderwood/Dropbox/PythonScripts/mine/testdata/testdata.csv";
		boolean pageFlag = true;
		
		// The name of a data source is passed in as an argument from the command line.
		// We use that to set static fields in Vocabulary, which can be shared
		// across all nodes without explicitly passing an instance of Vocabulary.
		// pageFlag defines whether we're clustering by page or by volume (default).
		
		Vocabulary.inputFile = dataSource;
		Vocabulary.vocabularySize = 100;
		Vocabulary.countWords();
				
		// The Vocabulary counts all words in the data and identifies
		// a subset of most-common words. It can now tell us whether 
		// a given word is in that subset. In Hadoop this would
		// probably require a map-reduce step.
		
		HashMap<String, Integer> vocabularyMap = Vocabulary.getMap();
		
		BlockReader mapper = new BlockReader(dataSource);
		
		// The mapper takes a text file and breaks it into
		// key, value pairs where the key is a docid,
		// and the value is the other 4 fields on the same line.
		
		ArrayList<Volume> volumes = mapper.mapVolumes();
		
		// The Volume objects will reduce all the lines associated with a
		// single docid. When they do this they produce DataPoints that can
		// either represent volumes or individual pages. I've implemented
		// these alternatives as two different methods of the Volume class.
		
		ArrayList<DataPoint> datapoints = new ArrayList<DataPoint>();
		
		if (pageFlag) {
			// We're producing page points.
			for (Volume thisVol : volumes) {
				ArrayList<DataPoint> newPoints = thisVol.makePagePoints(vocabularyMap);
				datapoints.addAll(newPoints);
			}
		}
		else {
			// We're producing volume points.
			for (Volume thisVol : volumes) {
				DataPoint newPoint = thisVol.makeVolumePoint(vocabularyMap);
				datapoints.add(newPoint);
			}
		}
		
		// What follows is insignificant code that I'm using merely to test
		// that the conversion has worked, by writing the DataPoints
		// to disk in a readable way.
		
		String[] output = new String[datapoints.size()];
		for (int i = 0; i < datapoints.size(); ++i) {
			DataPoint aPoint = datapoints.get(i);
			double[] vector = aPoint.vector;
			output[i] = aPoint.label + ": " + Arrays.toString(vector);
		}
		
		LineWriter outfile = new LineWriter("/Users/tunderwood/VectorOutput.txt", false);
		outfile.send(output);
	}

}
