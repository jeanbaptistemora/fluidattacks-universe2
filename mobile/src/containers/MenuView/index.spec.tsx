// tslint:disable-next-line: no-submodule-imports
import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { mount, ReactWrapper } from "enzyme";
import { GraphQLError } from "graphql";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { I18nextProvider } from "react-i18next";
import { Alert } from "react-native";
import { Appbar, Provider as PaperProvider } from "react-native-paper";
import { NativeRouter } from "react-router-native";
import wait from "waait";

import { i18next } from "../../utils/translations/translate";

import { MenuView } from "./index";
import { PROJECTS_QUERY } from "./queries";

jest.mock("react-native", (): Dictionary => {
  const mockedRN: Dictionary = jest.requireActual("react-native");
  Object.assign(mockedRN.Alert, { alert: jest.fn() });

  return mockedRN;
});

describe("MenuView", (): void => {
  it("should return a function", (): void => {
    expect(typeof (MenuView))
      .toEqual("function");
  });

  it("should render", async (): Promise<void> => {

    const projectMock: Readonly<MockedResponse> = {
      request: {
        query: PROJECTS_QUERY,
      },
      result: {
        data: {
          me: {
            projects: [
              { name: "unittesting", description: "Integrates unit test project" },
            ],
          },
        },
      },
    };

    const wrapper: ReactWrapper = mount(
      <PaperProvider>
        <I18nextProvider i18n={i18next}>
          <NativeRouter initialEntries={["/Menu"]}>
            <MockedProvider mocks={[projectMock]} addTypename={false}>
              <MenuView />
            </MockedProvider>
          </NativeRouter>
        </I18nextProvider>
      </PaperProvider>,
    );
    await act(async (): Promise<void> => { await wait(0); wrapper.update(); });

    expect(wrapper)
      .toHaveLength(1);
  });

  it("should handle errors", async (): Promise<void> => {

    const errorMock: Readonly<MockedResponse> = {
      request: {
        query: PROJECTS_QUERY,
      },
      result: {
        errors: [
          new GraphQLError("Unexpected error"),
        ],
      },
    };

    const wrapper: ReactWrapper = mount(
      <PaperProvider>
        <I18nextProvider i18n={i18next}>
          <NativeRouter initialEntries={["/Menu"]}>
            <MockedProvider mocks={[errorMock]} addTypename={false}>
              <MenuView />
            </MockedProvider>
          </NativeRouter>
        </I18nextProvider>
      </PaperProvider>,
    );
    await act(async (): Promise<void> => { await wait(0); wrapper.update(); });

    expect(wrapper)
      .toHaveLength(1);
    expect(Alert.alert)
      .toHaveBeenCalled();
  });

  it("should render drawer menu", async (): Promise<void> => {
    const wrapper: ReactWrapper = mount(
      <PaperProvider>
        <I18nextProvider i18n={i18next}>
          <NativeRouter initialEntries={["/Menu"]}>
            <MockedProvider>
              <MenuView />
            </MockedProvider>
          </NativeRouter>
        </I18nextProvider>
      </PaperProvider>,
    );
    await act(async (): Promise<void> => { await wait(0); wrapper.update(); });

    expect(wrapper)
      .toHaveLength(1);

    const menuBtn: ReactWrapper<React.ComponentProps<typeof Appbar.Action>> = wrapper
      .find({ icon: "menu" })
      .at(0);
    expect(menuBtn)
      .toHaveLength(1);

    const drawer: ReactWrapper<{}, { drawerTranslation: { _value: number } }> = wrapper.find("DrawerLayout");
    expect(drawer.state().drawerTranslation._value)
      .toEqual(0);

    (menuBtn.invoke("onPress") as () => void)();
    await act(async (): Promise<void> => { await wait(1); wrapper.update(); });
    expect(drawer.state().drawerTranslation._value)
      .toBeGreaterThan(0);
  });
});
