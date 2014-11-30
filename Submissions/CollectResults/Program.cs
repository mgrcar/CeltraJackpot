using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace CollectResults
{
    class Program
    {
        static void Main(string[] args)
        {
            string resultsFolder = @"C:\work\celtrajackpot\Submissions\Results";
            string[] names = Directory.GetFiles(resultsFolder, "*.1.1.log").Select(x => new FileInfo(x).Name.Split('.')[0].ToUpper()).ToArray();
            foreach (string name in names)
            {
                Console.WriteLine("Processing " + name + " ...");
                int i = 1;
                int successes = 0;
                int failures = 0;
                List<int> rewards = new List<int>();
                while (Directory.GetFiles(resultsFolder, name + "." + i + ".*").Length > 0)
                {
                    int reward = 0;
                    for (int e = 1; e <= 10; e++)
                    {
                        string fileName = resultsFolder + @"\" + name + "." + i + "." + e;
                        if (File.Exists(fileName + ".done")) { successes++; }
                        if (File.Exists(fileName + ".err")) { failures++; }
                        if (File.Exists(fileName + ".rew")) 
                        {
                            reward += Convert.ToInt32(File.ReadAllText(fileName + ".rew"));
                        }
                    }
                    rewards.Add(reward);
                    i++;
                }
                Console.WriteLine("Successes:  {0}", successes);
                Console.WriteLine("Failures:   {0}", failures);
                Console.WriteLine("Avg reward: {0:0.00}", rewards.Average());
            }
        }
    }
}
