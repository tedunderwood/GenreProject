/**
 * 
 */
package datamodel;

/**
 * @author tunderwood
 * 
 * This class does some of the work of a mapper, reading lines from a text
 * file, extracting a "key" from the line, and sending that "key" plus the
 * line itself (as a "value") to a GroupedSequence where values are grouped
 * by key. In Hadoop this might actually be simpler.
 * 
 * I've provided options that group lines by "page" as well as by "volume."
 * Probably I could have written that code more elegantly so there's less duplication
 * of code, and more encapsulation. But I just wanted to get a framework in place.
 * Also, it's a bit wasteful to send the <i>whole</i> line as a "value" when we
 * really only need the part after the "key." But this is a first draft.
 * 
 */

public class BlockReader {
	
	String dataSource;
	
	public BlockReader(String dataSource) {
		this.dataSource = dataSource;
	}
	
	public GroupedSequence readVolumes() {
		
		GroupedSequence volumes = new GroupedSequence();
		
		LineReader textSource = new LineReader(dataSource);
		String[] filelines = textSource.readlines();
		for (String line : filelines) {
			String[] tokens = line.split(",");
			int tokenCount = tokens.length;
			if (tokenCount != 5) {
				System.out.println("Error: tokenCount not equal to 5 at " + line);
				System.out.println(tokenCount);
				System.out.println(tokens[0]);
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
			// in our vocabulary
			
			// In Hadoop, this decision would be made by a mapper that would possess a copy
			// of the vocabulary, or at least its HashSet, aka, wordlist.vocabularySet.
			// The mapper's job is to extract the docid from the input line and send
			// (docid + whole line) as a (key, value) pair to a reducer. Here that job
			// is being done partly here, and partly by GroupedSequence.
			
			if (Vocabulary.includes(word)) {
				volumes.addLine(docid, line.trim());
			}
		}
		
		return volumes;
	}
	
public GroupedSequence readPages() {
		
		GroupedSequence pages = new GroupedSequence();
		
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
			// Here we're only interested in docid, page, and word.
			String word = tokens[3];
			String page = tokens[1];
			String docid = tokens[0];
			String key = docid + "<p>" + page;
			
			// Okay, this is admittedly cheesy, but it seems to me that it might be the simplest way
			// of creating generic functions that can handle clustering either at the volume or at the page
			// level. Simply define all our functions as dealing with data objects that have two
			// attributes: a) a String objectLabel, and b) a vector of double values. 
			
			// If we're dealing with volumes, the objectLabel will = docid.
			// If we're dealing with pages, objectLabel = docid + "<p>" + page, concatenated as a String.
			// I can guarantee that "<p>" will not ordinarily appear inside a docid, so we can
			// always parse this objectLabel back into a docid + pageNumber if we need to.
			
			if (Vocabulary.includes(word)) {
				pages.addLine(key, line.trim());
			}
			
			// We do nothing unless the word is in the subset of common words stored
			// in our vocabulary
			
			// In Hadoop, this decision would be made by a mapper that would possess a copy
			// of the vocabulary, or at least its HashSet, aka, wordlist.vocabularySet.
			// The mapper's job is to extract the docid from the input line and send
			// (docid + whole line) as a (key, value) pair to a reducer. Here that job
			// is being done partly here, and partly by GroupedSequence.
		}
		
		return pages;
	}

}
