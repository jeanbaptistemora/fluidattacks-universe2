/* eslint @typescript-eslint/no-floating-promises:0 */
import type { TOptions } from "i18next";
import i18next from "i18next";
import { initReactI18next } from "react-i18next";
import { pageTexts } from "./en";

i18next.use(initReactI18next).init({
  fallbackLng: "en",
  interpolation: {
    escapeValue: false,
  },
  lng: "en",
  resources: {
    en: { translation: pageTexts },
  },
});

interface ITranslationFn {
  (key: string[] | string, options?: TOptions): string;
}

const translate: { t: ITranslationFn } = {
  t: (key: string[] | string, options?: TOptions): string =>
    i18next.t(key, options),
};

export { i18next, translate };
