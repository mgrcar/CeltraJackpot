﻿using System.Web.Mvc;
using System;
using System.IO;
using System.Configuration;

namespace CeltraJackpot.Controllers
{
    public class ApiController : Controller
    {
        private static string mOutputFolder
            = ConfigurationManager.AppSettings["OutputFolder"].TrimEnd('\\');
        private static Random mRng
            = new Random();

        private string GetFileName(string ext)
        {
            return mOutputFolder + "\\" + Request.RawUrl.ToLower().Split('/')[2] + "." + ext;
        }

        private void WriteMsg(string fileNameExt, string msg, DateTime time)
        {
            using (StreamWriter w = new StreamWriter(GetFileName(fileNameExt), /*append=*/true))
            {
                w.WriteLine("{0:dd-MM HH:mm:ss} " + msg, time);
            }
        }

        private void WriteLogMsg(string msg)
        {
            WriteMsg("log", msg, DateTime.Now);
        }

        private void WriteErrMsg(string msg)
        {
            DateTime time = DateTime.Now;
            WriteMsg("err", msg, time);
            WriteMsg("log", "ERR " + msg, time);
        }

        private void Done()
        {
            WriteMsg("done", "", DateTime.Now);
        }

        private int GetExpectedPullNumber()
        {
            int pull = 1;
            try { pull = Convert.ToInt32(System.IO.File.ReadAllText(GetFileName("pull"))); } catch { }
            return pull;        
        }

        private void IncExpectedPullNumber(int expectedPullNumber)
        {
            System.IO.File.WriteAllText(GetFileName("pull"), (expectedPullNumber + 1).ToString());
        }

        private void IncReward()
        {
            int rew = 0;
            try { rew = Convert.ToInt32(System.IO.File.ReadAllText(GetFileName("rew"))); } catch { }
            System.IO.File.WriteAllText(GetFileName("rew"), (rew + 1).ToString());
        }

        private int _Pulls(int exampleNumber)
        {
            int pulls = -1;
            switch (exampleNumber)
            {
                case 1:
                    pulls = 500;
                    break;
                case 2:
                    pulls = 10000;
                    break;
                case 3:
                    pulls = 1000;
                    break;
                case 4:
                    pulls = 10000;
                    break;
                case 5:
                    pulls = 10000;
                    break;
                // time-dependent machines
                case 6:
                    pulls = 1000;
                    break;
                case 7:
                    pulls = 15000;
                    break;
                case 8:
                    pulls = 3000;
                    break;
                case 9:
                    pulls = 30000;
                    break;
                case 10:
                    pulls = 30000;
                    break;
            }
            return pulls;
        }

        public object Pulls(int exampleNumber)
        {
            WriteLogMsg(string.Format("Pulls({0}) was called.", exampleNumber));
            int pulls = _Pulls(exampleNumber);
            if (pulls == -1) { WriteErrMsg("Invalid example number in pulls."); return Content("ERR", "text/plain"); }
            return Content(pulls.ToString(), "text/plain");
        }

        public object Machines(int exampleNumber)
        {
            WriteLogMsg(string.Format("Machines({0}) was called.", exampleNumber));
            int machines;
            switch (exampleNumber)
            {
                case 1:
                    machines = 2;
                    break;
                case 2:
                    machines = 2;
                    break;
                case 3:
                    machines = 3;
                    break;
                case 4:
                    machines = 4;
                    break;
                case 5:
                    machines = 10;
                    break;
                // time-dependent machines
                case 6:
                    machines = 2;
                    break;
                case 7:
                    machines = 2;
                    break;
                case 8:
                    machines = 3;
                    break;
                case 9:
                    machines = 4;
                    break;
                case 10:
                    machines = 10;
                    break;
                default:
                    WriteErrMsg("Invalid example number in machines.");
                    return Content("ERR", "text/plain");
            }
            return Content(machines.ToString(), "text/plain");
        }

        public object Pull(int exampleNumber, int machineNumber, int pullNumber)
        {
            WriteLogMsg(string.Format("Pull({0},{1},{2}) was called.", exampleNumber, machineNumber, pullNumber));
            int expectedPullNumber = GetExpectedPullNumber();
            if (pullNumber != expectedPullNumber) { WriteErrMsg(string.Format("Invalid pull number (expected: {0}, actual: {1}).", expectedPullNumber, pullNumber)); return Content("ERR " + pullNumber + " <> " + expectedPullNumber, "text/plain"); }
            IncExpectedPullNumber(expectedPullNumber);
            double p = -1;
            int pulls = _Pulls(exampleNumber);
            if (pullNumber <= 0 || pullNumber > pulls) { WriteErrMsg("Pull number out of bounds."); return Content("ERR", "text/plain"); }
            double progress = (double)pullNumber / (double)pulls;
            switch (exampleNumber) 
            { 
                case 1: // 300 of 500 pulls
                    switch (machineNumber) 
                    { 
                        case 1:
                            p = 0.40; 
                            break;
                        case 2:
                            p = 0.60; 
                            break;
                    }
                    break;
                case 2: // 300 of 10,000 pulls
                    switch (machineNumber) 
                    {
                        case 1:
                            p = 0.030; 
                            break;
                        case 2:
                            p = 0.015; 
                            break;
                    }
                    break;
                case 3: // 200 of 1,000 pulls
                    switch (machineNumber)
                    {
                        case 1:
                            p = 0.20; 
                            break;
                        case 2:
                            p = 0.15; 
                            break;
                        case 3:
                            p = 0.10; 
                            break;
                    }
                    break;
                case 4: // 240 of 10,000 pulls
                    switch (machineNumber) 
                    {
                        case 1:
                            p = 0.020; 
                            break;
                        case 2:
                            p = 0.019; 
                            break;
                        case 3:
                            p = 0.024; 
                            break;
                        case 4:
                            p = 0.023; 
                            break;
                    }
                    break;
                case 5: // 130 of 10,000 pulls
                    switch (machineNumber) 
                    {
                        case 1:
                            p = 0.010;
                            break;
                        case 2:
                            p = 0.010; 
                            break;
                        case 3:
                            p = 0.010; 
                            break;
                        case 4:
                            p = 0.010; 
                            break;
                        case 5:
                            p = 0.010;
                            break;
                        case 6:
                            p = 0.010; 
                            break;
                        case 7:
                            p = 0.010; 
                            break;
                        case 8:
                            p = 0.010; 
                            break;
                        case 9:
                            p = 0.010; 
                            break;
                        case 10:
                            p = 0.013; 
                            break;
                    }
                    break;
                // time-dependent machines
                case 6: // 600 of 1,000 pulls
                    switch (machineNumber)
                    {
                        case 1:
                            if (progress < 0.5) { p = 0.6; }
                            else { p = 0.4; }
                            break;
                        case 2:
                            if (progress < 0.5) { p = 0.4; } 
                            else { p = 0.6; }
                            break;
                    }
                    break;
                case 7: // 525 of 15,000 pulls
                    switch (machineNumber)
                    {
                        case 1:
                            if (progress < 0.25) { p = 0.030; }
                            else if (progress < 0.75) { p = 0.020; }
                            else { p = 0.030; }
                            break;
                        case 2:
                            if (progress < 0.25) { p = 0.015; }
                            else if (progress < 0.75) { p = 0.040; }
                            else { p = 0.015; }
                            break;
                    }
                    break;
                case 8: // 675 of 3,000 pulls
                    switch (machineNumber)
                    {
                        case 1:
                            if (progress < 0.5) { p = 0.2; }
                            else if (progress < 0.75) { p = 0; }
                            else { p = 0.2; }
                            break;
                        case 2:
                            if (progress < 0.5) { p = 0.15; }
                            else if (progress < 0.75) { p = 0.3; }
                            else { p = 0; }
                            break;
                        case 3:
                            if (progress < 0.5) { p = 0.1; }
                            else if (progress < 0.75) { p = 0.1; }
                            else { p = 0.1; }
                            break;
                    }
                    break;
                case 9: // 414 of 30,000 pulls 
                    switch (machineNumber)
                    { 
                        case 1:
                            if (progress < 0.4) { p = 0; }
                            else { p = 0.02; }
                            break;
                        case 2:
                            if (progress < 0.4) { p = 0; }
                            else { p = 0; }
                            break;
                        case 3:
                            if (progress < 0.4) { p = 0; }
                            else { p = 0.023; }
                            break;
                        case 4:
                            if (progress < 0.4) { p = 0; }
                            else { p = 0; }
                            break;
                    }
                    break;
                case 10: // 540 of 30,000 pulls
                    switch (machineNumber)
                    { 
                        case 1:
                            if (progress < 0.2) { p = 0.01; }
                            else if (progress < 0.4) { p = 0.02; }
                            else if (progress < 0.8) { p = 0.01; }
                            else { p = 0.01; }
                            break;
                        case 2:
                            if (progress < 0.2) { p = 0.01; }
                            else if (progress < 0.4) { p = 0.01; }
                            else if (progress < 0.8) { p = 0.02; }
                            else { p = 0.01; }
                            break;
                        case 3:
                            if (progress < 0.2) { p = 0.01; }
                            else if (progress < 0.4) { p = 0.02; }
                            else if (progress < 0.8) { p = 0.01; }
                            else { p = 0.01; }
                            break;
                        case 4:
                            if (progress < 0.2) { p = 0.01; }
                            else if (progress < 0.4) { p = 0.01; }
                            else if (progress < 0.8) { p = 0.01; }
                            else { p = 0.02; }
                            break;
                        case 5:
                            if (progress < 0.2) { p = 0.01; }
                            else if (progress < 0.4) { p = 0.01; }
                            else if (progress < 0.8) { p = 0.01; }
                            else { p = 0.02; }
                            break;
                        case 6:
                            if (progress < 0.2) { p = 0.01; }
                            else if (progress < 0.4) { p = 0.01; }
                            else if (progress < 0.8) { p = 0.01; }
                            else { p = 0.02; }
                            break;
                        case 7:
                            if (progress < 0.2) { p = 0.01; }
                            else if (progress < 0.4) { p = 0.02; }
                            else if (progress < 0.8) { p = 0.01; }
                            else { p = 0.01; }
                            break;
                        case 8:
                            if (progress < 0.2) { p = 0.01; }
                            else if (progress < 0.4) { p = 0.02; }
                            else if (progress < 0.8) { p = 0.01; }
                            else { p = 0.01; }
                            break;
                        case 9:
                            if (progress < 0.2) { p = 0.01; }
                            else if (progress < 0.4) { p = 0.01; }
                            else if (progress < 0.8) { p = 0.02; }
                            else { p = 0.01; }
                            break;
                        case 10:
                            if (progress < 0.2) { p = 0.01; }
                            else if (progress < 0.4) { p = 0.01; }
                            else if (progress < 0.8) { p = 0.02; }
                            else { p = 0.01; }
                            break;                    
                    }
                    break;
            }
            if (p == -1) { WriteErrMsg("Invalid example number and/or machine number."); return Content("ERR", "text/plain"); }
            // generate reward randomly
            int reward = mRng.NextDouble() < p ? 1 : 0;
            if (reward == 1) { IncReward(); }
            if (pullNumber == pulls) { Done(); }
            return Content(reward.ToString(), "text/plain");
        }
    }
}
