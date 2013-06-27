import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import org.apache.commons.lang.StringUtils;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
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
		return r;
	}

	public static class Point {
		public List<Double> arr;

		public Point(String str) {
			arr = new ArrayList();
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
			if (s == null || (s = s.trim()).isEmpty()) {
				break;
			}
			r.add(new KMeans.Point(s.split(":")[0]));
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
				if (minIndex == -1 || d < minDist) {
					minIndex = i;
					minDist = d;
				}
			}
			context.write(centroids.get(minIndex).toText(), value);
		}
	}

	public static class Reduce extends Reducer<Text, Text, Text, Text> {

		@Override
		public void reduce(Text key, Iterable<Text> values, Context context)
				throws IOException, InterruptedException {
			List<Double> sum = null;
			int nPoints = 0;
			double cost = 0;
			Point centroid = new Point(key);
			for (Text val : values) {
				++nPoints;
				Point p = new KMeans.Point(val);
				cost += KMeans.distance(centroid, p);
				if (sum == null) {
					sum = p.arr;
				} else {
					for (int i = 0; i < sum.size(); ++i) {
						sum.set(i, sum.get(i) + p.arr.get(i));
					}
				}

			}
			for (int i = 0; i < sum.size(); ++i) {
				sum.set(i, sum.get(i) / nPoints);
			}
			context.write(new Text(), new Text(StringUtils.join(sum, " ") + ":"
					+ cost));
		}
	}

	private static double computeCost(String file) throws IOException {
		double cost = 0;
		BufferedReader br = new BufferedReader(new FileReader(file));
		while (true) {
			String s = br.readLine();
			if (s == null || s.isEmpty()) {
				break;
			}
			cost += Double.parseDouble(s.split(":")[1]);
		}
		return cost;
	}

	public static final String ARG_CENTROID = "CENTROID";
	public static final int NUM_ITERATIONS = 21;

	/**
	 * The output of each iteration is under: baseDir/r%d. The output contains
	 * 10 lines, one centroid on each line, in the format CENTROID:COST
	 * 
	 */
	public static void main(String[] args) throws Exception {
		String baseDir = args[0];
		List<Double> costs = new ArrayList();
		for (int i = 1; i <= NUM_ITERATIONS; ++i) {
			Configuration conf = new Configuration();

			conf.set(ARG_CENTROID,
					String.format("%s/r%d/part-r-00000", baseDir, i - 1));
			Job job = new Job(conf, "KMeans");
			job.setJarByClass(KMeans.class);
			job.setOutputKeyClass(Text.class);
			job.setOutputValueClass(Text.class);

			job.setMapperClass(Map.class);
			job.setReducerClass(Reduce.class);

			job.setInputFormatClass(TextInputFormat.class);
			job.setOutputFormatClass(TextOutputFormat.class);

			FileInputFormat.addInputPath(job, new Path(baseDir + "/input"));
			FileOutputFormat.setOutputPath(job,
					new Path(String.format("%s/r%d", baseDir, i)));

			job.waitForCompletion(true);

			costs.add(computeCost(String.format("%s/r%d/part-r-00000", baseDir,
					i)));

		}
		for (int i = 0; i < costs.size(); ++i) {
			System.out.println(String.format("Cost in round %d: %f", i,
					costs.get(i)));
		}
		System.out.println(StringUtils.join(costs, ","));
	}
}
