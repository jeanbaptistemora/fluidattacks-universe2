import java.util.ArrayList;
import java.util.Iterator;

class Role
{
   private String name;
   private ArrayList subjects = new ArrayList();
   public Role(String n)
   {
     name = n;
   }
   public String getName()
   {
     return name;
   }
   public void addSubject(Subject s)
   {
     subjects.add(s);
   }
   public boolean contains(Subject s0)
   {
     Iterator i = subjects.iterator();
     while(i.hasNext())
     {
       Subject s = (Subject) i.next();
       if(s.equals(s0))
       {
         return true;
       }
     }
     return false;
   }
   public boolean equals(Role r)
   {
     return (r.name.equals(name));
   }
}
