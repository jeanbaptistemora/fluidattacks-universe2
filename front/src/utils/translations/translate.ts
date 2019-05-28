import i18next from "i18next";
import rollbar from "../rollbar";
import enTranslations from "./en";

i18next
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

type translationFn = (key: string | string[], options?: i18next.TranslationOptions) => string;

const translate: { t: translationFn } = {
  t: (key: string | string[], options?: i18next.TranslationOptions): string => i18next.t(key, options),
};

export = translate;
