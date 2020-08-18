import { Logger } from "../logger";
import { enTranslations } from "./en";
import { initReactI18next } from "react-i18next";
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
    Logger.warning("There was an error initializing translations", reason);
  });

interface ITranslationFn {
  (key: string | string[], options?: TOptions): string;
}

const translate: { t: ITranslationFn } = {
  t: (key: string | string[], options?: TOptions): string =>
    i18next.t(key, options),
};

/*
 * I'll change every import of this file to named import and use the
 * useTranslation hook when it is posible.
 */
// eslint-disable-next-line import/no-default-export
export default translate;
