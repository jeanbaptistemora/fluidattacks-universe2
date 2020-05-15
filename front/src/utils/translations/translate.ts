import i18next, { TOptions } from "i18next";
import { initReactI18next } from "react-i18next";
import rollbar from "../rollbar";
import enTranslations from "./en";

i18next
  .use(initReactI18next)
  .init({
    fallbackLng: "en",
    interpolation: {
      escapeValue: false,
    },
    lng: localStorage.lang,
    resources: {
      en: { translation: enTranslations },
    },
  })
  .catch((reason: string): void => {
    rollbar.error("There was an error initializing translations", reason);
  });

type translationFn = (key: string | string[], options?: TOptions) => string;

const translate: { t: translationFn } = {
  t: (key: string | string[], options?: TOptions): string => i18next.t(key, options),
};

export = translate;
