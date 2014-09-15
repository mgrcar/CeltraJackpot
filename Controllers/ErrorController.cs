using System.Web.Mvc;

namespace CeltraJackpot.Controllers
{
    public class ErrorController : Controller
    {
        public ActionResult Index()
        {
            return Content("ERR", "text/plain");
        }
    }
}