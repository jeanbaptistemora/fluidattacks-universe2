import { enTranslations } from "./en";
import { initReactI18next } from "react-i18next";
import rollbar from "../rollbar";
import i18next, { TOptions } from "i18next";

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

interface ITranslationFn {
  (key: string | string[], options?: TOptions): string;
}

const translate: { t: ITranslationFn } = {
  t: (key: string | string[], options?: TOptions): string =>
    i18next.t(key, options),
};

export default translate;
