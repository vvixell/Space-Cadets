using System;
using System.Net.Http;
using System.Threading.Tasks;
using System.Text.RegularExpressions;

namespace C1
{
    class Program
    {
        static void Main(string[] args)
        {
            string ID = string.Empty;

            bool Running = true;
            Console.WriteLine("Enter email ID: ");
            ID = Console.ReadLine();

            User user = FetchUserFromID(ID);

            Console.ReadLine();
        }

        /// <summary>
        /// Fetches the user information from the webpage.
        /// </summary>
        /// <param name="ID"></param>
        /// <returns>A new user object if found else returns null</returns>
        static User FetchUserFromID(string ID)
        {
            string URL = $"https://ecs.soton.ac.uk/people/{ID}";

            string Page;

            try
            {
                Page = GetWebpage(URL).Result;
                //Console.WriteLine(Page);
                
                int index1 = Page.IndexOf("\"@type\": \"Person\"");
                int index2 = Page.IndexOf("</script>");
                
                string[] JsonSeperated = Page.Substring(index1, index2 - index1).Split(',');
                string name = JsonSeperated[1].Split('"')[3];
                string email = JsonSeperated[4].Split('"')[3];
                string tel = JsonSeperated[6].Split('"')[3];
                
                User user = new User(ID, name, email, tel);
                user.PrintInfo();
                return user;
            }
            catch (Exception e)
            {
                Console.WriteLine("Could not find user");
            }

            

            return null;
        }

        static async Task<string> GetWebpage(string URL)
        {
            HttpClient httpClient = new HttpClient();

            return await httpClient.GetStringAsync(URL);
        }
    }

    class User
    {
        public string UserID;
        public string Name;
        public string Email;
        public string Tel;

        public User(string _UserId, string _Name, string _Email, string _Tel)
        {
            UserID = _UserId;
            Name = _Name;
            Email = _Email;
            Tel = _Tel;
        }

        public void PrintInfo()
        {
            Console.WriteLine($"\n- User INFO - \n UserId: {UserID} \n Name: {Name} \n Email: {Email} \n Telephone: {Tel}\n");
        }
    }
}