/**
 * 
 */
package datamodel;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Arrays;

/**
 * @author tunderwood
 * 
 * This class acts as a reducer, collecting the features associated with a single docID
 * (aka volumeID).
 * 
 * addFeature is a method that gets called for every feature the Volume receives.
 * A feature is defined as an array of four strings: pageNum, formField, word, and count.
 * 
 * Then, after all features are received, there are two different methods that could be used 
 * to transform Volumes into DataPoints in vector space.
 * 
 * makeVolumePoint turns the whole volume into a single DataPoint.
 * 
 * makePagePoint turns the volume into a collection of DataPoints representing pages; these
 * DataPoints get three extra features that reflect structural information about a page's
 * length, shape, and position in the volume.
 * 
 * @param pagesPerVol	HashMap storing the number of pages (value) for a volume ID (key).
 * @param meanLinesPerPage	HashMap storing the mean number of lines per page 
 * 							in a volume ID (key).
 */

public class Volume {
	String volumeID;
	ArrayList<Integer> listOfLineCounts;
	ArrayList<Integer> listOfPages;
	int numberOfPages;
	int maxPageNum;
	ArrayList<String[]> sparseTable;
	
	public Volume(String volumeID) {
		this.volumeID = volumeID;
		listOfLineCounts = new ArrayList<Integer>();
		listOfPages = new ArrayList<Integer>();
		numberOfPages = 0;
		maxPageNum = 0;
		sparseTable = new ArrayList<String[]>();
	}
	/** 
	 * This method accepts a line from the database, already parsed into a
	 * sequence of fields, with docid removed (it is volumeID of this volume).
	 *  
	 * @param feature:	0 - pageNum, 1 - formField, 2 - word, 3 - count
	 * 
	 */
	public void addFeature(String[] feature) {
		
		sparseTable.add(feature);
		
		// The number of pages in the volume is defined as the number of distinct
		// page numbers it receives. Note that this is not necessarily == to the
		// maximum pageNum value. It's possible for some pages to be blank, in
		// which case we may have no information about them here even though they've
		// increased the max pageNum value.
		
		int pageNum = Integer.parseInt(feature[0]);
		if (!listOfPages.contains(pageNum)) {
			listOfPages.add(pageNum);
			numberOfPages = listOfPages.size();
		}
		
		if (pageNum > maxPageNum) maxPageNum = pageNum;
		
		// If the "word" is actually a structural feature recording the number
		// of lines in a page, this needs to be added to the listOfLineCounts
		// for pages in the volume.
		
		if (feature[2].equals("#textlines")) {
			int count = Integer.parseInt(feature[3]);
			listOfLineCounts.add(count);
		}
		
		// We don't assume that this list will have the same length as the
		// listOfPages, or that there is any mapping between the two. We use
		// it purely to produce a meanLinesPerPage value later.
			
	}
	
	public DataPoint makeVolumePoint(HashMap<String, Integer> vocabularyMap) {
		
		// Create a vector of the requisite dimensionality; initialize to zero.
		int dimensionality = vocabularyMap.size();
		double[] vector = new double[dimensionality];
		Arrays.fill(vector, 0);
		
		// Then sum all occurrences of words to the appropriate vector index.
		for (String[] feature : sparseTable) {
			String word = feature[2];
			if (vocabularyMap.containsKey(word)) {
				int idx = vocabularyMap.get(word);
				double count = Double.parseDouble(feature[3]);
				vector[idx] += count;
			}
		}
		
		DataPoint point = new DataPoint(volumeID, vector);
		return point;
	}
	
	public ArrayList<DataPoint> makePagePoints(HashMap<String, Integer> vocabularyMap) {
		// Page points are much more complex.
		// To start with, divide the sparseTable into page groups.
		
		ArrayList<ArrayList<String[]>> featuresByPage = new ArrayList<ArrayList<String[]>>();
		for (int i = 0; i < numberOfPages; ++ i) {
			ArrayList<String[]> blankPage = new ArrayList<String[]>();
			featuresByPage.add(blankPage);
		}
		
		for (String[] feature : sparseTable) {
			int pageNum = Integer.parseInt(feature[0]);
			if (listOfPages.contains(pageNum)) {
				int idx = listOfPages.indexOf(pageNum);
				ArrayList<String[]> thisPage = featuresByPage.get(idx);
				thisPage.add(feature);
			}
		}
		
		// We need to know the mean number of lines per page.
		
		int totalTextLines = 0;
		for (int lineCount: listOfLineCounts) {
			totalTextLines += lineCount;
		}
		
		double meanLinesPerPage;
		if (numberOfPages > 0 & totalTextLines > 0) {
			meanLinesPerPage = totalTextLines / (double) numberOfPages;		
		}
		else {
			// avoid division by zero, here and later
			meanLinesPerPage = 0.1;
		}
		
		// We're going to create a DataPoint for each page.
		ArrayList<DataPoint> points = new ArrayList<DataPoint>(numberOfPages);
		
		for (int i = 0; i < numberOfPages; ++i) {
			
			ArrayList<String[]> thisPage = featuresByPage.get(i);
			int thisPageNum = listOfPages.get(i);
			
			// The next detail requires some explanation. At present all pages
			// have a textlines and a caplines feature. Even if blank! So
			// a page with only two features in its sparse table is probably
			// blank. No point in creating a DataPoint for it.
			
			if (thisPage.size() < 3) continue;
			
			// Create a vector of the requisite dimensionality; initialize to zero.
			// Note that the dimensionality for page points is 
			// vocabularySize + 3  !!
			
			int vocabularySize = vocabularyMap.size();
			int dimensionality = vocabularySize + 3;
			double[] vector = new double[dimensionality];
			Arrays.fill(vector, 0);
			
			double textlines = 0.1;
			// simple hack to avoid division by zero later in case
			// of a missing value
			double caplines = 0;
			
			// Then sum all occurrences of words to the appropriate vector index.
			
			for (String[] feature : thisPage) {
				String word = feature[2];
				if (vocabularyMap.containsKey(word)) {
					int idx = vocabularyMap.get(word);
					double count = Double.parseDouble(feature[3]);
					vector[idx] += count;
					continue;
				}
				if (word.equals("#textlines")) {
					textlines = Double.parseDouble(feature[3]);
					// Really an integer but cast as double to avoid 
					// integer division
					continue;
				}
				if (word.equals("#caplines")) {
					caplines = Double.parseDouble(feature[3]);
					// Really an integer but cast as double to avoid 
					// integer division
					continue;
				}
			}
			
			// Now we have a feature vector with all the words filled in, but
			// the three extra spaces at the end are still zero.
			// We need to create structural "page features."
			
			double positionInVol = (double) thisPageNum / maxPageNum;
			// TODO: Error handling to avoid division by zero here.
			
			if (textlines == 0) textlines = 0.1;
			// hack to avoid division by zero
					
			double lengthRatio = textlines / meanLinesPerPage;
			double capRatio = caplines / textlines;
			
			vector[vocabularySize] = positionInVol;
			vector[vocabularySize + 1] = lengthRatio;
			vector[vocabularySize + 2] = capRatio;
			
			String label = volumeID + "," + Integer.toString(thisPageNum);
			DataPoint thisPoint = new DataPoint(label, vector);
			points.add(thisPoint);
		}
	return points;	
	}

}
