using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using System.Web.Routing;

namespace CeltraJackpot
{
    public class RouteConfig
    {
        public static void RegisterRoutes(RouteCollection routes)
        {
            routes.IgnoreRoute("{resource}.axd/{*pathInfo}");

            routes.MapRoute(
                name: "Api1",
                url: "{instance}/{exampleNumber}/{action}",
                defaults: new { controller = "Api" },
                constraints: new { exampleNumber = "\\d+", action = "Machines|Pulls|Who|Reset" }
            );
            routes.MapRoute(
                name: "Api2",
                url: "{instance}/{exampleNumber}/{machineNumber}/{pullNumber}",
                defaults: new { controller = "Api", action = "Pull" },
                constraints: new { exampleNumber = "\\d+", machineNumber = "\\d+", pullNumber = "\\d+" }
            );
            routes.MapRoute(
                name: "Default",
                url: "{controller}/{action}",
                defaults: new { controller = "Home", action = "Index" }
            );
        }
    }
}