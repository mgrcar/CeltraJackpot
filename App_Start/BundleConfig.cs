using System.Web.Optimization;

namespace CeltraJackpot
{
    public class BundleConfig 
    {
        public static void RegisterBundles(BundleCollection bundles)
        {
            bundles.IgnoreList.Clear(); // allow adding minified js files
            BundleTable.EnableOptimizations = true;
            // Styles
            bundles.Add(new StyleBundle("~/css/bootstrap").Include(
                "~/css/bootstrap.css"
                ));
            // Scripts
            bundles.Add(new ScriptBundle("~/js/jquery").Include(
                "~/js/jquery-2.1.0.min.js"
                ));
            bundles.Add(new ScriptBundle("~/js/bootstrap").Include(
                "~/js/bootstrap.js"
                ));
        }
    }
}
