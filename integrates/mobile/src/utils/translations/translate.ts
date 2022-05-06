import { locale } from "expo-localization";
import i18next from "i18next";
import { initReactI18next } from "react-i18next";

import { enTranslations } from "./en";

import { LOGGER } from "../logger";

// eslint-disable-next-line import/no-named-as-default-member
i18next
  .use(initReactI18next)
  .init({
    compatibilityJSON: "v3",
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
    // eslint-disable-next-line fp/no-throw
    throw error;
  });

export { i18next };
