// tslint:disable-next-line: no-submodule-imports
import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { mount, ReactWrapper } from "enzyme";
import { GraphQLError } from "graphql";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { I18nextProvider } from "react-i18next";
import { Alert } from "react-native";
import { Provider as PaperProvider, Text } from "react-native-paper";
import { MemoryRouter } from "react-router-native";
import wait from "waait";

import { i18next } from "../../utils/translations/translate";

import { MenuView } from "./index";
import { PROJECTS_QUERY } from "./queries";

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
              { openVulnerabilities: 0, closedVulnerabilities: 0 },
            ],
          },
        },
      },
    };

    const wrapper: ReactWrapper = mount(
      <PaperProvider>
        <I18nextProvider i18n={i18next}>
          <MemoryRouter initialEntries={[{ pathname: "/Menu", state: { userInfo: {} } }]}>
            <MockedProvider mocks={[projectMock]} addTypename={false}>
              <MenuView />
            </MockedProvider>
          </MemoryRouter>
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
          <MemoryRouter initialEntries={[{ pathname: "/Menu", state: { userInfo: {} } }]}>
            <MockedProvider mocks={[errorMock]} addTypename={false}>
              <MenuView />
            </MockedProvider>
          </MemoryRouter>
        </I18nextProvider>
      </PaperProvider>,
    );
    await act(async (): Promise<void> => { await wait(0); wrapper.update(); });

    expect(wrapper)
      .toHaveLength(1);
    expect(Alert.alert)
      .toHaveBeenCalled();
  });

  it("should perform logout", async (): Promise<void> => {
    const wrapper: ReactWrapper = mount(
      <PaperProvider>
        <I18nextProvider i18n={i18next}>
          <MemoryRouter initialEntries={[{ pathname: "/Menu", state: { userInfo: {} } }]}>
            <MockedProvider>
              <MenuView />
            </MockedProvider>
          </MemoryRouter>
        </I18nextProvider>
      </PaperProvider>,
    );
    await act(async (): Promise<void> => { await wait(0); wrapper.update(); });

    expect(wrapper)
      .toHaveLength(1);

    const logoutBtn: ReactWrapper<React.ComponentProps<typeof Text>> = wrapper
      .find({ children: "Logout" })
      .at(0);

    expect(logoutBtn)
      .toHaveLength(1);

    await (logoutBtn.invoke("onPress") as () => Promise<void>)();
    expect(mockHistoryReplace)
      .toHaveBeenCalled();
  });
});
