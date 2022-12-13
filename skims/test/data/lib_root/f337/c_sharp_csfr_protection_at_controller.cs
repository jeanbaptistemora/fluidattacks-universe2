namespace Controllers
{
    [AutoValidateAntiforgeryToken]
    public class ExampleController : ControllerBase
    {
        [HttpPost]
        public ActionResult Example(anyModel obj)
        {
            return ExampleResponse(obj);
        }
    }

}
