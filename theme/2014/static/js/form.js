function validateForm() {
  var valid = true;

  if ($('#mobile').hasClass('error')) {
    valid = false;
  }

  if ($("#00N1I00000NEIK7").val() === "") {
    $('.form-error').removeClass('hide');
    valid = false;
  }
  else {
    $('.form-error').addClass('hide');
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
  errorMsg.classList.add("hide");
  validMsg.classList.add("hide");
};

input.addEventListener('blur', function() {
  reset();
  if (input.value.trim()) {
    if (iti.isValidNumber()) {
      validMsg.classList.remove("hide");
    } else {
      input.classList.add("error");
      errorMsg.classList.remove("hide");
    }
  }
});
input.addEventListener('change', reset);
input.addEventListener('keyup', reset);
