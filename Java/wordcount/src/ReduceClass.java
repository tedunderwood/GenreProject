import java.io.IOException;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
 
public class ReduceClass extends
 Reducer<Text, LongWritable, Text, LongWritable> {
 protected void reduce(Text key, Iterable<LongWritable> values,
 Context context) throws IOException, InterruptedException {
 long sum = 0;
 for (LongWritable value : values) {				//add list of values to create aggregate count per word
	 sum += value.get();
 }
 context.write(key, new LongWritable(sum));			//output the word and its new count
 }
}