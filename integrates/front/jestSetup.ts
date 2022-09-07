/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint-disable fp/no-mutating-methods
  --------
  Since most Jest mocks override/mutate properties, we need to disable the above rules.
*/
import fetchMock from "fetch-mock";
import "@testing-library/jest-dom";

// Mock mixpanel
jest.mock("mixpanel-browser");

// Mock fetch
Object.defineProperty(global, "fetch", { value: fetchMock, writable: true });

// Mock i18n
jest.mock(
  "react-i18next",
  (): Record<string, unknown> => ({
    ...jest.requireActual("react-i18next"),
    useTranslation: (): Record<string, unknown> => ({
      t: (key: string): string => key,
    }),
  })
);

// Mock bugsnag
jest.mock("@bugsnag/js");

// Set max timeout from 5000
const newMaxTime: number = 15000;
jest.setTimeout(newMaxTime);

// Mock matchMedia
Object.defineProperty(window, "matchMedia", {
  value: jest.fn().mockImplementation(
    (query: string): MediaQueryList => ({
      addEventListener: jest.fn(),
      // Deprecated
      addListener: jest.fn(),
      dispatchEvent: jest.fn(),
      matches: false,
      media: query,
      onchange: jest.fn(),
      removeEventListener: jest.fn(),
      // Deprecated
      removeListener: jest.fn(),
    })
  ),
  writable: true,
});

/**
 * Mock announcekit
 * @see https://github.com/announcekitapp/announcekit-react/issues/8
 */
jest.mock("announcekit-react", (): React.ReactNode => "mocked");
