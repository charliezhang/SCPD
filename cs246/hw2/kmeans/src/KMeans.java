import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.StringTokenizer;

import org.apache.commons.lang.StringUtils;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;

public class KMeans {
	public static double distance(Point a, Point b) {
		double r = 0;
		for (int i = 0; i < a.arr.size(); ++i) {
			double d = a.arr.get(i) - b.arr.get(i);
			r += d * d;
		}
		return Math.sqrt(r);
	}

	public static class Point {
		public List<Double> arr;

		public Point(String str) {
			for (String s : str.split(" ")) {
				arr.add(Double.parseDouble(s));
			}
		}

		public Point(Text t) {
			this(t.toString());
		}

		@Override
		public String toString() {
			return StringUtils.join(arr, " ");
		}

		public Text toText() {
			return new Text(this.toString());
		}
	}

	public static List<Point> loadPointsFromFile(String file)
			throws IOException {
		List<Point> r = new ArrayList<Point>();
		BufferedReader br = new BufferedReader(new FileReader(file));
		while (true) {
			String s = br.readLine();
			if (s == null || s.isEmpty()) {
				break;
			}
			r.add(new KMeans.Point(s));
		}
		return r;
	}

	public static class Map extends Mapper<LongWritable, Text, Text, Text> {
		private List<Point> centroids;

		@Override
		protected void setup(Mapper.Context context) throws IOException {
			String file = context.getConfiguration().get(KMeans.ARG_CENTROID);
			centroids = KMeans.loadPointsFromFile(file);
		}

		@Override
		public void map(LongWritable key, Text value, Context context)
				throws IOException, InterruptedException {
			Point p = new KMeans.Point(value);
			double minDist = 0;
			int minIndex = -1;
			for (int i = 0; i < centroids.size(); ++i) {
				double d = KMeans.distance(centroids.get(i), p);
				if (minIndex == -1 || d < minDist)
			}
		}
	}

	public static class Reduce extends Reducer<Text, Text, LongWritable, Text> {

		@Override
		public void reduce(Text key, Iterable<IntWritable> values,
				Context context) throws IOException, InterruptedException {
			int sum = 0;
			for (IntWritable val : values) {
				sum += val.get();
			}
			context.write(key, new IntWritable(sum));
		}
	}

	public static final String ARG_CENTROID = "CENTROID";

	public static void main(String[] args) throws Exception {
		Configuration conf = new Configuration();
		
		conf.set(KMeans.ARG_CENTROID, )
		Job job = new Job(conf, "WordCount");
		job.setJarByClass(WordCount.class);
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(IntWritable.class);

		job.setMapperClass(Map.class);
		job.setReducerClass(Reduce.class);

		job.setInputFormatClass(TextInputFormat.class);
		job.setOutputFormatClass(TextOutputFormat.class);

		FileInputFormat.addInputPath(job, new Path(args[0]));
		FileOutputFormat.setOutputPath(job, new Path(args[1]));

		job.waitForCompletion(true);
	}
}
