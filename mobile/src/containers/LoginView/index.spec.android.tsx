import { mount, ReactWrapper } from "enzyme";
import { FetchMockStatic } from "fetch-mock";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { I18nextProvider } from "react-i18next";
import { Linking } from "react-native";
import { Button, Provider as PaperProvider } from "react-native-paper";
import { NativeRouter } from "react-router-native";
import wait from "waait";

import { i18next } from "../../utils/translations/translate";

import { LoginView } from "./index";
import { checkPlayStoreVersion } from "./version";

jest.mock("./version", (): Dictionary => ({ checkPlayStoreVersion: jest.fn() }));
const originalVersion: { checkPlayStoreVersion(): Promise<boolean> } = jest.requireActual("./version");

jest.mock("expo-constants", (): Dictionary => ({
  ...jest.requireActual("expo-constants"),
  manifest: {
    ...jest.requireActual<Dictionary>("expo-constants").manifest,
    android: {
      package: "com.fluidattacks.integrates",
    },
    version: "20.06.1337",
  },
}));

const mockedFetch: FetchMockStatic = fetch as typeof fetch & FetchMockStatic;

describe("LoginView", (): void => {
  afterEach((): void => {
    jest.clearAllMocks();
    mockedFetch.reset();
  });

  it("should display update dialog", async (): Promise<void> => {
    (checkPlayStoreVersion as jest.Mock).mockResolvedValue(true);

    const wrapper: ReactWrapper = mount(
      <PaperProvider>
        <I18nextProvider i18n={i18next}>
          <NativeRouter initialEntries={["/"]}>
            <LoginView />
          </NativeRouter>
        </I18nextProvider>
      </PaperProvider>,
    );
    expect(wrapper)
      .toHaveLength(1);

    await act(async (): Promise<void> => { await wait(0); wrapper.update(); });

    expect(wrapper
      .find("googleButton")
      .at(0)
      .prop("disabled"))
      .toEqual(true);
    expect(wrapper
      .find("Dialog")
      .at(0)
      .prop("visible"))
      .toEqual(true);
  });

  it("should not display update dialog", async (): Promise<void> => {
    (checkPlayStoreVersion as jest.Mock).mockResolvedValue(false);

    const wrapper: ReactWrapper = mount(
      <PaperProvider>
        <I18nextProvider i18n={i18next}>
          <NativeRouter initialEntries={["/"]}>
            <LoginView />
          </NativeRouter>
        </I18nextProvider>
      </PaperProvider>,
    );
    expect(wrapper)
      .toHaveLength(1);

    await act(async (): Promise<void> => { await wait(0); wrapper.update(); });

    expect(wrapper
      .find("googleButton")
      .at(0)
      .prop("disabled"))
      .toEqual(false);
    expect(wrapper
      .find("Dialog")
      .at(0)
      .prop("visible"))
      .toEqual(false);
  });

  it("should open google play store", async (): Promise<void> => {
    (checkPlayStoreVersion as jest.Mock).mockResolvedValue(true);
    (Linking.openURL as jest.Mock).mockImplementation((): Promise<void> => Promise.resolve());

    const wrapper: ReactWrapper = mount(
      <PaperProvider>
        <I18nextProvider i18n={i18next}>
          <NativeRouter initialEntries={["/"]}>
            <LoginView />
          </NativeRouter>
        </I18nextProvider>
      </PaperProvider>,
    );
    expect(wrapper)
      .toHaveLength(1);

    await act(async (): Promise<void> => { await wait(0); wrapper.update(); });

    const updateBtn: ReactWrapper<React.ComponentProps<typeof Button>> = wrapper
      .find("Dialog")
      .find<React.ComponentProps<typeof Button>>(Button)
      .at(0);

    await (updateBtn.invoke("onPress") as () => Promise<void>)();
    await act(async (): Promise<void> => { await wait(1); wrapper.update(); });
    const { openURL } = Linking;
    expect(openURL)
      .toHaveBeenCalled();
  });

  it("should report up to date", async (): Promise<void> => {
    mockedFetch.mock("https://play.google.com/store/apps/details?id=com.fluidattacks.integrates", {
      body: "<html><body><span>20.06.1337</span></body></html>",
      status: 200,
    });
    const isOutdated: boolean = await originalVersion.checkPlayStoreVersion();

    expect(isOutdated)
      .toBe(false);
  });

  it("should report outdated", async (): Promise<void> => {
    mockedFetch.mock("https://play.google.com/store/apps/details?id=com.fluidattacks.integrates", {
      body: "<html><body><span>20.07.1337</span></body></html>",
      status: 200,
    });
    const isOutdated: boolean = await originalVersion.checkPlayStoreVersion();

    expect(isOutdated)
      .toBe(true);
  });

  it("should gracefully fallback when it fails to retrieve version", async (): Promise<void> => {
    mockedFetch.mock("https://play.google.com/store/apps/details?id=com.fluidattacks.integrates", {
      body: "<html><body><span>thereisanerror</span></body></html>",
      status: 200,
    });
    const isOutdated: boolean = await originalVersion.checkPlayStoreVersion();

    expect(isOutdated)
      .toBe(false);
  });
});
