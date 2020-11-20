import { Logger } from "utils/logger";
import type { TOptions } from "i18next";
import { enTranslations } from "utils/translations/en";
import i18next from "i18next";
import { initReactI18next } from "react-i18next";

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

export { i18next, translate };
