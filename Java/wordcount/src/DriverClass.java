import java.io.IOException;
import java.util.Date;
import java.util.Formatter;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
 
public class DriverClass {
 
public static void main(String[] args) throws IOException,
 InterruptedException, ClassNotFoundException {
 Configuration conf = new Configuration();
 
 	Job job = new Job(conf, "wordcount");
 
 	job.setJarByClass(DriverClass.class);
 
 	job.setOutputKeyClass(Text.class);
 	job.setOutputValueClass(LongWritable.class);
 
 	job.setInputFormatClass(TextInputFormat.class);
 	job.setOutputFormatClass(TextOutputFormat.class);
 
 	Formatter formatter = new Formatter();
 	String outpath = "Out" + formatter.format("%1$tm%1$td%1$tH%1$tM%1$tS", new Date());
 
 	FileInputFormat.setInputPaths(job, new Path(args[0]));
 	FileOutputFormat.setOutputPath(job, new Path(outpath));
 	
 	job.setMapperClass(MapClass.class);
 	job.setReducerClass(ReduceClass.class);
 	
 	System.out.println(job.waitForCompletion(true));
 }
}