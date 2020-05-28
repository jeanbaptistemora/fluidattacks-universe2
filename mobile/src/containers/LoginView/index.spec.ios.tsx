import { mount, ReactWrapper } from "enzyme";
import * as Google from "expo-google-app-auth";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { I18nextProvider } from "react-i18next";
import { Provider as PaperProvider } from "react-native-paper";
import { NativeRouter } from "react-router-native";

import { i18next } from "../../utils/translations/translate";
import { checkVersion } from "../../utils/version";

import { GoogleButton, IGoogleButtonProps } from "./GoogleButton";
import { LoginView } from "./index";

jest.mock("expo-google-app-auth", (): Dictionary => {
  const mockedGoogleAuth: Dictionary = jest.requireActual("expo-google-app-auth");
  mockedGoogleAuth.logInAsync = jest.fn();

  return mockedGoogleAuth;
});

jest.mock("../../utils/version", (): Dictionary => {
  const mockedVersion: Dictionary = jest.requireActual("../../utils/version");
  mockedVersion.checkVersion = jest.fn();

  return mockedVersion;
});

describe("LoginView", (): void => {

  it("should handle auth permission deny", async (): Promise<void> => {
    (checkVersion as jest.Mock).mockImplementation((): Promise<boolean> => Promise.resolve(false));
    (Google.logInAsync as jest.Mock).mockImplementation((): Promise<Google.LogInResult> => Promise.reject({
      code: -3,
    }));

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

    const googleBtn: ReactWrapper<IGoogleButtonProps> = wrapper
      .find<IGoogleButtonProps>(GoogleButton);
    expect(googleBtn)
      .toHaveLength(1);

    await act(async (): Promise<void> => {
      await (googleBtn.invoke("onPress") as () => Promise<void>)();
      wrapper.update();
    });
    expect(wrapper
      .find("preloader")
      .prop("visible"))
      .toEqual(false);
  });
});
