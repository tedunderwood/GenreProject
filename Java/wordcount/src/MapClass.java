import java.io.IOException;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;


public class MapClass extends Mapper<LongWritable,Text,Text,LongWritable> {
	private Text word = new Text();
	private final static LongWritable count = new LongWritable();
	 
	protected void map(LongWritable key, Text value, Context context)
			throws IOException, InterruptedException {
	
		String line = value.toString();
		String[] splstr = line.split(",");
		word.set(splstr[3]);								//set output key as the word itself
		count.set(Long.valueOf(splstr[4]).longValue());		//set output value as the number of occurrences of the word
		context.write(word, count);							//output the key,value pair
	}
}
