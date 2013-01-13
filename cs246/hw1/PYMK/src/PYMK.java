import java.io.IOException;
import java.util.*;
import java.util.Map.Entry;
        
import org.apache.commons.lang.StringUtils;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.*;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
        
public class PYMK {
        
 public static class Map extends Mapper<LongWritable, Text, IntWritable, Text> {

    public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        String[] line = value.toString().split("\t");
        if (line.length != 2) {
          System.out.println("Mal-format data");
          return;
        }
        String[] friends = line[1].split(",");
        for (int i = 0; i < friends.length; ++i) {
        	for (int j = 0; j < friends.length; ++j) {
        		if (i != j) {
        		    context.write(
        		        new IntWritable(Integer.valueOf(friends[i]).intValue()),
        		        new Text(friends[j]));
        		}
        	}
        }
    }
 }
        
 public static class Reduce extends Reducer<IntWritable, Text, IntWritable, Text> {
	private static final int MAX_NUM_SUGGESTIONS = 10;
	
    public void reduce(IntWritable key, Iterable<Text> values, Context context)
      throws IOException, InterruptedException {
        HashMap<String, Integer> map = new HashMap<String, Integer>();
        for (Text val : values) {
        	String mapKey = val.toString();
        	if (!map.containsKey(mapKey)) {
        		map.put(mapKey, 0);
        	}
        	map.put(mapKey, ((Integer)map.get(mapKey)).intValue() + 1);
        }
        List<Entry<String, Integer>> list = new LinkedList<Entry<String, Integer>>(map.entrySet());
        Collections.sort(list, new Comparator<Entry<String, Integer>>() {
            public int compare(Entry<String, Integer> e1, Entry<String, Integer> e2) {
                return e2.getValue() - e1.getValue();
           }
        });
        int cnt = 0;
        List<String> suggestions = new LinkedList<String>();
        for (Iterator<Entry<String, Integer>> it = list.iterator(); it.hasNext();) {
        	Entry<String, Integer> entry = it.next();
        	suggestions.add(entry.getKey());
        	cnt++;
        	if (cnt >= MAX_NUM_SUGGESTIONS) {
        	  break;
        	}
        };
        context.write(key, new Text(StringUtils.join(suggestions, ",")));
    }
 }
        
 public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
        
    Job job = new Job(conf, "PeopleYouMayKnow");
    job.setJarByClass(PYMK.class);
    job.setOutputKeyClass(IntWritable.class);
    job.setOutputValueClass(Text.class);

    job.setMapperClass(Map.class);
    job.setReducerClass(Reduce.class);

    job.setInputFormatClass(TextInputFormat.class);
    job.setOutputFormatClass(TextOutputFormat.class);
        
    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));
        
    job.waitForCompletion(true);
 }
        
}