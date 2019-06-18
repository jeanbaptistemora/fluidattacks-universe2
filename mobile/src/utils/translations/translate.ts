
import * as Localization from "expo-localization";
import i18next from "i18next";
import { initReactI18next } from "react-i18next";
import { ToastAndroid } from "react-native";

import { enTranslations } from "./en";

i18next
  .use(initReactI18next)
  .init({
    fallbackLng: "en",
    interpolation: {
      escapeValue: false,
    },
    lng: Localization.locale,
    resources: {
      en: { translation: enTranslations },
    },
  })
  .catch((error: Error): void => {
    ToastAndroid.show("Oops! There was an error initializing translations.", ToastAndroid.SHORT);
    throw error;
  });

type translationKey = string | TemplateStringsArray;
type translationOpts = string | i18next.TOptions<object>;
type translationFunction = (key: translationKey | translationKey[], options?: translationOpts) => string;

export const translate: { t: translationFunction } = {
  t: (key: translationKey | translationKey[], options?: translationOpts): string => i18next.t(key, options),
};
