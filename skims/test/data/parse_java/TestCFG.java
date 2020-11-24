import org.apache.logging.log4j.Logger;
import org.apache.logging.log4j.LogManager;

public class Test {

  public static void main(String[ ] args) {
    boolean isCar = true;
    String vehicle = "Car";
    try {
      int[] myNumbers = {1, 2, 3};
      System.out.println(myNumbers[10]);
    } catch (IndexException e) {
      if (e.toString() == "Error"){
        System.out.println("Error");
      }
      e.printStackTrace();
    }

    if(isCar)
    {
    	System.out.println("I am a Car");
    }

    if(isCar)
    {
    	System.out.println("I am a Car");
    }
    else
    {
    	System.out.println("I am a Truck");
    }

    if(vehicle="Car")
    {
    	System.out.println("I am a Car");
    }
    else if(vehicle="Truck")
    {
    	System.out.println("I am a Truck");
    }
    else
    {
    	System.out.println("I am a Bike");
    }

    int age = 3;
    String yourAge;
    switch (age) {
        case 1:  System.out.println("You are one yr old");
                 break;
        case 2:  System.out.println("You are two yr old");
                 break;
        case 3:  System.out.println("You are three yr old");
                 break;
        default: System.out.println("You are more than three yr old");
                 break;
    }

    int age = 2;
    String yourAge;
    switch (age) {
        case 1:  System.out.println("You are one yr old");
        case 2:  System.out.println("You are two yr old");
        case 3:  System.out.println("You are three yr old");
        default: System.out.println("You are more than three yr old");
			break;
    }

	int age = 2;
	String yourAge;
	switch (age) {
		case 1:
		case 2:
		case 3: System.out.println("You are three or less than three yr old");
			break;
		case 4:
		case 5:
		case 6: System.out.println("You are six or less than six yr old");
			break;
		default: System.out.println("You are more than six yr old");
			break;
	}

    int counter = 0;
    while(counter < 5) {
        System.out.println("Inside the while loop, counting: " + counter);
        counter++;
    }

    int counter = 0;
    do {
        System.out.println("Inside the while loop, counting: " + counter);
        counter++;
    } while(counter < 5);

    for(int i=1; i<=5; i++){
    	  System.out.println("Printing using for loop. Count is: " + i);
    }

    String[] people = {"Vivek","Kavya","Aryan"};
    for (String person : people) {
    	System.out.println("Hi, I am " + person);
    }

    for(int i=1; i<=5; i++){
    	if(i==3)
    	{
    		System.out.println("Breaking the for loop.");
    		break;
    	}
    	System.out.println("Printing using for loop. Count is: " + i);
    }

    int counter = 0;
    while(counter < 5) {
    	if(counter==3)
    	{
    		System.out.println("Breaking the for loop.");
    		break;
    	}
        System.out.println("Inside the while loop, counting: " + counter);
        counter++;
    }

    int[] nums = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
    for (int i = 0; i < nums.length; i++) {
    	if (nums[i] % 2 != 0) {
    		continue;
    	}
    	System.out.println(nums[i] + " is even");
    }

	int[][] nums = { {1, 3, 7, 5},
					 {5, 8, 4, 6},
					 {7, 4, 2, 9} };
	int search = 8;

	for (int i = 0; i < nums.length; i++) {
		for (int j = 0; j < nums[i].length; j++) {
			if (nums[i][j] == search) {
				System.out.println(
					"Found " + search + " at position " + i + "," + j);
				break;
			}
		}
	}

  try {int j = 0;} catch (E e) {log(e);} catch (E2 e2) {log2(e);};
  try {int j = 0;} catch (E e) {log(e);};
  try {int j = 0;} finally {log(e);};
  try (T r = 0) {int j = 0;};
  }
}
