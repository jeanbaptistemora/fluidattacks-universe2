import { mount, ReactWrapper } from "enzyme";
import * as Google from "expo-google-app-auth";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { I18nextProvider } from "react-i18next";
import { Alert, Platform } from "react-native";
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

jest.mock("react-native", (): Dictionary => {
  const mockedRN: Dictionary = jest.requireActual("react-native");
  Object.assign(mockedRN.Alert, { alert: jest.fn() });

  return mockedRN;
});

const mockHistoryReplace: jest.Mock = jest.fn();

jest.mock("react-router-native", (): Dictionary => {
  const mockedRouter: Dictionary<() => Dictionary> = jest.requireActual("react-router-native");

  return {
    ...mockedRouter,
    useHistory: (): Dictionary => ({
      ...mockedRouter.useHistory(),
      replace: mockHistoryReplace,
    }),
  };
});

jest.mock("../../utils/version", (): Dictionary => {
  const mockedVersion: Dictionary = jest.requireActual("../../utils/version");
  mockedVersion.checkVersion = jest.fn();

  return mockedVersion;
});

describe("LoginView", (): void => {
  afterEach((): void => {
    jest.clearAllMocks();
  });

  it("should return a function", (): void => {
    expect(typeof (LoginView))
      .toEqual("function");
  });

  it("should render", (): void => {

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
    expect(wrapper.find("logo")
      .length)
      .toBeGreaterThan(0);
    expect(wrapper.find("googleButton"))
      .toHaveLength(1);
  });

  it("should auth with google", async (): Promise<void> => {
    (checkVersion as jest.Mock).mockImplementation((): Promise<boolean> => Promise.resolve(false));
    (Google.logInAsync as jest.Mock).mockImplementation((): Promise<Google.LogInResult> => Promise.resolve({
      accessToken: "abc123",
      idToken: "abc123",
      refreshToken: "abc123",
      type: "success",
      user: {
        email: "test@fluidattacks.com",
        familyName: "Doe",
        givenName: "John",
        name: "JOHN DOE",
      },
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
    expect(mockHistoryReplace)
      .toHaveBeenCalledWith("/Welcome", {
        authProvider: "GOOGLE",
        authToken: "abc123",
        type: "success",
        user: {
          email: "test@fluidattacks.com",
          firstName: "John",
          fullName: "John Doe",
          lastName: "Doe",
        },
      });
  });

  it("should handle auth cancel", async (): Promise<void> => {
    (checkVersion as jest.Mock).mockImplementation((): Promise<boolean> => Promise.resolve(false));
    (Google.logInAsync as jest.Mock).mockImplementation((): Promise<Google.LogInResult> => Promise.reject({
      code: Platform.select({ android: 2, ios: -3 }),
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

    (Google.logInAsync as jest.Mock).mockImplementation((): Promise<Google.LogInResult> => Promise.resolve({
      type: "cancel",
    }));
    await act(async (): Promise<void> => {
      await (googleBtn.invoke("onPress") as () => Promise<void>)();
      wrapper.update();
    });

    expect(wrapper
      .find("preloader")
      .prop("visible"))
      .toEqual(false);
  });

  it("should handle errors", async (): Promise<void> => {
    (checkVersion as jest.Mock).mockImplementation((): Promise<boolean> => Promise.reject("Oops :("));
    (Google.logInAsync as jest.Mock).mockImplementation((): Promise<Google.LogInResult> => Promise.reject("Oops :("));

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
    expect(Alert.alert)
      .toHaveBeenCalled();
  });
});
