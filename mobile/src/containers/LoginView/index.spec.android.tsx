import { mount, ReactWrapper } from "enzyme";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { I18nextProvider } from "react-i18next";
import { Linking } from "react-native";
import { Button, Provider as PaperProvider } from "react-native-paper";
import { NativeRouter } from "react-router-native";
import wait from "waait";

import { i18next } from "../../utils/translations/translate";
import { checkVersion } from "../../utils/version";

import { LoginView } from "./index";

jest.mock("../../utils/version", (): Dictionary => {
  const mockedVersion: Dictionary = jest.requireActual("../../utils/version");
  mockedVersion.checkVersion = jest.fn();

  return mockedVersion;
});

jest.mock("expo-constants", (): Dictionary => ({
  ...jest.requireActual("expo-constants"),
  manifest: {
    ...jest.requireActual<Dictionary>("expo-constants").manifest,
    android: {
      package: "com.fluidattacks.integrates",
    },
  },
}));

describe("LoginView", (): void => {
  it("should display update dialog", async (): Promise<void> => {
    (checkVersion as jest.Mock).mockImplementation((): Promise<boolean> => Promise.resolve(true));

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
      .find("Button")
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
    (checkVersion as jest.Mock).mockImplementation((): Promise<boolean> => Promise.resolve(false));

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
      .find("Button")
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
    (checkVersion as jest.Mock).mockImplementation((): Promise<boolean> => Promise.resolve(true));
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
});
