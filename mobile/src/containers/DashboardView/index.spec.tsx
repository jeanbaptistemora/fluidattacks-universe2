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

import { DashboardView } from "./index";
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

describe("DashboardView", (): void => {
  it("should return a function", (): void => {
    expect(typeof (DashboardView))
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
              { openVulnerabilities: 5, closedVulnerabilities: 7 },
            ],
          },
        },
      },
    };

    const wrapper: ReactWrapper = mount(
      <PaperProvider>
        <I18nextProvider i18n={i18next}>
          <MemoryRouter initialEntries={[{ pathname: "/Dashboard", state: { user: { fullName: "Test" } } }]}>
            <MockedProvider mocks={[projectMock]} addTypename={false}>
              <DashboardView />
            </MockedProvider>
          </MemoryRouter>
        </I18nextProvider>
      </PaperProvider>,
    );
    await act(async (): Promise<void> => { await wait(0); wrapper.update(); });

    expect(wrapper)
      .toHaveLength(1);
    expect(wrapper.text())
      .toContain("58.3%");
    expect(wrapper.text())
      .toContain("of 12 found in 1 system");
  });

  it("should render empty", async (): Promise<void> => {

    const emptyMock: Readonly<MockedResponse> = {
      request: {
        query: PROJECTS_QUERY,
      },
      result: {
        data: {
          me: {
            projects: [],
          },
        },
      },
    };

    const wrapper: ReactWrapper = mount(
      <PaperProvider>
        <I18nextProvider i18n={i18next}>
          <MemoryRouter initialEntries={[{ pathname: "/Dashboard", state: { user: { fullName: "Test" } } }]}>
            <MockedProvider mocks={[emptyMock]} addTypename={false}>
              <DashboardView />
            </MockedProvider>
          </MemoryRouter>
        </I18nextProvider>
      </PaperProvider>,
    );
    await act(async (): Promise<void> => { await wait(0); wrapper.update(); });

    expect(wrapper)
      .toHaveLength(1);
    expect(wrapper.text())
      .toContain("0%");
    expect(wrapper.text())
      .toContain("of 0 found in 0 systems");
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
          <MemoryRouter initialEntries={[{ pathname: "/Dashboard", state: { user: { fullName: "Test" } } }]}>
            <MockedProvider mocks={[errorMock]} addTypename={false}>
              <DashboardView />
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
          <MemoryRouter initialEntries={[{ pathname: "/Dashboard", state: { user: { fullName: "Test" } } }]}>
            <MockedProvider>
              <DashboardView />
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
