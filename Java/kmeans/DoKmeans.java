package kmeans;
import datamodel.*;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Random;
import java.util.Scanner;

import datamodel.ExtractVectors;

public class DoKmeans {
	
	/**
	 * Right now I find that this code runs with either Euclidean distance or kmeans as the
	 * distance metric when you're *not* using the quasi-mahalanobis adjustment in "Centroid."
	 * But when you flip useDistortion to "true," it only runs with Euclidean distance.
	 * In other words, the "spherical" flag below has to be "false" if the useDistorion flag
	 * in Centroid is set to "true."
	 * 
	 * @param args
	 */
	public static void main(String[] args) {
		String dataSource = "/Users/tunderwood/Dropbox/PythonScripts/mine/testdata/testdata.csv";
		boolean pageFlag = true;
		int featureCount = 100;
		int k = 10;
		int maxIters = 10;
		boolean spherical = false;
		
		Random rolldice = new Random();
		Scanner keyboard = new Scanner(System.in);

//	If I were running this with real data, I would use the following line.
//
//		ArrayList<DataPoint> datapoints = ExtractVectors.getPoints(dataSource, pageFlag, featureCount);

//	But instead I'm using sample data. 
		ArrayList<DataPoint> datapoints = SampleGenerator.generate();
		int numPoints = datapoints.size();
		
		Centroid[] centroids = new Centroid[k];
		
		DataPoint firstCenter = datapoints.get(rolldice.nextInt(numPoints));
		for (DataPoint point : datapoints) {
			point.normalizeLength();
		}
		
		centroids[0] = new Centroid(firstCenter.getVector(), 0);
		int nextCentroid = 1;
		
		ArrayList<Integer> takenPoints = new ArrayList<Integer>();
		takenPoints.add(datapoints.indexOf(firstCenter));
		
		// A mode of initializing clusters known as Kmeans ++
		// We start by assigning one cluster to a random point (selected above),
		// and then assign the next cluster to the point that has the largest
		// *minimum* distance to an existing cluster.
		
		// The outer loop below selects clusters. Inside that there's a loop
		// for points, looking for the point with the largest minDistance from
		// existing clusters. That requires yet another loop, to loop through 
		// all existing clusters and find the one that's closest to the point.
		
		for (int i = 1; i < k; ++i) {
			DataPoint furthestPoint = datapoints.get(rolldice.nextInt(numPoints));
			double maxDistance = 0;
			for (int j = 0; j < numPoints; ++j) {
				DataPoint thisPoint = datapoints.get(j);
				double minForPoint = 1000;
				for (int h = 0; h < nextCentroid; ++h) {
					double thisDistance = centroids[h].getDistance(thisPoint, spherical);
					if (Double.isNaN(thisDistance)) {
						System.out.println(h);
						continue;
					}
					if (thisDistance < minForPoint) {
						minForPoint = thisDistance;
					}
				}
				if (minForPoint > maxDistance) {
					maxDistance = minForPoint;
					furthestPoint = thisPoint;
				}
			}
			centroids[i] = new Centroid(furthestPoint.getVector(), i);
			takenPoints.add(datapoints.indexOf(furthestPoint));
			System.out.println(furthestPoint.label);
			nextCentroid += 1;
		}
		
		// We keep track of clusters that have "died" because they lost
		// all their members.
		boolean[] isDead = new boolean[k];
		Arrays.fill(isDead, false);
		
		for (int iter = 0; iter < maxIters; ++ iter) {
			
			// Initialize the member lists of all the centroids. 
			for (int i = 0; i < k; ++i) {
				centroids[i].clearMembers();
			}
			
			// Assign points to centroids.
			for (DataPoint thisPoint: datapoints) {
				double minDistance = 1000;
				int closestCentroid = -1;
				for (int i = 0; i < k; ++i) {
					if (isDead[i]) {
						// System.out.println("Dead cluster at " + Integer.toString(i));
						continue;
					}
					double thisDistance = centroids[i].getDistance(thisPoint, spherical);
					// System.out.println(thisDistance);
					if (thisDistance < minDistance) {
						minDistance = thisDistance;
						closestCentroid = i;
					}
				}
				if (closestCentroid < 0) {
					// System.out.println("Error assigning points to centroids.");
					closestCentroid = 0;
				}
				centroids[closestCentroid].addMember(thisPoint);
			}
			
			// Calculate new centers.
			for (int i = 0; i < k; ++i) {
				if (isDead[i]) {
					continue;
				}
				
				// The method newCenter causes a centroid to recalculate its
				// center and return the distance moved. If flag spherical
				// is true, the distance metric is cosine similarity rather
				// than Euclidean distance.
				double distanceMoved = centroids[i].newCenter(spherical);
				if (distanceMoved < 0) {
					isDead[i] = true;
					System.out.println(distanceMoved);
				}
			}	
			
		}
		
		// Time to output the clusters
		ArrayList<String> prepOutput = new ArrayList<String>();
		
		for (int i = 0; i < k; ++i) {
			prepOutput.add("CLUSTER " + Integer.toString(i));
			ArrayList<DataPoint> thisCluster = centroids[i].members;
			for (DataPoint aPoint : thisCluster) {
				double[] vector = aPoint.getVector();
				prepOutput.add(aPoint.label + ": " + Arrays.toString(vector));
			}
		}
		
		LineWriter outfile = new LineWriter("/Users/tunderwood/KmeansClusters.txt", false);
		
		// The following conversion is really hacky. I ought to rewrite LineWriter so that
		// it accepts an ArrayList. Instead I'm converting ArrayList to array before output.
		
		String[] output = new String[prepOutput.size()];
		for (int i = 0; i < prepOutput.size(); ++i) {
			output[i] = prepOutput.get(i);
		}
		outfile.send(output);
	
	}

}
