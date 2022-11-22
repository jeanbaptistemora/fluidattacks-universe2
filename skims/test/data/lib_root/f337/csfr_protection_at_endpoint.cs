namespace Controllers
{
    public class ExampleController : Controller
    {
        [HttpPost]
        [ValidateAntiforgeryToken]
        public ActionResult NotFail(anyModel obj)
        {
            return ExampleResponse(obj);
        }

        [HttpPost]
        public ActionResult Fail(anyModel obj)
        {
            return ExampleResponse(obj);
        }
    }
}
