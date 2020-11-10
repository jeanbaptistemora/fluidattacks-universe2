import { default as $ } from "jquery";

import { logger, startBugsnag } from "./bugsnagErrorBoundary";

startBugsnag();

/* tslint:disable: no-unsafe-any
   this is needed so the plugin works propperly */

// tslint:disable-next-line: typedef
const extendedWindow =
  // tslint:disable-next-line: no-any
  window as typeof window & {[key: string]: any };

const validator: (() => void) = (): void => {
  // tslint:disable-next-line: prefer-const
  extendedWindow.validateForm = (): boolean => {
    let valid: boolean; valid = true;
    const captchaResponse: string = grecaptcha.getResponse();

    if ($("#COBJ1CF2")
        .hasClass("error")) {
      valid = false;
    }

    if ($("#COBJ1CF5")
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
};

try {
  validator();
} catch (error) {
  logger.error("Error executing validator() function", error);
}

// tslint:disable-next-line: no-any
const input: any = document.querySelector("#Mobile") as HTMLElement;
const country: HTMLElement = document.getElementById("Country") as HTMLElement;
// tslint:disable-next-line: no-any
const countryList: any = window.intlTelInputGlobals.getCountryData();
const errorMsg: HTMLElement = document.querySelector("#error-msg") as HTMLElement;
const validMsg: HTMLElement = document.querySelector("#valid-msg") as HTMLElement;

const fieldHandler: (() => void) = (): void => {
  const iti: intlTelInput.Plugin = window.intlTelInput(input, {
    // Rule disabled cause of a bug in TsLint
    // tslint:disable-next-line: typedef
    geoIpLookup(callback: (countryCode: string) => void) {
      // tslint:disable-next-line: no-empty
      $.get("https://ipinfo.io?token=8ff59332458d40", () => {}, "jsonp")
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
};

try {
  fieldHandler();
} catch (error) {
  logger.error("Error executing fieldHandler() function", error);
}

const selectedValue: (() => void) = (): void => {
  const opt: HTMLSelectElement = document.getElementById("LEADCF23") as HTMLSelectElement;
  const sel: string = opt.options[opt.selectedIndex].value;
  const selpoi: HTMLElement = document.querySelector(".poi") as HTMLSelectElement;

  sel !== "I want a service proposal" ?
  selpoi.classList.add("dn") :
  selpoi.classList.remove("dn");
};

const userSelection: (() => void) = (): void => {
  const mainSelectField: HTMLElement = document.getElementById("LEADCF23") as HTMLElement;

  mainSelectField.addEventListener("change", (event: Event) => {
    selectedValue();
  });
};

try {
  userSelection();
} catch (error) {
  logger.error("Error executing userSelection() function", error);
}
