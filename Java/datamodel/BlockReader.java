/**
 * 
 */
package datamodel;
import java.util.ArrayList;
import java.util.Arrays;

/**
 * @author tunderwood
 * 
 * This class does some of the work of a mapper, reading lines from a text
 * file, extracting a "key" (docID) from the line, and sending that "key" plus the
 * remaining line fields (as a "value") to a Volume that collects all the lines
 * describing a single docID.
 * 
 * The Volume will then act as a reducer.
 * 
 */

public class BlockReader {
	
	String dataSource;
	
	public BlockReader(String dataSource) {
		this.dataSource = dataSource;
	}

// THIS METHOD NOW DEPRECATED.
//	public GroupedSequence readVolumes() {
//		
//		GroupedSequence volumes = new GroupedSequence();
//		
//		LineReader textSource = new LineReader(dataSource);
//		String[] filelines = textSource.readlines();
//		for (String line : filelines) {
//			String[] tokens = line.split(",");
//			int tokenCount = tokens.length;
//			if (tokenCount != 5) {
//				System.out.println("Error: tokenCount not equal to 5 at " + line);
//				System.out.println(tokenCount);
//				System.out.println(tokens[0]);
//				// not the world's most sophisticated error handling here
//				// TODO: define Exception handling for input format issues
//				continue;
//			}
//			// The format of an input line, as you'll recall, is
//			// String docid, int pagenumber, int formFlag, String word, int countOfWord
//			// Here we're only interested in docid and word.
//			String word = tokens[3];
//			String docid = tokens[0];
//			
//			// We do nothing unless the word is in the subset of common words stored
//			// in our vocabulary. Note that the Vocabulary class ensures this subset
//			// contains the special features #textlines and caplines.
//			
//			// In Hadoop, the mapper doing this will need to possess a copy
//			// of the vocabulary, or at least its HashSet, aka, wordlist.vocabularySet.
//			// The mapper's job is to extract the docid from the input line and send
//			// (docid + whole line) as a (key, value) pair to a reducer.
//			
//			if (Vocabulary.includes(word)) {
//				volumes.addLine(docid, line.trim());
//			}
//		}
//		
//		return volumes;
//	}
	
public ArrayList<Volume> mapVolumes() {
		
		ArrayList<Volume> volumes = new ArrayList<Volume>();
		ArrayList<String> volumeIDs = new ArrayList<String>();
		
		// If we were maximixing speed, we could use a HashMap for volumes
		// and a HashSet for volumeIDs. But in the real implementation, this
		// mapping of keys (volumeIDs) to particular reducers (volumes)
		// will be taken care of by Hadoop, so I
		// have made no effort to optimize it here.
		
		LineReader textSource = new LineReader(dataSource);
		String[] filelines = textSource.readlines();
		
		for (String line : filelines) {
			String[] tokens = line.split(",");
			int tokenCount = tokens.length;
			if (tokenCount != 5) {
				System.out.println("Error: tokenCount not equal to 4 at " + line);
				// not the world's most sophisticated error handling here
				// TODO: define Exception handling for input format issues
				continue;
			}
			// The format of an input line, as you'll recall, is
			// String docid, int pagenumber, int formFlag, String word, int countOfWord
			// Here we're only interested in docid and word.
			
			String word = tokens[3];
			String docid = tokens[0];
			
			// We do nothing unless the word is in the subset of common words stored
			// in our vocabulary.
			
			// If it's in the vocabulary, then we check to see whether this is a volume
			// we already "own." If so, we add the feature (the four fields after the docid)
			// to that volume. Otherwise, create a new volume.
			
			if (Vocabulary.includes(word)) {
				if (volumeIDs.contains(docid)) {
					int idx = volumeIDs.indexOf(docid);
					Volume thisvol = volumes.get(idx);
					thisvol.addFeature(Arrays.copyOfRange(tokens, 1, tokens.length));
					// we only send the fields after docid
				}
				else {
					Volume newvol = new Volume(docid);
					newvol.addFeature(Arrays.copyOfRange(tokens, 1, tokens.length));
					volumes.add(newvol);
					volumeIDs.add(docid);
				}	
			}
			
			// In Hadoop, everything above would be done by a mapper that would possess a copy
			// of the vocabulary, or at least its HashSet, aka, wordlist.vocabularySet.
			// The mapper's job is to extract the docid from the input line and send
			// (docid + remainder of line) as a (key, value) pair to a reducer.
		}
		
		return volumes;
	}

}
