using System.Web.Mvc;
using Newtonsoft.Json;

namespace EmptyMvcProject.Controllers
{
    public class ApiController : Controller
    {
        [ValidateInput(false)] 
        public object Test(string val)
        {
            // return JSON (proper way)
            return Content(JsonConvert.SerializeObject(new { val = val }, Formatting.Indented), "application/json");
        }
    }
}
