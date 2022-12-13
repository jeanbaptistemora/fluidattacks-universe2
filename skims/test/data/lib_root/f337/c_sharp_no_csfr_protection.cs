namespace Controllers
{
    public class ExampleController : Controller
    {
        [HttpPost]
        public ActionResult Example(anyModel obj)
        {
            return ExampleResponse(obj);
        }
    }
}
