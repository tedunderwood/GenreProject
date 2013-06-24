package kmeans;
import datamodel.*;
import java.util.Random;
import java.util.ArrayList;

public class SampleGenerator {
	
	public static ArrayList<DataPoint> generate() {
		String[] firstlabels = {"a", "b", "c"};
		String[] secondlabels = {"0", "1", "2"};
		ArrayList<DataPoint> datapoints = new ArrayList<DataPoint>(); 
		int counter = 0;
		Random dice = new Random();
		
		for (int i = 0; i < 11; ++i) {
			int firstidx = i % 3;
			for (int j = 0; j < 11; ++j) {
				int secondidx = j % 3;
				String label = Integer.toString(counter) + firstlabels[firstidx] + secondlabels[secondidx];
				counter += 1;
				double[] vector = new double[11];
				for (int k = 0; k < 11; ++k) {
					double value = (double) dice.nextInt(10);
					int kdex = k % 3;
					if (kdex == secondidx) value = value + 5;
					if (kdex == firstidx) value = value * 2;
					if (k == secondidx + 3) value = value + 10;
					if (k == firstidx) value = value + 10;
					vector[k] = value;
				}
				DataPoint newPoint = new DataPoint(label, vector);
				datapoints.add(newPoint);
			}
		}
		return datapoints;
	}

}
