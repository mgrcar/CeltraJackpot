using System.Web.Optimization;

namespace EmptyMvcProject
{
    public class BundleConfig 
    {
        public static void RegisterBundles(BundleCollection bundles)
        {
            bundles.IgnoreList.Clear(); // allow adding minified js files
            BundleTable.EnableOptimizations = true;
            // Styles
            // ...
            // Scripts
            // ...
        }
    }
}
