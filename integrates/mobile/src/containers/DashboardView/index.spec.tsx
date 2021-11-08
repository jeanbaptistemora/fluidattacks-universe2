import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { mount } from "enzyme";
import type { ReactWrapper } from "enzyme";
import { GraphQLError } from "graphql";
import React from "react";
import type { PropsWithChildren } from "react";
import { act } from "react-dom/test-utils";
import { I18nextProvider } from "react-i18next";
import { Alert, AppState } from "react-native";
import type { AppStateEvent, AppStateStatus } from "react-native";
import { Provider as PaperProvider } from "react-native-paper";
import type { Text } from "react-native-paper";
import { MemoryRouter } from "react-router-native";
import wait from "waait";

import { Indicators } from "./Indicators";
import type { IIndicatorsProps } from "./Indicators";
import { ORGS_QUERY } from "./queries";

import { DashboardView } from ".";
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

jest.mock("../../utils/socialAuth");

describe("DashboardView", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof DashboardView).toStrictEqual("function");

    jest.clearAllMocks();
  });

  it("should render", async (): Promise<void> => {
    expect.hasAssertions();

    const groupMock: Readonly<MockedResponse> = {
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
                  previous: {
                    closed: 7,
                    open: 5,
                  },
                  totalGroups: 1,
                },
                name: "okada",
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
              { pathname: "/Dashboard", state: { user: { fullName: "Test" } } },
            ]}
          >
            <MockedProvider addTypename={false} mocks={[groupMock]}>
              <DashboardView />
            </MockedProvider>
          </MemoryRouter>
        </I18nextProvider>
      </PaperProvider>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    expect(wrapper).toHaveLength(1);
    expect(wrapper.text()).toContain("58.3%");
    expect(wrapper.text()).toContain("0%Compared");
    expect(wrapper.text()).toContain("of 12 CVSSF found in 1 group");

    jest.clearAllMocks();
  });

  it("should render empty", async (): Promise<void> => {
    expect.hasAssertions();

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
          <MemoryRouter
            initialEntries={[
              { pathname: "/Dashboard", state: { user: { fullName: "Test" } } },
            ]}
          >
            <MockedProvider addTypename={false} mocks={[emptyMock]}>
              <DashboardView />
            </MockedProvider>
          </MemoryRouter>
        </I18nextProvider>
      </PaperProvider>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    expect(wrapper).toHaveLength(1);
    expect(wrapper.text()).toContain("0%");
    expect(wrapper.text()).toContain("of 0 CVSSF found in 0 groups");

    jest.clearAllMocks();
  });

  it("should handle errors", async (): Promise<void> => {
    expect.hasAssertions();

    jest.mock("react-native/Libraries/Alert/Alert");

    const errorMock: Readonly<MockedResponse> = {
      request: {
        query: ORGS_QUERY,
      },
      result: {
        errors: [new GraphQLError("Unexpected error")],
      },
    };

    const wrapper: ReactWrapper = mount(
      <PaperProvider>
        <I18nextProvider i18n={i18next}>
          <MemoryRouter
            initialEntries={[
              { pathname: "/Dashboard", state: { user: { fullName: "Test" } } },
            ]}
          >
            <MockedProvider addTypename={false} mocks={[errorMock]}>
              <DashboardView />
            </MockedProvider>
          </MemoryRouter>
        </I18nextProvider>
      </PaperProvider>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    expect(wrapper).toHaveLength(1);
    // eslint-disable-next-line jest/prefer-called-with
    expect(Alert.alert).toHaveBeenCalled();

    jest.clearAllMocks();
  });

  it("should exclude orgs without analytics", async (): Promise<void> => {
    expect.hasAssertions();

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
                  previous: {
                    closed: 0,
                    open: 0,
                  },
                  totalGroups: 1,
                },
                name: "okada",
              },
              {
                analytics: null,
                name: "testorg2",
              },
            ],
          },
        },
        errors: [new GraphQLError("Exception - Document not found")],
      },
    };

    const wrapper: ReactWrapper = mount(
      <PaperProvider>
        <I18nextProvider i18n={i18next}>
          <MemoryRouter
            initialEntries={[
              { pathname: "/Dashboard", state: { user: { fullName: "Test" } } },
            ]}
          >
            <MockedProvider addTypename={false} mocks={[errorMock]}>
              <DashboardView />
            </MockedProvider>
          </MemoryRouter>
        </I18nextProvider>
      </PaperProvider>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    expect(wrapper).toHaveLength(1);
    expect(wrapper.text()).toContain("58.3%");
    expect(wrapper.text()).toContain("of 12 CVSSF found in 1 group");
    expect(Alert.alert).not.toHaveBeenCalled();

    jest.clearAllMocks();
  });

  it("should refresh on resume", async (): Promise<void> => {
    expect.hasAssertions();

    // Needed for the test to succesfully run
    // eslint-disable-next-line fp/no-let
    let stateListener: (state: AppStateStatus) => Promise<void> =
      async (): Promise<void> => wait(0);

    jest.mock("react-native", (): Record<string, unknown> => {
      const mockedRN: Record<string, unknown> =
        jest.requireActual("react-native");

      return {
        ...mockedRN,
        AppState: { addEventListener: jest.fn() },
      };
    });

    (AppState.addEventListener as jest.Mock).mockImplementation(
      (
        _: AppStateEvent,
        listener: (state: AppStateStatus) => Promise<void>
      ): void => {
        // Needed for the test to succesfully run
        // eslint-disable-next-line fp/no-mutation
        stateListener = listener;
      }
    );

    const groupMock: Readonly<MockedResponse> = {
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
                  previous: {
                    closed: 8,
                    open: 4,
                  },
                  totalGroups: 1,
                },
                name: "okada",
              },
            ],
          },
        },
      },
    };

    const newGroupMock: Readonly<MockedResponse> = {
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
                    closed: 11,
                    open: 1,
                  },
                  previous: {
                    closed: 8,
                    open: 4,
                  },
                  totalGroups: 1,
                },
                name: "okada",
              },
              {
                analytics: {
                  current: {
                    closed: 8,
                    open: 0,
                  },
                  previous: {
                    closed: 5,
                    open: 3,
                  },
                  totalGroups: 2,
                },
                name: "testorg2",
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
              addTypename={false}
              mocks={[groupMock, newGroupMock]}
            >
              <DashboardView />
            </MockedProvider>
          </MemoryRouter>
        </I18nextProvider>
      </PaperProvider>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    expect(wrapper).toHaveLength(1);
    expect(wrapper.text()).toContain("58.3%");
    expect(wrapper.text()).toContain("-8.3%Compared");
    expect(wrapper.text()).toContain("of 12 CVSSF found in 1 group");

    await stateListener("background");
    await stateListener("active");
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    expect(wrapper.text()).toContain("91.7%");
    expect(wrapper.text()).toContain("+25%Compared");
    expect(wrapper.text()).toContain("of 12 CVSSF found in 1 group");
    expect(wrapper.text()).toContain("100%");
    expect(wrapper.text()).toContain("+37.5%Compared");
    expect(wrapper.text()).toContain("of 8 CVSSF found in 2 groups");

    wrapper.unmount();
    jest.clearAllMocks();
  });

  it("should scroll", async (): Promise<void> => {
    expect.hasAssertions();

    const groupMock: Readonly<MockedResponse> = {
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
                    closed: 11,
                    open: 1,
                  },
                  previous: {
                    closed: 8,
                    open: 4,
                  },
                  totalGroups: 1,
                },
                name: "okada",
              },
              {
                analytics: {
                  current: {
                    closed: 8,
                    open: 0,
                  },
                  previous: {
                    closed: 5,
                    open: 3,
                  },
                  totalGroups: 2,
                },
                name: "testorg2",
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
            <MockedProvider addTypename={false} mocks={[groupMock]}>
              <DashboardView />
            </MockedProvider>
          </MemoryRouter>
        </I18nextProvider>
      </PaperProvider>
    );

    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    const scrollComponent = wrapper.find(Indicators).at(0);

    expect(
      (): ReactWrapper<PropsWithChildren<IIndicatorsProps>> =>
        scrollComponent.simulate("scroll", {
          deltaX: 1000,
          nativeEvent: { contentOffset: { x: 0 } },
        })
    ).not.toThrow();

    wrapper.unmount();
  });

  it("should perform logout", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <PaperProvider>
        <I18nextProvider i18n={i18next}>
          <MemoryRouter
            initialEntries={[
              { pathname: "/Dashboard", state: { user: { fullName: "Test" } } },
            ]}
          >
            <MockedProvider>
              <DashboardView />
            </MockedProvider>
          </MemoryRouter>
        </I18nextProvider>
      </PaperProvider>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    expect(wrapper).toHaveLength(1);

    const logoutBtn: ReactWrapper<React.ComponentProps<typeof Text>> = wrapper
      .find({ children: "Logout" })
      .at(0);

    expect(logoutBtn).toHaveLength(1);

    await (logoutBtn.invoke("onPress") as () => Promise<void>)();

    // eslint-disable-next-line jest/prefer-called-with
    expect(mockHistoryReplace).toHaveBeenCalled();

    jest.clearAllMocks();
  });
});
