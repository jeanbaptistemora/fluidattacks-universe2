/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint @typescript-eslint/no-floating-promises:0 */
import type { TOptions } from "i18next";
import i18next, { t, use } from "i18next";
import { initReactI18next } from "react-i18next";

import { pageTexts } from "./en";

use(initReactI18next).init({
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
  t: (key: string[] | string, options?: TOptions): string => t(key, options),
};

export { i18next, translate };
