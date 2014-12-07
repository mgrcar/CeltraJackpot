using System.Web.Mvc;

namespace CeltraJackpot.Controllers
{
    public class HomeController : Controller
    {
        public ActionResult Index()
        {
            ViewBag.Title = "IZZIV 1: Jackpot";
            return View();
        }

        public ActionResult Results()
        {
            ViewBag.Title = "IZZIV 1: Jackpot";
            return View();
        }
    }
}