import i18next from "i18next";
import { reactI18nextModule } from "react-i18next";
import enTranslations from "./en";
import esTranslations from "./es";

const translate: i18next.i18n = i18next
  .use(reactI18nextModule)
  .init({
    interpolation: {
      escapeValue: false,
    },
    lng: localStorage.lang,
    resources: {
      en: { translation: enTranslations },
      es: { translation: esTranslations },
    },
  });

export = translate;
