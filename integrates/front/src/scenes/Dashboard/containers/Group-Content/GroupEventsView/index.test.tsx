import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { GraphQLError } from "graphql";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { GET_ROOTS } from "../GroupScopeView/queries";
import { GroupEventsView } from "scenes/Dashboard/containers/Group-Content/GroupEventsView";
import {
  ADD_EVENT_MUTATION,
  GET_EVENTS,
  REQUEST_EVENT_VERIFICATION_MUTATION,
} from "scenes/Dashboard/containers/Group-Content/GroupEventsView/queries";
import { authzPermissionsContext } from "utils/authz/config";
import { msgError, msgSuccess } from "utils/notifications";

const mockHistoryPush: jest.Mock = jest.fn();
jest.mock("react-router", (): Record<string, unknown> => {
  const mockedRouter: Record<string, () => Record<string, unknown>> =
    jest.requireActual("react-router");

  return {
    ...mockedRouter,
    useHistory: (): Record<string, unknown> => ({
      ...mockedRouter.useHistory(),
      push: mockHistoryPush,
    }),
  };
});

jest.mock("../../../../../utils/notifications", (): Record<string, unknown> => {
  const mockedNotifications: Record<string, () => Record<string, unknown>> =
    jest.requireActual("../../../../../utils/notifications");
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

describe("eventsView", (): void => {
  const mockError: readonly MockedResponse[] = [
    {
      request: {
        query: GET_EVENTS,
        variables: {
          groupName: "unittesting",
        },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
    },
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GroupEventsView).toBe("function");
  });

  it("should render an error in component", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/groups/unittesting/events"]}>
        <MockedProvider addTypename={false} mocks={mockError}>
          <Route
            component={GroupEventsView}
            path={"/groups/:groupName/events"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith("groupAlerts.errorTextsad");
    });
    jest.clearAllMocks();
  });

  it("should render events table and go to event", async (): Promise<void> => {
    expect.hasAssertions();

    const mocks: readonly MockedResponse[] = [
      {
        request: {
          query: GET_EVENTS,
          variables: {
            groupName: "unittesting",
          },
        },
        result: {
          data: {
            group: {
              events: [
                {
                  closingDate: "-",
                  detail: "Test description",
                  eventDate: "2018-10-17 00:00:00",
                  eventStatus: "SOLVED",
                  eventType: "AUTHORIZATION_SPECIAL_ATTACK",
                  groupName: "unittesting",
                  id: "463457733",
                },
              ],
              name: "unittesting",
            },
          },
        },
      },
    ];

    render(
      <MemoryRouter initialEntries={["/groups/unittesting/events"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route
            component={GroupEventsView}
            path={"/groups/:groupName/events"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryByRole("table")).toBeInTheDocument();
      expect(
        screen.getByRole("cell", { name: "Authorization for a special attack" })
      ).toBeInTheDocument();
      expect(screen.getByRole("cell", { name: "Solved" })).toBeInTheDocument();
    });

    await userEvent.click(
      screen.getByRole("cell", { name: "Authorization for a special attack" })
    );

    expect(mockHistoryPush).toHaveBeenCalledWith(
      "/groups/unittesting/events/463457733/description"
    );

    jest.clearAllMocks();
  });

  it("should render new event modal", async (): Promise<void> => {
    expect.hasAssertions();

    const mocks: readonly MockedResponse[] = [
      {
        request: {
          query: GET_EVENTS,
          variables: {
            groupName: "unittesting",
          },
        },
        result: {
          data: {
            group: {
              events: [
                {
                  closingDate: "-",
                  detail: "Test description",
                  eventDate: "2018-10-17 00:00:00",
                  eventStatus: "SOLVED",
                  eventType: "AUTHORIZATION_SPECIAL_ATTACK",
                  groupName: "unittesting",
                  id: "463457733",
                },
              ],
              name: "unittesting",
            },
          },
        },
      },
    ];

    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_add_event_mutate" },
    ]);
    render(
      <MemoryRouter initialEntries={["/groups/unittesting/events"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={GroupEventsView}
              path={"/groups/:groupName/events"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryByText("group.events.btn.text")).toBeInTheDocument();
    });
    await userEvent.click(screen.getByText("group.events.btn.text"));
    await waitFor((): void => {
      expect(screen.queryByText("group.events.new")).toBeInTheDocument();
    });

    expect(screen.getAllByText("group.events.form.date")).toHaveLength(1);
    expect(screen.getAllByRole("combobox", { name: "eventType" })).toHaveLength(
      1
    );
    expect(
      screen.getAllByRole("textbox", { name: "rootNickname" })
    ).toHaveLength(1);
    expect(screen.getAllByRole("textbox", { name: "detail" })).toHaveLength(1);
    expect(screen.getAllByTestId("files")).toHaveLength(1);
    expect(screen.getAllByTestId("images")).toHaveLength(1);

    jest.clearAllMocks();
  });

  it("should render add event", async (): Promise<void> => {
    expect.hasAssertions();

    const images = [
      new File(
        ["okada-unittesting-0192837465"],
        "okada-unittesting-0192837465.png",
        { type: "image/png" }
      ),
      new File(
        ["okada-unittesting-5647382910"],
        "okada-unittesting-0192837465.png",
        { type: "image/png" }
      ),
    ];
    const file = new File(
      ["okada-unittesting-56789abcde"],
      "okada-unittesting-56789abcde.txt",
      {
        type: "text/plain",
      }
    );

    const mockedQueries: readonly MockedResponse[] = [
      {
        request: {
          query: GET_EVENTS,
          variables: {
            groupName: "unittesting",
          },
        },
        result: {
          data: {
            group: {
              events: [
                {
                  closingDate: "-",
                  detail: "Test description",
                  eventDate: "2018-10-17 00:00:00",
                  eventStatus: "SOLVED",
                  eventType: "AUTHORIZATION_SPECIAL_ATTACK",
                  groupName: "unittesting",
                  id: "463457733",
                  root: {
                    __typename: "GitRoot",
                    branch: "master",
                    cloningStatus: {
                      __typename: "GitRootCloningStatus",
                      message: "root created",
                      status: "UNKNOWN",
                    },
                    credentials: {
                      __typename: "Credentials",
                      id: "",
                      name: "",
                      type: "",
                    },
                    environment: "production",
                    environmentUrls: [],
                    gitEnvironmentUrls: [],
                    gitignore: ["bower_components/*", "node_modules/*"],
                    id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
                    includesHealthCheck: true,
                    nickname: "universe",
                    state: "ACTIVE",
                    url: "https://gitlab.com/fluidattacks/universe",
                    useVpn: false,
                  },
                },
              ],
              name: "unittesting",
            },
          },
        },
      },
      {
        request: {
          query: GET_ROOTS,
          variables: { groupName: "unittesting" },
        },
        result: {
          data: {
            group: {
              __typename: "Group",
              codeLanguages: null,
              name: "unittesting",
              roots: [
                {
                  __typename: "GitRoot",
                  branch: "master",
                  cloningStatus: {
                    __typename: "GitRootCloningStatus",
                    message: "root created",
                    status: "UNKNOWN",
                  },
                  credentials: {
                    __typename: "Credentials",
                    id: "",
                    name: "",
                    type: "",
                  },
                  environment: "production",
                  environmentUrls: [],
                  gitEnvironmentUrls: [],
                  gitignore: ["bower_components/*", "node_modules/*"],
                  id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
                  includesHealthCheck: true,
                  nickname: "universe",
                  state: "ACTIVE",
                  url: "https://gitlab.com/fluidattacks/universe",
                  useVpn: false,
                },
              ],
            },
          },
        },
      },
    ];
    const mockedMutations: MockedResponse[] = [
      {
        request: {
          query: ADD_EVENT_MUTATION,
          variables: {
            detail: "detail test",
            eventDate: "2021-09-07T00:00:00Z",
            eventType: "CLONING_ISSUES",
            groupName: "unittesting",
            rootId: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
          },
        },
        result: {
          data: {
            addEvent: {
              eventId: "123",
              success: true,
            },
          },
        },
      },
    ];

    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_add_event_mutate" },
    ]);
    render(
      <MemoryRouter initialEntries={["orgs/okada/groups/unittesting/events"]}>
        <MockedProvider
          addTypename={false}
          mocks={[...mockedQueries, ...mockedMutations]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={GroupEventsView}
              path={"orgs/:organizationName/groups/:groupName/events"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryByText("group.events.btn.text")).toBeInTheDocument();
    });
    await userEvent.click(screen.getByText("group.events.btn.text"));
    await waitFor((): void => {
      expect(screen.queryByText("group.events.new")).toBeInTheDocument();
    });

    expect(screen.getByRole("button", { name: /confirm/iu })).toBeDisabled();

    await userEvent.type(
      screen.getByRole("textbox", { name: "rootNickname" }),
      "universe"
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "detail" }),
      "detail test"
    );

    // 09/07/2021 12:00 AM
    await userEvent.type(
      screen.getByPlaceholderText("mm/dd/yyyy hh:mm (a|p)m"),
      "090720211200A"
    );

    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "eventType" }),
      ["group.events.type.cloningIssues"]
    );
    await userEvent.upload(screen.getByTestId("images"), images);
    await userEvent.upload(screen.getByTestId("files"), file);
    await waitFor((): void => {
      expect(
        screen.getByRole("button", { name: /confirm/iu })
      ).not.toBeDisabled();
    });
    await userEvent.click(screen.getByRole("button", { name: /confirm/iu }));

    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledWith(
        "group.events.successCreate",
        "group.events.titleSuccess"
      );
    });
    jest.clearAllMocks();
  });

  it("should request verification", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedQueries: readonly MockedResponse[] = [
      {
        request: {
          query: GET_EVENTS,
          variables: {
            groupName: "unittesting",
          },
        },
        result: {
          data: {
            group: {
              events: [
                {
                  closingDate: "-",
                  detail: "Test description",
                  eventDate: "2018-10-17 00:00:00",
                  eventStatus: "SOLVED",
                  eventType: "AUTHORIZATION_SPECIAL_ATTACK",
                  groupName: "unittesting",
                  id: "463457733",
                  root: null,
                },
                {
                  closingDate: "-",
                  detail: "Test description",
                  eventDate: "2018-10-17 00:00:00",
                  eventStatus: "CREATED",
                  eventType: "NETWORK_ACCESS_ISSUES",
                  groupName: "unittesting",
                  id: "12314123",
                  root: null,
                },
              ],
              name: "unittesting",
            },
          },
        },
      },
    ];
    const mockedMutations: MockedResponse[] = [
      {
        request: {
          query: REQUEST_EVENT_VERIFICATION_MUTATION,
          variables: {
            comments: "The solution test",
            eventId: "12314123",
          },
        },
        result: {
          data: {
            requestEventVerification: {
              success: true,
            },
          },
        },
      },
    ];

    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_request_event_verification_mutate" },
    ]);
    render(
      <MemoryRouter initialEntries={["/groups/unittesting/events"]}>
        <MockedProvider
          addTypename={false}
          mocks={[...mockedQueries, ...mockedMutations]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={GroupEventsView}
              path={"/groups/:groupName/events"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(
        screen.getByRole("cell", { name: "Network access issues" })
      ).toBeInTheDocument();
    });

    const row = screen.getByRole("row", {
      name: /12314123 2018-10-17 00:00:00 test description network access issues unsolved -/iu,
    });
    await userEvent.click(within(row).getByRole("checkbox"));
    await waitFor((): void => {
      expect(
        screen.queryAllByRole("checkbox", { checked: true })[0]
      ).toBeInTheDocument();
    });

    await userEvent.click(
      screen.getByRole("button", {
        name: /group.events.remediationmodal.btn.text/iu,
      })
    );

    await userEvent.type(
      screen.getByRole("textbox", { name: /treatmentjustification/iu }),
      "The solution test"
    );
    await userEvent.click(
      screen.getByRole("button", { name: /components\.modal\.confirm/iu })
    );

    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledWith(
        "group.events.successRequestVerification",
        "groupAlerts.updatedTitle"
      );
    });
    jest.clearAllMocks();
  });

  it("should handle error in request verification", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedQueries: readonly MockedResponse[] = [
      {
        request: {
          query: GET_EVENTS,
          variables: {
            groupName: "unittesting",
          },
        },
        result: {
          data: {
            group: {
              events: [
                {
                  closingDate: "-",
                  detail: "Test description",
                  eventDate: "2018-10-17 00:00:00",
                  eventStatus: "SOLVED",
                  eventType: "AUTHORIZATION_SPECIAL_ATTACK",
                  groupName: "unittesting",
                  id: "463457733",
                  root: null,
                },
                {
                  closingDate: "-",
                  detail: "Test description",
                  eventDate: "2018-10-17 00:00:00",
                  eventStatus: "CREATED",
                  eventType: "NETWORK_ACCESS_ISSUES",
                  groupName: "unittesting",
                  id: "12314123",
                  root: null,
                },
              ],
              name: "unittesting",
            },
          },
        },
      },
    ];
    const mockedMutations: MockedResponse[] = [
      {
        request: {
          query: REQUEST_EVENT_VERIFICATION_MUTATION,
          variables: {
            comments: "The solution test",
            eventId: "463457733",
          },
        },
        result: {
          errors: [
            new GraphQLError("Exception - The event has already been closed"),
          ],
        },
      },
    ];

    // eslint-disable-next-line
    const mockedPermissions = new PureAbility<string>([  // NOSONAR
      { action: "api_mutations_request_event_verification_mutate" },
    ]);
    render(
      <MemoryRouter initialEntries={["/groups/unittesting/events"]}>
        <MockedProvider
          addTypename={false}
          mocks={[...mockedQueries, ...mockedMutations]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={GroupEventsView}
              path={"/groups/:groupName/events"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(
        screen.getByRole("cell", { name: "Network access issues" })
      ).toBeInTheDocument();
    });

    const rowUnSlv = screen.getByRole("row", {
      name: /12314123 2018-10-17 00:00:00 test description network access issues unsolved -/iu,
    });
    await userEvent.click(within(rowUnSlv).getByRole("checkbox"));
    await waitFor((): void => {
      expect(
        screen.queryAllByRole("checkbox", { checked: true })[0]
      ).toBeInTheDocument();
    });

    const rowSolv = screen.getByRole("row", {
      name: /463457733 2018-10-17 00:00:00 Test description Authorization for a special attack solved -/iu,
    });
    await userEvent.click(within(rowSolv).getByRole("checkbox"));
    await waitFor((): void => {
      expect(
        screen.queryAllByRole("checkbox", { checked: true })[0]
      ).toBeInTheDocument();
    });

    await userEvent.click(
      screen.getByRole("button", {
        name: /group.events.remediationmodal.btn.text/iu,
      })
    );

    expect(msgError).toHaveBeenCalledWith("group.events.selectedError");

    jest.clearAllMocks();
  });
});
