import { locale } from "expo-localization";
import i18next from "i18next";
import { initReactI18next } from "react-i18next";

import { LOGGER } from "../logger";

import { enTranslations } from "./en";

i18next
  .use(initReactI18next)
  .init({
    fallbackLng: "en",
    lng: locale,
    react: {
      useSuspense: false,
    },
    resources: {
      en: { translation: enTranslations },
    },
  })
  .catch((error: Error): void => {
    LOGGER.warning("Couldn't initialize translations", error);
    throw error;
  });

export { i18next };
