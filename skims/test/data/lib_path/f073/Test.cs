class Test {
    static void Main() {
      switch (caseSwitch) {}
      switch (caseSwitch)
      {
          case 1:
              Console.WriteLine("Case 1");
          case 2:
              Console.WriteLine("Case 2");

                switch (caseSwitch)
                {
                    case 1 when 2:
                    case 2 when 3:
                        switch (caseSwitch)
                        {
                            case 1:
                            case 2:
                            default:
                                switch (caseSwitch)
                                {
                                    case 1:
                                    case 2:
                                        x;
                                }
                                break;
                        }
                        break;
                    case 2:
                        Console.WriteLine("Case 2");
                        break;
                    default:
                        Console.WriteLine("Default case");
                        break;
                }
          default:
              Console.WriteLine("Default case");
              break;
      }

      switch (caseSwitch)
      {
          case 1:
                    switch (caseSwitch)
                    {
                        case 1: Console.WriteLine("Case 1");
                        case 2: Console.WriteLine("Case 2");
                                break;
                    }
                  break;
          case 2:
              Console.WriteLine("Case 2");
              break;
      }


    }
}
