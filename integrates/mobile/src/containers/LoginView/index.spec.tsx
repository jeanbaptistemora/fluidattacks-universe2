import { mount, ReactWrapper } from "enzyme";
import * as AppAuth from "expo-app-auth";
import { FetchMockStatic } from "fetch-mock";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { I18nextProvider } from "react-i18next";
import { Alert, Platform } from "react-native";
import { Provider as PaperProvider } from "react-native-paper";
import { NativeRouter } from "react-router-native";

import { authWithGoogle, IAuthResult } from "../../utils/socialAuth";
import { i18next } from "../../utils/translations/translate";

import { BitbucketButton, IBitbucketButtonProps } from "./BitbucketButton";
import { GoogleButton, IGoogleButtonProps } from "./GoogleButton";
import { LoginView } from "./index";
import { IMicrosoftButtonProps, MicrosoftButton } from "./MicrosoftButton";
import { checkPlayStoreVersion } from "./version";

jest.mock(
  "../../utils/socialAuth/providers/google",
  (): Record<string, jest.Mock> => ({
    authWithGoogle: jest.fn(),
  }),
);

jest.mock("expo-app-auth", (): Dictionary => {
  const mockedMicrosoftAuth: Dictionary = jest.requireActual("expo-app-auth");
  mockedMicrosoftAuth.authAsync = jest.fn();

  return mockedMicrosoftAuth;
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

jest.mock("./version", (): Dictionary => {
  const mockedVersion: Dictionary = jest.requireActual("./version");
  mockedVersion.checkPlayStoreVersion = jest.fn();

  return mockedVersion;
});

jest.mock("expo-secure-store");
jest.mock("expo-local-authentication");

const mockedFetch: FetchMockStatic = fetch as typeof fetch & FetchMockStatic;

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

  it("should auth with bitbucket", async (): Promise<void> => {
    (checkPlayStoreVersion as jest.Mock).mockImplementation((): Promise<boolean> => Promise.resolve(false));
    (AppAuth.authAsync as jest.Mock).mockImplementation((): Promise<AppAuth.TokenResponse> => Promise.resolve({
      accessToken: "abc123",
      accessTokenExpirationDate: "",
      additionalParameters: {},
      idToken: "def456",
      refreshToken: "",
      tokenType: "",
    }));
    mockedFetch.mock("https://api.bitbucket.org/2.0/user", {
      body: {
        account_id: "",
        display_name: "JOHN DOE",
        links: {
          avatar: {
            href: "https://bitbucket.org/some/picture.png",
          },
        },
        username: "jdoe",
      },
      status: 200,
    });
    mockedFetch.mock("https://api.bitbucket.org/2.0/user/emails", {
      body: {
        values: [
          { email: "something@test.com", is_primary: false },
          { email: "test@fluidattacks.com", is_primary: true },
        ],
      },
      status: 200,
    });

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

    const bitbucketBtn: ReactWrapper<IBitbucketButtonProps> = wrapper
      .find<IBitbucketButtonProps>(BitbucketButton);
    expect(bitbucketBtn)
      .toHaveLength(1);

    await act(async (): Promise<void> => {
      await (bitbucketBtn.invoke("onPress") as () => Promise<void>)();
      wrapper.update();
    });
    expect(mockHistoryReplace)
      .toHaveBeenCalledWith("/Welcome", {
        authProvider: "BITBUCKET",
        authToken: "abc123",
        type: "success",
        user: {
          email: "test@fluidattacks.com",
          firstName: "Jdoe",
          fullName: "John Doe",
          id: "",
          photoUrl: "https://bitbucket.org/some/picture.png",
        },
      });
  });

  it("should auth with google", async (): Promise<void> => {
    (checkPlayStoreVersion as jest.Mock).mockImplementation((): Promise<boolean> => Promise.resolve(false));
    (authWithGoogle as jest.Mock).mockImplementation((): Promise<IAuthResult> => Promise.resolve({
      authProvider: "GOOGLE",
      authToken: "abc123",
      type: "success",
      user: {
        email: "test@fluidattacks.com",
        firstName: "John",
        fullName: "John Doe",
        id: "",
        lastName: "Doe",
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
          id: "",
          lastName: "Doe",
        },
      });
  });

  it("should auth with microsoft", async (): Promise<void> => {
    (checkPlayStoreVersion as jest.Mock).mockImplementation((): Promise<boolean> => Promise.resolve(false));
    (AppAuth.authAsync as jest.Mock).mockImplementation((): Promise<AppAuth.TokenResponse> => Promise.resolve({
      accessToken: "abc123",
      accessTokenExpirationDate: "",
      additionalParameters: {},
      idToken: "def456",
      refreshToken: "",
      tokenType: "",
    }));
    mockedFetch.mock("https://login.microsoftonline.com/common/openid/userinfo", {
      body: {
        email: "test@fluidattacks.com",
        family_name: "DOE",
        given_name: "JOHN",
        name: "JOHN DOE",
      },
      status: 200,
    });

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

    const microsoftBtn: ReactWrapper<IMicrosoftButtonProps> = wrapper
      .find<IMicrosoftButtonProps>(MicrosoftButton);
    expect(microsoftBtn)
      .toHaveLength(1);

    await act(async (): Promise<void> => {
      await (microsoftBtn.invoke("onPress") as () => Promise<void>)();
      wrapper.update();
    });
    expect(mockHistoryReplace)
      .toHaveBeenCalledWith("/Welcome", {
        authProvider: "MICROSOFT",
        authToken: "def456",
        type: "success",
        user: {
          email: "test@fluidattacks.com",
          firstName: "John",
          fullName: "John Doe",
          lastName: "DOE",
        },
      });
  });

  it("should handle auth cancel", async (): Promise<void> => {
    (checkPlayStoreVersion as jest.Mock).mockImplementation((): Promise<boolean> => Promise.resolve(false));
    (authWithGoogle as jest.Mock).mockImplementation((): Promise<IAuthResult> => Promise.resolve({
      type: "cancel",
    }));
    (AppAuth.authAsync as jest.Mock).mockImplementation((): Promise<AppAuth.TokenResponse> => Promise.reject({
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

    const microsoftBtn: ReactWrapper<IMicrosoftButtonProps> = wrapper
      .find<IMicrosoftButtonProps>(MicrosoftButton);
    expect(microsoftBtn)
      .toHaveLength(1);

    await act(async (): Promise<void> => {
      await (microsoftBtn.invoke("onPress") as () => Promise<void>)();
      wrapper.update();
    });

    expect(wrapper
      .find("preloader")
      .prop("visible"))
      .toEqual(false);
  });

  it("should handle errors", async (): Promise<void> => {
    (checkPlayStoreVersion as jest.Mock).mockImplementation((): Promise<boolean> => Promise.reject("Oops :("));
    (AppAuth.authAsync as jest.Mock).mockImplementation((): Promise<AppAuth.TokenResponse> =>
      Promise.reject("Oops :("));

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

    const microsoftBtn: ReactWrapper<IMicrosoftButtonProps> = wrapper
      .find<IMicrosoftButtonProps>(MicrosoftButton);
    expect(microsoftBtn)
      .toHaveLength(1);

    await act(async (): Promise<void> => {
      await (microsoftBtn.invoke("onPress") as () => Promise<void>)();
      wrapper.update();
    });

    const bitbucketBtn: ReactWrapper<IBitbucketButtonProps> = wrapper
      .find<IBitbucketButtonProps>(BitbucketButton);
    expect(bitbucketBtn)
      .toHaveLength(1);

    await act(async (): Promise<void> => {
      await (bitbucketBtn.invoke("onPress") as () => Promise<void>)();
      wrapper.update();
    });

    const expectedErrors: number = 2;

    expect(Alert.alert)
      .toHaveBeenCalledTimes(expectedErrors);
  });
});
