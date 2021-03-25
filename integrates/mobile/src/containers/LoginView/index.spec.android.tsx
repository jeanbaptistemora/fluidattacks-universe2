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
import { getOutdatedStatus } from "./version";

jest.mock("expo-constants", (): Record<string, unknown> => ({
  ...jest.requireActual("expo-constants"),
  manifest: {
    ...jest.requireActual<Record<string, Record<string, unknown>>>(
      "expo-constants",
    ).manifest,
    android: {
      package: "com.fluidattacks.integrates",
    },
  },
  nativeAppVersion: "21.02.01912",
}));

const mockedFetch: FetchMockStatic = fetch as typeof fetch & FetchMockStatic;

const mockVersion: (options: {
  httpStatus: number;
  version: string;
}) => void = ({
  version,
  httpStatus,
}: {
  httpStatus: number;
  version: string;
}): void => {
  mockedFetch.reset();
  mockedFetch.mock(
    "https://play.google.com/store/apps/details?id=com.fluidattacks.integrates",
    {
      body: [
        '<div class="hAyfc">',
        '<div class="BgcNfc">Current Version</div>',
        '<span class="htlgb">',
        '<div class="IQ1z0d">',
        `<span class="htlgb">${version}</span>`,
        "</div>",
        "</span>",
        "</div>",
      ].join(""),
      status: httpStatus,
    },
  );
};

describe("LoginView", (): void => {
  afterEach((): void => {
    jest.clearAllMocks();
    mockedFetch.reset();
  });

  it("should not display update dialog", async (): Promise<void> => {
    mockVersion({ version: "21.02.01912", httpStatus: 200 });
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
      .find("GoogleButton")
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
    mockVersion({ version: "21.01.00000", httpStatus: 200 });
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

    const dialog: ReactWrapper = wrapper
      .find("Dialog");
    expect(dialog
      .prop("visible"))
      .toEqual(true);

    const updateBtn: ReactWrapper<React.ComponentProps<typeof Button>> = dialog
      .find<React.ComponentProps<typeof Button>>(Button)
      .at(0);

    await (updateBtn.invoke("onPress") as () => Promise<void>)();
    await act(async (): Promise<void> => { await wait(1); wrapper.update(); });
    const { openURL } = Linking;
    expect(openURL)
      .toHaveBeenCalled();
  });

  it("should report up to date", async (): Promise<void> => {
    mockVersion({ version: "21.02.01912", httpStatus: 200 });
    const isOutdated: boolean = await getOutdatedStatus();

    expect(isOutdated)
      .toBe(false);
  });

  it("should report outdated", async (): Promise<void> => {
    mockVersion({ version: "21.01.00000", httpStatus: 200 });
    const isOutdated: boolean = await getOutdatedStatus();

    expect(isOutdated)
      .toBe(true);
  });

  it("should gracefully fallback when it fails to retrieve version", async (): Promise<void> => {
    mockVersion({ version: "", httpStatus: 400 });
    const isOutdated: boolean = await getOutdatedStatus();

    expect(isOutdated)
      .toBe(false);
  });
});
