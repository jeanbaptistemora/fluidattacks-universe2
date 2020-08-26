class SwitchDefaultClose{
   public static void main(String args[]){
      String monthString;
      switch (month) {
         case 1:  monthString = "January";
                  break;
         case 2:  monthString = "February";
                  break;
         case 3:  monthString = "March";
                  break;
         case 4:  monthString = "April";
                  break;
         case 5:  monthString = "May";
                  break;
         case 6:  monthString = "June";
                  break;
         case 7:  monthString = "July";
                  break;
         case 8:  monthString = "August";
                  break;
         case 9:  monthString = "September";
                  break;
         case 10: monthString = "October";
                  break;
         case 11: monthString = "November";
                  break;
         case 12: monthString = "December";
                  dummyString = "default";
                  dummyString = "block should not end here }";
                  // default
                  /* default */
                  // block should not end here }
                  /* block should not end here } */
                  break;
         default: monthString = "Invalid month";
                  break;
     }

     switch (month + somethingWithParens("default")) { /* default } */ case 1: monthString = "January"; break; default: monthString = "default"; dummyString = "block should not end here }"; throw } //default

   }
}
