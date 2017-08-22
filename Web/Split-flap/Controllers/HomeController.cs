using Newtonsoft.Json;
using Split_flap.Models;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Web.Mvc;

namespace Split_flap.Controllers
{
    public class HomeController : Controller
    {
        private string FileName = "history.txt";
        private MessageDBContext db = new MessageDBContext();

        public ActionResult Index()
        {
            return View();
        }

        private void CreateFileIfNecessary()
        {
            if (!System.IO.File.Exists(FileName))
            {
                System.IO.File.Create(FileName);
            }
        }

        //public string Messages()
        //{
        //    //CreateFileIfNecessary();
        //    //List<string> messages = new List<string>();
        //    //string line;
        //    //using (StreamReader readtext = new StreamReader(FileName, true))
        //    //{
        //    //    while ((line = readtext.ReadLine()) != null)
        //    //    {
        //    //        messages.Add(line);
        //    //    }
        //    //}
        //    //List<Message> messages = /*db.Messages.ToList()*/.Select(x => x.Content);
        //    return JsonConvert.SerializeObject(db.Messages.ToList());
        //}

        //[HttpPost]
        //public void Write(string message)
        //{
        //    CreateFileIfNecessary();
        //    using (StreamWriter writer = new StreamWriter(FileName, true))
        //    {
        //        writer.WriteLine(message);
        //    }
        //}
    }
}