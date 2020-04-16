import { default as $ } from "jquery";

/* tslint:disable: no-unsafe-any
   this is needed so the plugin works propperly */

// tslint:disable-next-line: typedef
const extendedWindow =
  // tslint:disable-next-line: no-any
  window as typeof window & {[key: string]: any };

// tslint:disable-next-line: prefer-const
extendedWindow.validateForm = (): boolean => {
  let valid: boolean; valid = true;
  const captchaResponse: string = grecaptcha.getResponse();

  if ($("#mobile")
      .hasClass("error")) {
    valid = false;
  }

  if ($("#00N1I00000NEIK7")
      .val() === "") {
    $(".form-error")
      .removeClass("dn");
    valid = false;
  } else {
    $(".form-error")
      .addClass("dn");
  }

  if (captchaResponse.length === 0) {
    valid = false;
    alert("You must verify the Captcha first");
  }

  return valid;
};

// tslint:disable-next-line: no-any
const input: any = document.querySelector("#mobile") as HTMLElement;
const country: HTMLElement = document.getElementById("country") as HTMLElement;
// tslint:disable-next-line: no-any
const countryList: any = window.intlTelInputGlobals.getCountryData();
const errorMsg: HTMLElement = document.querySelector("#error-msg") as HTMLElement;
const validMsg: HTMLElement = document.querySelector("#valid-msg") as HTMLElement;

const iti: intlTelInput.Plugin = window.intlTelInput(input, {
  // Rule disabled cause of a bug in TsLint
  // tslint:disable-next-line: typedef
  geoIpLookup(callback: (countryCode: string) => void) {
    // tslint:disable-next-line: no-empty
    $.get("https://ipinfo.io", () => {}, "jsonp")
    .always((resp: {[country: string]: string}) => {
      // tslint:disable-next-line: strict-boolean-expressions
      const countryCode: string = (resp && resp.country) ? resp.country : "";
      let i: number;
      for (i = 0; i < countryList.length; i += 1) {
        if (countryCode.toLowerCase() === countryList[i].iso2) {
          country.setAttribute("value", countryList[i].name.split(" ")[0]);
          break;
        }
      }
      callback(countryCode);
    });
  },
  hiddenInput: "mobile",
  initialCountry: "auto",
  separateDialCode: true,
  utilsScript: "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/14.0.10/js/utils.js",
});

const reset: (() => void) = (): void => {
  input.classList.remove("error");
  errorMsg.classList.add("dn");
  validMsg.classList.add("dn");
};

input.addEventListener("blur", () => {
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
input.addEventListener("change", reset);
input.addEventListener("keyup", reset);
