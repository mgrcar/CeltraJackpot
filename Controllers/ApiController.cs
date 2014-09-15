using System.Web.Mvc;

namespace CeltraJackpot.Controllers
{
    public class ApiController : Controller
    {
        public object Pulls(int exampleNumber)
        {
            return Content(string.Format("{0}/pulls", exampleNumber), "text/plain");
        }

        public object Machines(int exampleNumber)
        {
            return Content(string.Format("{0}/machines", exampleNumber), "text/plain");
        }

        public object Pull(int exampleNumber, int machineNumber, int pullNumber)
        {
            return Content(string.Format("{0}/{1}/{2}", exampleNumber, machineNumber, pullNumber), "text/plain");
        }
    }
}
