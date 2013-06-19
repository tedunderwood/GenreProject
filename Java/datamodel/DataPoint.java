package datamodel;
import java.lang.Math;

/**
 * @author tunderwood
 *
 * A fuller implementation of this class will have more getter and setter methods.
 * At the moment, I'm just treating this as a data object that pairs a label with
 * a vector of feature values.
 * 
 */

public class DataPoint {
	String label;
	double[] vector;
	int dimensionality;
	double length;
	
	public DataPoint(String label, double[] vector){
		this.label = label;
		this.vector = vector;
		System.out.println(vector[0]);
		dimensionality = vector.length;
		double length = 0;
		for (int i = 0; i < dimensionality; ++ i) {
			length = length + Math.pow(vector[i], 2);
		}
		length = Math.sqrt(length);
		
	}

}
