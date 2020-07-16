import { MockedProvider, MockedResponse, wait } from "@apollo/react-testing";
import { mount, ReactWrapper } from "enzyme";
import { GraphQLError } from "graphql";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { I18nextProvider } from "react-i18next";
import { Alert, AppState, AppStateEvent, AppStateStatus } from "react-native";
import { Provider as PaperProvider, Text } from "react-native-paper";
import { MemoryRouter } from "react-router-native";

import { i18next } from "../../utils/translations/translate";

import { DashboardView } from "./index";
import { ORGS_QUERY } from "./queries";

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

jest.mock("../../utils/socialAuth");

describe("DashboardView", (): void => {
  afterEach((): void => {
    jest.clearAllMocks();
  });

  it("should return a function", (): void => {
    expect(typeof (DashboardView))
      .toEqual("function");
  });

  it("should render", async (): Promise<void> => {

    const projectMock: Readonly<MockedResponse> = {
      request: {
        query: ORGS_QUERY,
      },
      result: {
        data: {
          me: {
            organizations: [
              {
                analytics: {
                  current: {
                    closed: 7,
                    open: 5,
                  },
                },
                totalGroups: 1,
              },
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
        query: ORGS_QUERY,
      },
      result: {
        data: {
          me: {
            organizations: [],
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
    jest.mock("react-native/Libraries/Alert/Alert");

    const errorMock: Readonly<MockedResponse> = {
      request: {
        query: ORGS_QUERY,
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

  it("should exclude orgs without analytics", async (): Promise<void> => {
    jest.mock("react-native/Libraries/Alert/Alert");

    const errorMock: Readonly<MockedResponse> = {
      request: {
        query: ORGS_QUERY,
      },
      result: {
        data: {
          me: {
            organizations: [
              {
                analytics: {
                  current: {
                    closed: 7,
                    open: 5,
                  },
                },
                totalGroups: 1,
              },
              {
                // tslint:disable-next-line: no-null-keyword
                analytics: null,
                totalGroups: 1,
              },
            ],
          },
        },
        errors: [
          new GraphQLError("Exception - Document not found"),
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
    expect(wrapper.text())
      .toContain("58.3%");
    expect(wrapper.text())
      .toContain("of 12 found in 1 system");
    expect(Alert.alert)
      .not
      .toHaveBeenCalled();
  });

  it("should refresh on resume", async (): Promise<void> => {
    let stateListener: (state: AppStateStatus) => Promise<void> =
      async (): Promise<void> => undefined;

    jest.mock(
      "react-native",
      (): Record<string, {}> => {
        const mockedRN: Dictionary<() => Dictionary> =
          jest.requireActual("react-native");

        return {
          ...mockedRN,
          AppState: { addEventListener: jest.fn() },
        };
      },
    );

    (AppState.addEventListener as jest.Mock).mockImplementation((
      _: AppStateEvent,
      listener: (state: AppStateStatus) => Promise<void>,
    ): void => {
      stateListener = listener;
    });

    const projectMock: Readonly<MockedResponse> = {
      request: {
        query: ORGS_QUERY,
      },
      result: {
        data: {
          me: {
            organizations: [
              {
                analytics: {
                  current: {
                    closed: 7,
                    open: 5,
                  },
                },
                totalGroups: 1,
              },
            ],
          },
        },
      },
    };

    const newProjectMock: Readonly<MockedResponse> = {
      request: {
        query: ORGS_QUERY,
      },
      result: {
        data: {
          me: {
            organizations: [
              {
                analytics: {
                  current: {
                    closed: 12,
                    open: 0,
                  },
                },
                totalGroups: 1,
              },
              {
                analytics: {
                  current: {
                    closed: 8,
                    open: 0,
                  },
                },
                totalGroups: 1,
              },
            ],
          },
        },
      },
    };

    const wrapper: ReactWrapper = mount(
      <PaperProvider>
        <I18nextProvider i18n={i18next}>
          <MemoryRouter
            initialEntries={[
              {
                pathname: "/Dashboard",
                state: { user: { fullName: "Test" } },
              },
            ]}
          >
            <MockedProvider
              mocks={[projectMock, newProjectMock]}
              addTypename={false}
            >
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

    await stateListener("background");
    await stateListener("active");
    await act(async (): Promise<void> => { await wait(0); wrapper.update(); });

    expect(wrapper.text())
      .toContain("100%");
    expect(wrapper.text())
      .toContain("of 20 found in 2 systems");

    wrapper.unmount();
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
