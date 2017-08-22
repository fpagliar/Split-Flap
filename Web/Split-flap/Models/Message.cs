using System;
using System.Data.Entity;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace Split_flap.Models
{
    public class Message
    {
        [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
        public int ID { get; set; }
        public string Content { get; set; }
        [DataType(DataType.Date)]
        public DateTime CreatedOn { get; set; }

        public Message()
        {
            this.CreatedOn = DateTime.Now;
        }
    }
    public class MessageDBContext : DbContext
    {
        public DbSet<Message> Messages { get; set; }
    }
}