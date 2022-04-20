import { mount } from "enzyme";
import type { ReactWrapper } from "enzyme";
import React from "react";
import { act } from "react-dom/test-utils";
import { I18nextProvider } from "react-i18next";
import { Provider as PaperProvider } from "react-native-paper";
import { NativeRouter } from "react-router-native";

import { BitbucketButton } from "./BitbucketButton";
import type { IBitbucketButtonProps } from "./BitbucketButton";
import { GoogleButton } from "./GoogleButton";
import type { IGoogleButtonProps } from "./GoogleButton";
import { MicrosoftButton } from "./MicrosoftButton";
import type { IMicrosoftButtonProps } from "./MicrosoftButton";
import { getOutdatedStatus } from "./version";

import { LoginView } from ".";
import type { IAuthResult } from "../../utils/socialAuth";
import {
  authWithBitbucket,
  authWithGoogle,
  authWithMicrosoft,
} from "../../utils/socialAuth";
import { i18next } from "../../utils/translations/translate";

jest.mock(
  "../../utils/socialAuth",
  (): Record<string, jest.Mock> => ({
    authWithBitbucket: jest.fn(),
    authWithGoogle: jest.fn(),
    authWithMicrosoft: jest.fn(),
  })
);

jest.mock("react-native", (): Record<string, unknown> => {
  const mockedRN: Record<string, unknown> = jest.requireActual("react-native");
  // Needed for the mocks
  // eslint-disable-next-line fp/no-mutating-assign
  Object.assign(mockedRN.Alert, { alert: jest.fn() });

  return mockedRN;
});

const mockHistoryReplace: jest.Mock = jest.fn();

jest.mock("react-router-native", (): Record<string, unknown> => {
  const mockedRouter: Record<string, () => Record<string, unknown>> =
    jest.requireActual("react-router-native");

  return {
    ...mockedRouter,
    useHistory: (): Record<string, unknown> => ({
      ...mockedRouter.useHistory(),
      replace: mockHistoryReplace,
    }),
  };
});

jest.mock("./version", (): Record<string, unknown> => {
  const mockedVersion: Record<string, unknown> =
    jest.requireActual("./version");
  // Must use mutations for the mocks, spy-on autofix breaks some mocks
  // eslint-disable-next-line jest/prefer-spy-on, fp/no-mutation
  mockedVersion.getOutdatedStatus = jest.fn();

  return mockedVersion;
});

jest.mock("expo-secure-store");
jest.mock("expo-local-authentication");

describe("LoginView", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof LoginView).toBe("function");

    jest.clearAllMocks();
  });

  it("should render", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <PaperProvider>
        <I18nextProvider i18n={i18next}>
          <NativeRouter initialEntries={["/"]}>
            <LoginView />
          </NativeRouter>
        </I18nextProvider>
      </PaperProvider>
    );

    expect(wrapper).toHaveLength(1);
    expect(wrapper.find("Logo").length).toBeGreaterThan(0);
    expect(wrapper.find("GoogleButton")).toHaveLength(1);

    jest.clearAllMocks();
  });

  it("should auth with bitbucket", async (): Promise<void> => {
    expect.hasAssertions();

    (getOutdatedStatus as jest.Mock).mockImplementation(
      async (): Promise<boolean> => Promise.resolve(false)
    );
    (authWithBitbucket as jest.Mock).mockImplementation(
      async (): Promise<IAuthResult> =>
        Promise.resolve({
          authProvider: "BITBUCKET",
          authToken: "abc123",
          type: "success",
          user: {
            email: "test@fluidattacks.com",
            firstName: "Jdoe",
            fullName: "John Doe",
            photoUrl: "https://bitbucket.org/some/picture.png",
          },
        })
    );

    const wrapper: ReactWrapper = mount(
      <PaperProvider>
        <I18nextProvider i18n={i18next}>
          <NativeRouter initialEntries={["/"]}>
            <LoginView />
          </NativeRouter>
        </I18nextProvider>
      </PaperProvider>
    );

    expect(wrapper).toHaveLength(1);

    const bitbucketBtn: ReactWrapper<IBitbucketButtonProps> =
      wrapper.find<IBitbucketButtonProps>(BitbucketButton);

    expect(bitbucketBtn).toHaveLength(1);

    await act(async (): Promise<void> => {
      await (bitbucketBtn.invoke("onPress") as () => Promise<void>)();
      wrapper.update();
    });

    expect(mockHistoryReplace).toHaveBeenCalledWith("/Welcome", {
      authProvider: "BITBUCKET",
      authToken: "abc123",
      type: "success",
      user: {
        email: "test@fluidattacks.com",
        firstName: "Jdoe",
        fullName: "John Doe",
        photoUrl: "https://bitbucket.org/some/picture.png",
      },
    });

    jest.clearAllMocks();
  });

  it("should auth with google", async (): Promise<void> => {
    expect.hasAssertions();

    (getOutdatedStatus as jest.Mock).mockImplementation(
      async (): Promise<boolean> => Promise.resolve(false)
    );
    (authWithGoogle as jest.Mock).mockImplementation(
      async (): Promise<IAuthResult> =>
        Promise.resolve({
          authProvider: "GOOGLE",
          authToken: "abc123",
          type: "success",
          user: {
            email: "test@fluidattacks.com",
            firstName: "John",
            fullName: "John Doe",
            lastName: "Doe",
          },
        })
    );

    const wrapper: ReactWrapper = mount(
      <PaperProvider>
        <I18nextProvider i18n={i18next}>
          <NativeRouter initialEntries={["/"]}>
            <LoginView />
          </NativeRouter>
        </I18nextProvider>
      </PaperProvider>
    );

    expect(wrapper).toHaveLength(1);

    const googleBtn: ReactWrapper<IGoogleButtonProps> =
      wrapper.find<IGoogleButtonProps>(GoogleButton);

    expect(googleBtn).toHaveLength(1);

    await act(async (): Promise<void> => {
      await (googleBtn.invoke("onPress") as () => Promise<void>)();
      wrapper.update();
    });

    expect(mockHistoryReplace).toHaveBeenCalledWith("/Welcome", {
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

    jest.clearAllMocks();
  });

  it("should auth with microsoft", async (): Promise<void> => {
    expect.hasAssertions();

    (getOutdatedStatus as jest.Mock).mockImplementation(
      async (): Promise<boolean> => Promise.resolve(false)
    );
    (authWithMicrosoft as jest.Mock).mockImplementation(
      async (): Promise<IAuthResult> =>
        Promise.resolve({
          authProvider: "MICROSOFT",
          authToken: "def456",
          type: "success",
          user: {
            email: "test@fluidattacks.com",
            firstName: "John",
            fullName: "John Doe",
            lastName: "DOE",
          },
        })
    );

    const wrapper: ReactWrapper = mount(
      <PaperProvider>
        <I18nextProvider i18n={i18next}>
          <NativeRouter initialEntries={["/"]}>
            <LoginView />
          </NativeRouter>
        </I18nextProvider>
      </PaperProvider>
    );

    expect(wrapper).toHaveLength(1);

    const microsoftBtn: ReactWrapper<IMicrosoftButtonProps> =
      wrapper.find<IMicrosoftButtonProps>(MicrosoftButton);

    expect(microsoftBtn).toHaveLength(1);

    await act(async (): Promise<void> => {
      await (microsoftBtn.invoke("onPress") as () => Promise<void>)();
      wrapper.update();
    });

    expect(mockHistoryReplace).toHaveBeenCalledWith("/Welcome", {
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

    jest.clearAllMocks();
  });

  it("should handle auth cancel", async (): Promise<void> => {
    expect.hasAssertions();

    (getOutdatedStatus as jest.Mock).mockImplementation(
      async (): Promise<boolean> => Promise.resolve(false)
    );
    (authWithGoogle as jest.Mock).mockImplementation(
      async (): Promise<IAuthResult> =>
        Promise.resolve({
          type: "cancel",
        })
    );
    (authWithMicrosoft as jest.Mock).mockImplementation(
      // Exception: WF(Function implementation must be here)
      // eslint-disable-next-line
      async (): Promise<IAuthResult> => // NOSONAR
        Promise.resolve({
          type: "cancel",
        })
    );
    (authWithBitbucket as jest.Mock).mockImplementation(
      // Exception: WF(Function implementation must be here)
      // eslint-disable-next-line
      async (): Promise<IAuthResult> => // NOSONAR
        Promise.resolve({
          type: "cancel",
        })
    );

    const wrapper: ReactWrapper = mount(
      <PaperProvider>
        <I18nextProvider i18n={i18next}>
          <NativeRouter initialEntries={["/"]}>
            <LoginView />
          </NativeRouter>
        </I18nextProvider>
      </PaperProvider>
    );

    expect(wrapper).toHaveLength(1);

    const googleBtn: ReactWrapper<IGoogleButtonProps> =
      wrapper.find<IGoogleButtonProps>(GoogleButton);

    expect(googleBtn).toHaveLength(1);

    await act(async (): Promise<void> => {
      await (googleBtn.invoke("onPress") as () => Promise<void>)();
      wrapper.update();
    });

    const microsoftBtn: ReactWrapper<IMicrosoftButtonProps> =
      wrapper.find<IMicrosoftButtonProps>(MicrosoftButton);

    expect(microsoftBtn).toHaveLength(1);

    await act(async (): Promise<void> => {
      await (microsoftBtn.invoke("onPress") as () => Promise<void>)();
      wrapper.update();
    });

    expect(wrapper.find("Preloader").prop("visible")).toBe(false);

    jest.clearAllMocks();
  });
});
