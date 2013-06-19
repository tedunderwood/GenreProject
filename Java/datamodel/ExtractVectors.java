/**
 * 
 */
package datamodel;
import java.util.Arrays;

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
	 * @param args	A string containing path to a text file as data source.
	 */
	
	public static void main(String[] args) {
		// String dataSource = args[0];
		String dataSource = "/Users/tunderwood/Dropbox/PythonScripts/mine/testdata/testdata.csv";
		
		// The name of a data source is passed in as an argument from the command line.
		// We use that to set static fields in Vocabulary, which can be shared
		// across all nodes without explicitly passing an instance of Vocabulary.
		
		Vocabulary.inputFile = dataSource;
		Vocabulary.vocabularySize = 100;
		Vocabulary.countWords();
			
		// The Vocabulary counts all words in the data and identifies
		// a subset of most-common words. It can now tell us whether 
		// a given word is in that subset. In Hadoop this would
		// probably require a map-reduce step.
		
		BlockReader thisBlock = new BlockReader(dataSource);
		
		// I've implemented the reader
		// in a way that would allow multiple readers to read from
		// different dataSources.
		
		GroupedSequence mappedLines = thisBlock.readPages();
		
		// Now we have a sequence of lines separated out by document ID.
		// If we wanted them separated by page, we could say readPages().
		
		// The next stage is to transform groups of lines into vectors.
		// I've implemented this "reducing stage" as a static method
		// of the Vocabulary, because the information to align words
		// with particular index positions of the vector is
		// contained in the Vocabulary.
		
		DataPoint[] points = Vocabulary.makeDataPoints(mappedLines);
		
		// What follows is insignificant code that I'm using merely to test
		// that the conversion has worked, by writing the DataPoints
		// to disk in a readable way.
		
		String[] output = new String[points.length];
		for (int i = 0; i < points.length; ++i) {
			DataPoint aPoint = points[i];
			double[] vector = aPoint.vector;
			output[i] = aPoint.label + ": " + Arrays.toString(vector);
		}
		
		LineWriter outfile = new LineWriter("/Users/tunderwood/VectorOutput.txt", false);
		outfile.send(output);
	}

}
