package kmeans;
import java.util.ArrayList;
import java.util.Arrays;
import datamodel.*;

public class Centroid {
	double[] center;
	int label;
	int dimensionality;
	double[] mahalanobis;
	final static double alpha = 50;
	final static boolean useDistortion = true;
	ArrayList<DataPoint> members;
	
	public Centroid(double[] center, int label) {
		this.center = center;
		dimensionality = center.length;
		this.label = label;
		this.mahalanobis = new double[dimensionality];
		Arrays.fill(mahalanobis, 1);
	}
	
	public double getDistance(DataPoint aPoint, boolean spherical) {
		double[] pointVector = aPoint.getVector();
		assert (center.length == pointVector.length);
		if (spherical) return cossim(center, pointVector, mahalanobis, useDistortion);
		else return euclid(center, pointVector, mahalanobis, useDistortion);
	}
	
	public void clearMembers(){
		members = new ArrayList<DataPoint>();
	}
	
	public void addMember(DataPoint point) {
		members.add(point);
	}
	
	public double newCenter(boolean spherical) {
		double[] newCenter = new double[dimensionality];
		int numberMembers = members.size();
		if (numberMembers < 1) {
			return -1;
			// returning a negative number will indicate that this centroid is "dead";
			// it has no members
		}
		
		// Take the mean value of members in every dimension to produce the
		// new center. In spherical clustering, members have already been
		// normalized.
		Arrays.fill(newCenter, 0);
		for (DataPoint member : members) {
			double[] thisVector = member.getVector();
			for (int i = 0; i < dimensionality; ++i) {
				newCenter[i] += thisVector[i];
			}
		}
		for (int i = 0; i < dimensionality; ++i) {
			newCenter[i] = newCenter[i] / numberMembers;
		}
		
		// We're going to return the distance between old center and new center.
		// We don't distort this cossim calculation with mahalanobis. We use
		// cossim as a distance metric if we're doing spherical clustering,
		// otherwise Euclidean distance.
		
		double distanceMoved;
		if (spherical) {
			distanceMoved = cossim(center, newCenter, mahalanobis, false);
		}
		else {
			distanceMoved = euclid(center, newCenter, mahalanobis, false);
		}
		
		calculateMahalanobis(newCenter);
		center = newCenter;
		System.out.println("Cluster: " + Integer.toString(label));
		System.out.println("Dist: " + distanceMoved);
		return distanceMoved;
		
	}
	
	private void calculateMahalanobis(double[] newCenter) {
		// Now calculate a new mahalanobis distortion, by getting the variance
		// of members in every dimension.
		
		int numberMembers = members.size();
		
		double[] dimensionVariance = new double[dimensionality];
		for (DataPoint member: members) {
			double[] thisVector = member.getVector();
			for (int i = 0; i < dimensionality; ++i) {
				dimensionVariance[i] += Math.pow(newCenter[i] - thisVector[i], 2);
			}
		}
		
		// Now we go through a couple tricky kinds of normalization
		// and correction. We want to take the sqrt of the variance
		// to produce a std deviation in each dimension, but we also
		// want to add a correction to each dimension
		// to prevent it going entirely to zero. This correction is
		// (meanstandarddeviation / alpha) where alpha is some
		// arbitrary constant. 
		
		// Finally, we normalize the whole vector of standard deviations
		// so that the sum doesn't vary from one cluster to another.
		// Otherwise it could cause clusters to grow/shrink indefinitely. 
		
		double mahalanobisSum = 0;
		for (int i = 0; i < dimensionality; ++i) {
			mahalanobis[i] = Math.sqrt(dimensionVariance[i] / numberMembers);
			mahalanobisSum += mahalanobis[i];
		}
		double meanStandardDev = mahalanobisSum / dimensionality;
		double nozeroCorrection = meanStandardDev / alpha;
		
		// Instead of normalizing mahalanobis[] so that it sums to one, we normalize it so that the 
		// *mean* value is one. This requires dividing every value by the mean value of the
		// numerator.
		
		double normalizingDenominator = meanStandardDev + nozeroCorrection;
		
		for (int i = 0; i < dimensionality; ++i) {
			mahalanobis[i] = (mahalanobis[i] + nozeroCorrection) / normalizingDenominator;
			System.out.println(Integer.toString(i) + ": " + Double.toString(mahalanobis[i]));
		}
	}
	
	private double cossim(double[] a, double[] b, double[] distortionField, boolean distort) {
		double dotproduct = 0;
		double amagnitude = 0;
		double bmagnitude = 0;
		for (int i = 0; i < a.length; ++i) {
			// We start by varying the importance of features using the Mahalanobis distortion field.
			if (distort) {
				a[i] = a[i] / distortionField[i];
				b[i] = b[i] / distortionField[i];
			}
			dotproduct += a[i] * b[i];
			amagnitude += a[i] * a[i];
			bmagnitude += b[i] * b[i];
		}
		amagnitude = Math.sqrt(amagnitude);
		bmagnitude = Math.sqrt(bmagnitude);
		return 1.01 - (dotproduct / (amagnitude * bmagnitude));
	}
	
	private double euclid(double[] a, double[] b, double[] distortionField, boolean distort) {
		double sumofsquares = 0;
		for (int i = 0; i < a.length; ++i) {
			// We start by varying the importance of features using the Mahalanobis distortion field.
			if (distort) sumofsquares += Math.pow(a[i]-b[i], 2) / distortionField[i];
			else sumofsquares += Math.pow(a[i]-b[i], 2);
		}
		return Math.sqrt(sumofsquares);
	}
}
