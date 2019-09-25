function validateForm() {
  var valid = true;
  var captcha_response = grecaptcha.getResponse();

  if ($('#mobile').hasClass('error')) {
    valid = false;
  }

  if ($("#00N1I00000NEIK7").val() === "") {
    $('.form-error').removeClass('dn');
    valid = false;
  }
  else {
    $('.form-error').addClass('dn');
  }

  if(captcha_response.length == 0){
    valid = false;
    alert("You must verify the Captcha first");
  }

  return valid;
}

var input   = document.querySelector("#mobile"),
    country = document.getElementById('country'),
    countryList = window.intlTelInputGlobals.getCountryData(),
    errorMsg = document.querySelector("#error-msg"),
    validMsg = document.querySelector("#valid-msg");

var iti = window.intlTelInput(input, {
  initialCountry: "auto",
  geoIpLookup: function(callback) {
    $.get("https://ipinfo.io", function() {}, "jsonp").always(function(resp) {
      var countryCode = (resp && resp.country) ? resp.country : "";
      for (i = 0; i < countryList.length; i++) {
        if (countryCode.toLowerCase() == countryList[i].iso2) {
          country.setAttribute('value', countryList[i].name.split(' ')[0]);
          break;
        }
      }
      callback(countryCode);
    });
  },
  hiddenInput: "mobile",
  separateDialCode: true,
  utilsScript: "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/14.0.10/js/utils.js",
});

var reset = function() {
  input.classList.remove("error");
  errorMsg.classList.add("dn");
  validMsg.classList.add("dn");
};

input.addEventListener('blur', function() {
  reset();
  if (input.value.trim()) {
    if (iti.isValidNumber()) {
      validMsg.classList.remove("dn");
    } else {
      input.classList.add("error");
      errorMsg.classList.remove("dn");
    }
  }
});
input.addEventListener('change', reset);
input.addEventListener('keyup', reset);
