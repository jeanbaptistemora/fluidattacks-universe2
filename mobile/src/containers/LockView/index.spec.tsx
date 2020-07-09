import { wait } from "@apollo/react-testing";
import { mount, ReactWrapper } from "enzyme";
import * as LocalAuthentication from "expo-local-authentication";
import * as SecureStore from "expo-secure-store";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { I18nextProvider } from "react-i18next";
import { Button, Provider as PaperProvider } from "react-native-paper";
import { NativeRouter } from "react-router-native";

import { i18next } from "../../utils/translations/translate";

import { LockView } from "./index";

const mockHistoryReplace: jest.Mock = jest.fn();

jest.mock("react-router-native", (): Dictionary => {
  const mockedRouter: Dictionary<() => Dictionary> =
    jest.requireActual("react-router-native");

  return {
    ...mockedRouter,
    useHistory: (): Dictionary => ({
      ...mockedRouter.useHistory(),
      replace: mockHistoryReplace,
    }),
  };
});

jest.mock("expo-secure-store");
jest.mock("expo-local-authentication");

describe("LockView", (): void => {
  afterEach((): void => {
    jest.clearAllMocks();
  });

  it("should return a function", (): void => {
    expect(typeof (LockView))
      .toEqual("function");
  });

  it("should render", (): void => {

    const wrapper: ReactWrapper = mount(
      <PaperProvider>
        <I18nextProvider i18n={i18next}>
          <NativeRouter initialEntries={["/"]}>
            <LockView />
          </NativeRouter>
        </I18nextProvider>
      </PaperProvider>,
    );

    expect(wrapper)
      .toHaveLength(1);
    expect(wrapper.text())
      .toContain("Unlock to continue");
  });

  it("should prompt for biometric unlock", async (): Promise<void> => {
    (SecureStore.getItemAsync as jest.Mock)
      .mockResolvedValueOnce(JSON.stringify({}));
    (LocalAuthentication.authenticateAsync as jest.Mock).mockResolvedValue({
      success: true,
    });

    const wrapper: ReactWrapper = mount(
      <PaperProvider>
        <I18nextProvider i18n={i18next}>
          <NativeRouter initialEntries={["/"]}>
            <LockView />
          </NativeRouter>
        </I18nextProvider>
      </PaperProvider>,
    );

    await act(async (): Promise<void> => { await wait(0); wrapper.update(); });

    expect(wrapper)
      .toHaveLength(1);

    expect(LocalAuthentication.authenticateAsync)
      .toHaveBeenCalled();
    expect(mockHistoryReplace)
      .toHaveBeenCalledWith("/Dashboard", {});
  });

  it("should handle unsuccessful biometric unlock", async (): Promise<void> => {
    (SecureStore.getItemAsync as jest.Mock)
      .mockResolvedValueOnce("some.session.token")
      .mockResolvedValueOnce(JSON.stringify({}));
    (LocalAuthentication.authenticateAsync as jest.Mock).mockResolvedValue({
      success: false,
    });

    const wrapper: ReactWrapper = mount(
      <PaperProvider>
        <I18nextProvider i18n={i18next}>
          <NativeRouter initialEntries={["/"]}>
            <LockView />
          </NativeRouter>
        </I18nextProvider>
      </PaperProvider>,
    );

    await act(async (): Promise<void> => { await wait(0); wrapper.update(); });

    expect(wrapper)
      .toHaveLength(1);
    expect(mockHistoryReplace)
      .not
      .toHaveBeenCalled();
    expect(wrapper.find(Button))
      .toHaveLength(1);
    expect(wrapper.text())
      .toContain("Authenticate");
  });
});
