using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Diagnostics;

namespace CollectResults
{
    static class Program
    {
        public static double StandardError(this IEnumerable<int> vals)
        {
            double avg = vals.Average();
            double n = vals.Count();
            double s = Math.Sqrt((1.0 / (n - 1.0)) * vals.Select(x => Math.Pow(x - avg, 2.0)).Sum());
            return s / Math.Sqrt(n);
        }

        static void Main(string[] args)
        {
            string resultsFolder = @"C:\work\celtrajackpot\Submissions\Results";
            StreamWriter w = new StreamWriter(@"C:\work\celtrajackpot\Submissions\results.json");
            Dictionary<string, int> results = new Dictionary<string, int>();
            string[] names = Directory.GetFiles(resultsFolder, "*.1.1.log").Select(x => new FileInfo(x).Name.Split('.')[0].ToUpper()).ToArray();
            w.WriteLine("[");
            foreach (string name in names)
            {
                w.WriteLine("{{\r\n\"name\":       \"{0}\",", name);
                Console.WriteLine("Processing {0} ...", name);
                int i = 1;
                int successes = 0;
                int failures = 0;
                List<int> rewards = new List<int>();
                while (Directory.GetFiles(resultsFolder, name + "." + i + ".*").Length > 0)
                {
                    int reward = 0;
                    int all = 0;
                    for (int e = 1; e <= 10; e++)
                    {
                        string fileName = resultsFolder + @"\" + name + "." + i + "." + e;
                        if (File.Exists(fileName + ".done")) { successes++; all++; }
                        if (File.Exists(fileName + ".err")) { failures++; }
                        if (File.Exists(fileName + ".rew")) 
                        {
                            if (File.Exists(fileName + ".done")) { results.Add(name + "." + i + "." + e, Convert.ToInt32(File.ReadAllText(fileName + ".rew"))); }
                            reward += Convert.ToInt32(File.ReadAllText(fileName + ".rew"));
                        }
                    }
                    if (all == 10) { rewards.Add(reward); }
                    i++;
                }
                w.WriteLine("\"successes\":  {0},", successes);
                w.WriteLine("\"failures\":   {0},", failures);
                w.WriteLine("\"completed\":  {0},", rewards.Count);
                Console.WriteLine("Successes:  {0}", successes);
                Console.WriteLine("Failures:   {0}", failures);
                Console.WriteLine("Completed:  {0}", rewards.Count);
                if (rewards.Count != 0) 
                {
                    w.WriteLine("\"reward\":     {0:0.00},", rewards.Average());
                    w.WriteLine("\"stderr\":     {0:0.00}", rewards.StandardError());
                    Console.WriteLine("Reward:     {0:0.00} ± {1:0.00}", rewards.Average(), rewards.StandardError());
                }
                w.WriteLine("},");
            }
            //foreach (string name in names)
            //{
            //    Console.WriteLine(name);
            //    for (int e = 1; e <= 10; e++)
            //    {
            //        Console.WriteLine("Ex " + e + ":");
            //        for (int i = 1; i <= 100; i++)
            //        {
            //            try
            //            {
            //                int val = results[name + "." + i + "." + e];
            //                Console.Write(val + " ");
            //            } 
            //            catch 
            //            {
            //            }
            //        }
            //        Console.WriteLine();
            //    }
            //}
            w.WriteLine("]");
            w.Close();
        }
    }
}
