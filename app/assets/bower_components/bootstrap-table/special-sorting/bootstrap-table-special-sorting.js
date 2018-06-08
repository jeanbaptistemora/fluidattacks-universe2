function lastLogin(a, b) {
    function AlphanumericToNumber(s) {
        val=s.split(" ");
        if (val[1]==="day(s)" || val[1]==="dia(s)"){
          aux=300;
        } else if (val[1]==="hour(s)" || val[1]==="hora(s)")
        {
          aux=200;
        } else if (val[0]==="-")
        {
          return 0;
        }
        else {
          aux=100;
        }
        return parseInt(val[0], 10) + aux;
    }
    return AlphanumericToNumber(a) - AlphanumericToNumber(b);
}
