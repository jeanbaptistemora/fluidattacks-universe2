import { mount } from "enzyme";
import type { ReactWrapper } from "enzyme";
import {
  SecurityLevel,
  authenticateAsync,
  getEnrolledLevelAsync,
} from "expo-local-authentication";
import { getItemAsync } from "expo-secure-store";
import React from "react";
import { act } from "react-dom/test-utils";
import { I18nextProvider } from "react-i18next";
import { Button, Provider as PaperProvider } from "react-native-paper";
import { NativeRouter } from "react-router-native";
import wait from "waait";

import { LockView } from ".";
import { i18next } from "../../utils/translations/translate";

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

jest.mock("expo-secure-store");
jest.mock("expo-local-authentication");

describe("LockView", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof LockView).toStrictEqual("function");

    jest.clearAllMocks();
  });

  it("should render", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <PaperProvider>
        <I18nextProvider i18n={i18next}>
          <NativeRouter initialEntries={["/"]}>
            <LockView />
          </NativeRouter>
        </I18nextProvider>
      </PaperProvider>
    );

    expect(wrapper).toHaveLength(1);
    expect(wrapper.text()).toContain("Unlock to continue");

    jest.clearAllMocks();
  });

  it("should prompt for biometric unlock", async (): Promise<void> => {
    expect.hasAssertions();

    (getItemAsync as jest.Mock).mockResolvedValueOnce(JSON.stringify({}));
    (authenticateAsync as jest.Mock).mockResolvedValue({
      success: true,
    });
    (getEnrolledLevelAsync as jest.Mock).mockResolvedValue(
      SecurityLevel.BIOMETRIC
    );

    const wrapper: ReactWrapper = mount(
      <PaperProvider>
        <I18nextProvider i18n={i18next}>
          <NativeRouter initialEntries={["/"]}>
            <LockView />
          </NativeRouter>
        </I18nextProvider>
      </PaperProvider>
    );

    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    expect(wrapper).toHaveLength(1);
    // ESLint suggested the change from toBeCalled to the current method
    expect(authenticateAsync).toHaveBeenCalledWith();
    expect(mockHistoryReplace).toHaveBeenCalledWith("/Dashboard", {});

    jest.clearAllMocks();
  });

  it("should not prompt for biometric unlock", async (): Promise<void> => {
    expect.hasAssertions();

    (getItemAsync as jest.Mock).mockResolvedValueOnce(JSON.stringify({}));
    (authenticateAsync as jest.Mock).mockResolvedValue({
      success: true,
    });
    (getEnrolledLevelAsync as jest.Mock).mockResolvedValue(SecurityLevel.NONE);

    const wrapper: ReactWrapper = mount(
      <PaperProvider>
        <I18nextProvider i18n={i18next}>
          <NativeRouter initialEntries={["/"]}>
            <LockView />
          </NativeRouter>
        </I18nextProvider>
      </PaperProvider>
    );

    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    expect(wrapper).toHaveLength(1);
    expect(authenticateAsync).not.toHaveBeenCalled();
    expect(mockHistoryReplace).toHaveBeenCalledWith("/Login");

    jest.clearAllMocks();
  });

  it("should handle unsuccessful biometric unlock", async (): Promise<void> => {
    expect.hasAssertions();

    (getItemAsync as jest.Mock)
      .mockResolvedValueOnce("some.session.token")
      .mockResolvedValueOnce(JSON.stringify({}));
    (authenticateAsync as jest.Mock).mockResolvedValue({
      success: false,
    });

    const wrapper: ReactWrapper = mount(
      <PaperProvider>
        <I18nextProvider i18n={i18next}>
          <NativeRouter initialEntries={["/"]}>
            <LockView />
          </NativeRouter>
        </I18nextProvider>
      </PaperProvider>
    );

    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    expect(wrapper).toHaveLength(1);
    expect(mockHistoryReplace).not.toHaveBeenCalled();
    expect(wrapper.find(Button)).toHaveLength(1);
    expect(wrapper.text()).toContain("Authenticate");

    jest.clearAllMocks();
  });
});
