using System.Web.Mvc;

namespace EmptyMvcProject.Controllers
{
    public class HomeController : Controller
    {
        public ActionResult Index()
        {
            return View();
        }
    }
}