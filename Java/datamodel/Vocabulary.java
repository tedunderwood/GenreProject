/**
 * 
 */
package datamodel;
import java.util.HashSet;
import java.util.HashMap;
import java.util.Arrays;
import java.util.ArrayList;

/**
 * @author tunderwood
 *
 * This is a static class. No instances are ever created. All of its fields,
 * and all of its methods, are static.
 * 
 */

public class Vocabulary {
	static String inputFile;
	static int vocabularySize = 10000;
	static String[] vocabularyList;
	static HashSet<String> vocabularySet;
	static HashMap<String, Integer> vocabularyMap;
	
	public Vocabulary(String dataSource) {
		inputFile = dataSource;
	}
	
	public Vocabulary(String dataSource, int vocabSize) {
		inputFile = dataSource;
		vocabularySize = vocabSize;
	}
	
	static public void countWords() {
		HashMap<String, Integer> sumOfWords = new HashMap<String, Integer>();
		// This will keep track of the count of words for each word
		
		LineReader textSource = new LineReader(inputFile);
		String[] filelines = textSource.readlines();
		for (String line : filelines) {
			String[] tokens = line.split(",");
			int tokenCount = tokens.length;
			if (tokenCount != 5) {
				System.out.println("Error: tokenCount not equal to 5 at " + line);
				// not the world's most sophisticated error handling here
				// TODO: define Exception handling for input format issues
				continue;
			}
			// The format of an input line, as you'll recall, is
			// String docid, int pagenumber, int formFlag, String word, int countOfWord
			// Here we're only interested in word and countOfWord
			String word = tokens[3];
			Integer newCountOfWord = Integer.parseInt(tokens[4]);
			
			if (sumOfWords.containsKey(word)) {
				Integer currentCount = sumOfWords.get(word);
				currentCount += newCountOfWord;
				sumOfWords.put(word, currentCount);
			}
			else {
				sumOfWords.put(word, newCountOfWord);
			}
		}
		
		// now we have a HashMap that maps each word to its count
		ValueComparator inValueOrder = new ValueComparator(sumOfWords);
		int mapSize = sumOfWords.size();
		String[] allTheKeys = new String[mapSize];
		int idx = 0;
		for (String aWord : sumOfWords.keySet()) {
			allTheKeys[idx] = aWord;
			idx += 1;
		}
		
		Arrays.sort(allTheKeys, inValueOrder);
		
		vocabularyList = new String[vocabularySize];
		vocabularySet = new HashSet<String>();
		vocabularyMap = new HashMap<String, Integer>();
		
		for (int i = 0; i < vocabularySize; ++i) {
			System.out.println(i);
			System.out.println(allTheKeys[i]);
			vocabularyList[i] = allTheKeys[i];
			vocabularySet.add(allTheKeys[i]);
			vocabularyMap.put(allTheKeys[i], i);
		}
		
		// The vocabulary is stored in several different ways to maximize
		// efficiency. It's not going to be that large; memory is less an
		// issue than speed here.
	}
	
	static public boolean includes(String aWord) {
		if (vocabularySet.contains(aWord)) {
			return true;
		}
		else {
			return false;
		}
	}
	
	static public DataPoint[] makeDataPoints(GroupedSequence linegroups) {
		int memberCount = linegroups.memberCount;
		DataPoint[] points = new DataPoint[memberCount];
		ArrayList<String> labelList = linegroups.memberList;
		int idx = 0;
		for (String label : labelList) {
			ArrayList<String> thisMember = linegroups.getMember(label);
			double[] vector = new double[vocabularySize];
			Arrays.fill(vector, 0);
			for (String line : thisMember) {
				String[] tokens = line.split(",");
				String word = tokens[3];
				double count = Double.parseDouble(tokens[4]);
				if (vocabularySet.contains(word)) {
					int featureIdx = vocabularyMap.get(word);
					vector[featureIdx] = count;	
				}
			}
			points[idx] = new DataPoint(label, vector);
			idx += 1;
		}
	return points;
	}

}
