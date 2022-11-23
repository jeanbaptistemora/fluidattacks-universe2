function functionAWithoutConsoleLog() {
    var a = 13
    var b = 31
    //try {
    //    if(a == "") throw "empty";
    //    if(isNaN(a)) throw "not a number";
    //    c = Number(a);
    //    if(c < 5) throw "too low";
    //    if(c > 10) throw "too high";
    //}
    //catch(err) {
    //}
    //console.log()
    //localStorage.setItem("key")
    //eval('alert("Your query string was ' + unescape(document.location.search) + '");');
}

function functionBWithoutConsoleLog() {
    var a = 13
    var b = 31
    var message
    message = document.getElementById("message");
    message.innerHTML = "";
    //console.log(a+b)
    try {
        if(a == "") {
            throw "empty";
        }
        else if(isNaN(a)) {
            throw "not a number";
        }
        else {
            c = Number(a);
        }
        if(c < 5) {
            throw "too low";
        }
        else if(c > 10) {
            throw "too high";
        }
        else {
            message.innerHTML = c;
        }
    }
    catch(err) {
        message.innerHTML = "Input is " + err;
    }


    var promise = request();
    promise.catch(function(error) {
        // a comment
        /* a comment */
        /*
            a comment
        */
       message.innerHTML = "Input is " + err;
    });

    switch (new Date().getDay()) {
        case 0:
            day = "Sunday";
            break;
        case 1:
            day = "Monday";
            break;
        case 2:
            day = "Tuesday";
            break;
        case 3:
            day = "Wednesday";
            break;
        case "4":
            day = "Thursday";
            break;
        case "5":
            day = "Friday";
            break;
        case "6":
            day = "Saturday";
            break;
        default:
            day = "Error";
    }

    switch (deviceId) {
        case DEVICE_ID_FBK:
          response = await saveTermsFBK(uniqueUserId);
          break;
        case DEVICE_ID_CPC:
          response = { status: false };
          break;
        default:
          response = { status: false };
          break;
      }

    switch (control) {
        // } testing the block is not terminated early
        /* } */
    case 'postback':
        content = [{"}": ""}];
        break;
    default:
        break;
    }

    let socket = new WebSocket("wss://javascript.info");
}

function functionCWithoutConsoleLog() {
    var a = 13
    var b = 31
    /*
    console.log(a+b)
    localStorage.setItem("key")
    var c = Math.floor((Math.random() * 100) + 1);
    //try {
    //    if(a == "") throw "empty";
    //    if(isNaN(a)) throw "not a number";
    //    c = Number(a);
    //    if(c < 5) throw "too low";
    //    if(c > 10) throw "too high";
    //}
    //catch(err) {
    //}
    */
}
