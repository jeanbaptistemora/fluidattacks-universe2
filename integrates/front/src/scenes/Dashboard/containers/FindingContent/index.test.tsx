import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { GraphQLError } from "graphql";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { FindingContent } from "scenes/Dashboard/containers/FindingContent";
import {
  APPROVE_DRAFT_MUTATION,
  GET_FINDING_HEADER,
  REJECT_DRAFT_MUTATION,
  REMOVE_FINDING_MUTATION,
  SUBMIT_DRAFT_MUTATION,
} from "scenes/Dashboard/containers/FindingContent/queries";
import { authzPermissionsContext } from "utils/authz/config";
import { msgError, msgSuccess } from "utils/notifications";

jest.mock("../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary<() => Dictionary> = jest.requireActual(
    "../../../../utils/notifications"
  );
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

const mockHistoryReplace: jest.Mock = jest.fn();

jest.mock(
  "react-router-dom",
  (): Dictionary => ({
    ...jest.requireActual<Dictionary>("react-router-dom"),
    useHistory: (): { replace: (path: string) => void } => ({
      replace: mockHistoryReplace,
    }),
  })
);

describe("FindingContent", (): void => {
  const findingMock: Readonly<MockedResponse> = {
    request: {
      query: GET_FINDING_HEADER,
      variables: {
        canGetHistoricState: true,
        findingId: "438679960",
      },
    },
    result: {
      data: {
        finding: {
          closedVulns: 0,
          historicState: [
            {
              analyst: "someone@fluidattacks.com",
              date: "2019-10-31 10:00:53",
              state: "CREATED",
            },
            {
              analyst: "approver@fluidattacks.com",
              date: "2019-10-31 12:00:00",
              state: "APPROVED",
            },
          ],
          id: "438679960",
          minTimeToRemediate: 60,
          openVulns: 3,
          releaseDate: "2018-12-04 09:04:13",
          reportDate: "2017-12-04 09:04:13",
          severityScore: 2.6,
          state: "open",
          title: "050. Guessed weak credentials",
          tracking: [
            {
              closed: 0,
              cycle: 0,
              date: "2019-08-30",
              effectiveness: 0,
              open: 1,
            },
          ],
        },
      },
    },
  };

  const removeFindingMock: Readonly<MockedResponse> = {
    request: {
      query: GET_FINDING_HEADER,
      variables: {
        canGetHistoricState: true,
        findingId: "438679960",
      },
    },
    result: {
      data: {
        finding: {
          closedVulns: 0,
          historicState: [
            {
              analyst: "someone@fluidattacks.com",
              date: "2019-10-31 10:00:53",
              state: "CREATED",
            },
          ],
          id: "438679960",
          minTimeToRemediate: 60,
          openVulns: 3,
          releaseDate: null,
          reportDate: "2017-12-04 09:04:13",
          severityScore: 2.6,
          state: "open",
          title: "050. Guessed weak credentials",
          tracking: [
            {
              closed: 0,
              cycle: 0,
              date: "2019-08-30",
              effectiveness: 0,
              open: 1,
            },
          ],
        },
      },
    },
  };

  const draftMock: Readonly<MockedResponse> = {
    request: {
      query: GET_FINDING_HEADER,
      variables: {
        canGetHistoricState: true,
        findingId: "438679960",
      },
    },
    result: {
      data: {
        finding: {
          closedVulns: 0,
          historicState: [
            {
              analyst: "someone@fluidattacks.com",
              date: "2019-10-31 10:00:53",
              state: "CREATED",
            },
          ],
          id: "438679960",
          minTimeToRemediate: 60,
          openVulns: 3,
          releaseDate: null,
          reportDate: "2017-12-04 09:04:13",
          severityScore: 2.6,
          state: "open",
          title: "050. Guessed weak credentials",
          tracking: [
            {
              closed: 0,
              cycle: 0,
              date: "2019-08-30",
              effectiveness: 0,
              open: 1,
            },
          ],
        },
      },
    },
  };

  type resultType = Dictionary<{ finding: { historicState: Dictionary[] } }>;
  const result: resultType = draftMock.result as resultType;
  const submittedDraftMock: Readonly<MockedResponse> = {
    ...draftMock,
    result: {
      ...draftMock.result,
      data: {
        ...result.data,
        finding: {
          ...result.data.finding,
          historicState: [
            ...result.data.finding.historicState,
            {
              analyst: "someone@fluidattacks.com",
              date: "2019-10-31 11:30:00",
              state: "SUBMITTED",
            },
          ],
        },
      },
    },
  };

  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof FindingContent).toStrictEqual("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_resolvers_finding_historic_state_resolve" },
    ]);
    render(
      <MemoryRouter initialEntries={["/TEST/vulns/438679960/description"]}>
        <MockedProvider addTypename={false} mocks={[findingMock]}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={FindingContent}
              path={"/:groupName/vulns/:findingId/description"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );

    // Including heading inside `ContentTab`
    const numberOfHeading: number = 6;
    await waitFor((): void => {
      expect(screen.queryAllByRole("heading")).toHaveLength(numberOfHeading);
    });
  });

  it("should render header", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_resolvers_finding_historic_state_resolve" },
    ]);
    render(
      <MemoryRouter initialEntries={["/TEST/vulns/438679960/description"]}>
        <MockedProvider addTypename={false} mocks={[findingMock]}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={FindingContent}
              path={"/:groupName/vulns/:findingId/description"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryByRole("heading", { level: 1 })).toBeInTheDocument();
    });

    expect(screen.getAllByRole("heading")[0].textContent).toContain(
      "050. Guessed weak credentials"
    );
  });

  it("should render unsubmitted draft actions", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_resolvers_finding_historic_state_resolve" },
      { action: "api_mutations_submit_draft_mutate" },
    ]);
    render(
      <MemoryRouter initialEntries={["/TEST/vulns/438679960/description"]}>
        <MockedProvider addTypename={false} mocks={[draftMock]}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={FindingContent}
              path={"/:groupName/vulns/:findingId/description"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(
        screen.queryByText("group.drafts.submit.text")
      ).toBeInTheDocument();
    });

    expect(screen.queryAllByRole("button")).toHaveLength(1);
  });

  it("should prompt delete justification", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_resolvers_finding_historic_state_resolve" },
      { action: "api_mutations_remove_finding_mutate" },
    ]);
    render(
      <MemoryRouter initialEntries={["/TEST/vulns/438679960/description"]}>
        <MockedProvider addTypename={false} mocks={[removeFindingMock]}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={FindingContent}
              path={"/:groupName/vulns/:findingId/description"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.delete.btn.text")
      ).toBeInTheDocument();
    });

    expect(screen.queryAllByRole("button")).toHaveLength(1);

    userEvent.click(screen.getByText("searchFindings.delete.btn.text"));
    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.delete.title")
      ).toBeInTheDocument();
    });

    userEvent.click(screen.getByText("confirmmodal.cancel"));
    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.delete.title")
      ).not.toBeInTheDocument();
    });
  });

  it("should submit draft", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const submitMutationMock: Readonly<MockedResponse> = {
      request: {
        query: SUBMIT_DRAFT_MUTATION,
        variables: {
          findingId: "438679960",
        },
      },
      result: {
        data: {
          submitDraft: {
            success: true,
          },
        },
      },
    };

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_resolvers_finding_historic_state_resolve" },
      { action: "api_mutations_submit_draft_mutate" },
    ]);
    render(
      <MemoryRouter initialEntries={["/TEST/vulns/438679960/description"]}>
        <MockedProvider
          addTypename={false}
          mocks={[draftMock, submitMutationMock, submittedDraftMock]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={FindingContent}
              path={"/:groupName/vulns/:findingId/description"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryByText("group.drafts.submit.text")).not.toBeDisabled();
    });

    userEvent.click(screen.getByText("group.drafts.submit.text"));

    await waitFor((): void => {
      expect(screen.queryByText("group.drafts.submit.text")).toBeDisabled();
    });
  });

  it("should handle submit errors", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const submitErrorMock: Readonly<MockedResponse> = {
      request: {
        query: SUBMIT_DRAFT_MUTATION,
        variables: {
          findingId: "438679960",
        },
      },
      result: {
        errors: [
          new GraphQLError("Exception - This draft has missing fields"),
          new GraphQLError("Exception - This draft has already been submitted"),
          new GraphQLError("Exception - This draft has already been approved"),
          new GraphQLError("Unexpected error"),
        ],
      },
    };

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_resolvers_finding_historic_state_resolve" },
      { action: "api_mutations_submit_draft_mutate" },
    ]);
    render(
      <MemoryRouter initialEntries={["/TEST/vulns/438679960/description"]}>
        <MockedProvider
          addTypename={false}
          mocks={[draftMock, submitErrorMock, draftMock]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={FindingContent}
              path={"/:groupName/vulns/:findingId/description"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryByText("group.drafts.submit.text")).not.toBeDisabled();
    });

    userEvent.click(screen.getByText("group.drafts.submit.text"));

    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledTimes(4);
    });
  });

  it("should approve draft", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const approveMutationMock: Readonly<MockedResponse> = {
      request: {
        query: APPROVE_DRAFT_MUTATION,
        variables: {
          findingId: "438679960",
        },
      },
      result: {
        data: {
          approveDraft: {
            success: true,
          },
        },
      },
    };

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_resolvers_finding_historic_state_resolve" },
      { action: "api_mutations_approve_draft_mutate" },
    ]);
    render(
      <MemoryRouter initialEntries={["/TEST/vulns/438679960/description"]}>
        <MockedProvider
          addTypename={false}
          mocks={[submittedDraftMock, approveMutationMock, findingMock]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={FindingContent}
              path={"/:groupName/vulns/:findingId/description"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(
        screen.queryByText("group.drafts.approve.text")
      ).not.toBeDisabled();
    });

    userEvent.click(screen.getByText("group.drafts.approve.text"));

    await waitFor((): void => {
      expect(
        screen.queryByText("group.drafts.approve.title")
      ).toBeInTheDocument();
    });
    userEvent.click(screen.getByText("confirmmodal.proceed"));
    await waitFor((): void => {
      expect(
        screen.queryByText("group.drafts.approve.text")
      ).not.toBeInTheDocument();
    });
  });

  it("should handle approval errors", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const approveErrorMock: Readonly<MockedResponse> = {
      request: {
        query: APPROVE_DRAFT_MUTATION,
        variables: {
          findingId: "438679960",
        },
      },
      result: {
        errors: [
          new GraphQLError("Exception - This draft has already been approved"),
          new GraphQLError("Exception - The draft has not been submitted yet"),
          new GraphQLError("CANT_APPROVE_FINDING_WITHOUT_VULNS"),
          new GraphQLError("Unexpected error"),
        ],
      },
    };

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_resolvers_finding_historic_state_resolve" },
      { action: "api_mutations_approve_draft_mutate" },
    ]);
    render(
      <MemoryRouter initialEntries={["/TEST/vulns/438679960/description"]}>
        <MockedProvider
          addTypename={false}
          mocks={[submittedDraftMock, approveErrorMock, submittedDraftMock]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={FindingContent}
              path={"/:groupName/vulns/:findingId/description"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(
        screen.queryByText("group.drafts.approve.text")
      ).not.toBeDisabled();
    });

    userEvent.click(screen.getByText("group.drafts.approve.text"));

    await waitFor((): void => {
      expect(
        screen.queryByText("group.drafts.approve.title")
      ).toBeInTheDocument();
    });
    userEvent.click(screen.getByText("confirmmodal.proceed"));
    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledTimes(4);
    });

    expect(screen.queryByText("group.drafts.approve.text")).toBeInTheDocument();
  });

  it("should reject draft", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const rejectMutationMock: Readonly<MockedResponse> = {
      request: {
        query: REJECT_DRAFT_MUTATION,
        variables: {
          findingId: "438679960",
        },
      },
      result: {
        data: {
          rejectDraft: {
            success: true,
          },
        },
      },
    };

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_resolvers_finding_historic_state_resolve" },
      { action: "api_mutations_reject_draft_mutate" },
    ]);
    render(
      <MemoryRouter initialEntries={["/TEST/vulns/438679960/description"]}>
        <MockedProvider
          addTypename={false}
          mocks={[submittedDraftMock, rejectMutationMock, findingMock]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={FindingContent}
              path={"/:groupName/vulns/:findingId/description"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryByText("group.drafts.reject.text")).not.toBeDisabled();
    });

    userEvent.click(screen.getByText("group.drafts.reject.text"));

    await waitFor((): void => {
      expect(
        screen.queryByText("group.drafts.reject.title")
      ).toBeInTheDocument();
    });
    userEvent.click(screen.getByText("confirmmodal.proceed"));
    await waitFor((): void => {
      expect(
        screen.queryByText("group.drafts.reject.title")
      ).not.toBeInTheDocument();
    });
  });

  it("should handle rejection errors", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const rejectErrorMock: Readonly<MockedResponse> = {
      request: {
        query: REJECT_DRAFT_MUTATION,
        variables: {
          findingId: "438679960",
        },
      },
      result: {
        errors: [
          new GraphQLError("Exception - This draft has already been approved"),
          new GraphQLError("Exception - The draft has not been submitted yet"),
          new GraphQLError("Unexpected error"),
        ],
      },
    };

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_resolvers_finding_historic_state_resolve" },
      { action: "api_mutations_reject_draft_mutate" },
    ]);
    render(
      <MemoryRouter initialEntries={["/TEST/vulns/438679960/description"]}>
        <MockedProvider
          addTypename={false}
          mocks={[submittedDraftMock, rejectErrorMock, submittedDraftMock]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={FindingContent}
              path={"/:groupName/vulns/:findingId/description"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.queryByText("group.drafts.reject.text")).not.toBeDisabled();
    });

    userEvent.click(screen.getByText("group.drafts.reject.text"));

    await waitFor((): void => {
      expect(
        screen.queryByText("group.drafts.reject.title")
      ).toBeInTheDocument();
    });
    userEvent.click(screen.getByText("confirmmodal.proceed"));
    const numberOfErrors: number = 3;
    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledTimes(numberOfErrors);
    });
  });

  it("should delete finding", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const deleteMutationMock: Readonly<MockedResponse> = {
      request: {
        query: REMOVE_FINDING_MUTATION,
        variables: {
          findingId: "438679960",
          justification: "DUPLICATED",
        },
      },
      result: {
        data: {
          removeFinding: {
            success: true,
          },
        },
      },
    };

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_resolvers_finding_historic_state_resolve" },
      { action: "api_mutations_remove_finding_mutate" },
    ]);
    render(
      <MemoryRouter initialEntries={["/TEST/vulns/438679960/description"]}>
        <MockedProvider
          addTypename={false}
          mocks={[removeFindingMock, deleteMutationMock]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={FindingContent}
              path={"/:groupName/vulns/:findingId/description"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.delete.btn.text")
      ).not.toBeDisabled();
    });

    userEvent.click(screen.getByText("searchFindings.delete.btn.text"));

    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.delete.title")
      ).toBeInTheDocument();
    });
    userEvent.selectOptions(
      screen.getByRole("combobox", { name: "justification" }),
      ["DUPLICATED"]
    );

    userEvent.click(screen.getByText("confirmmodal.proceed"));

    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledTimes(1);
    });
  });

  it("should handle deletion errors", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const deleteMutationMock: Readonly<MockedResponse> = {
      request: {
        query: REMOVE_FINDING_MUTATION,
        variables: {
          findingId: "438679960",
          justification: "DUPLICATED",
        },
      },
      result: {
        errors: [new GraphQLError("Unexpected error")],
      },
    };

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_resolvers_finding_historic_state_resolve" },
      { action: "api_mutations_remove_finding_mutate" },
    ]);
    render(
      <MemoryRouter initialEntries={["/TEST/vulns/438679960/description"]}>
        <MockedProvider
          addTypename={false}
          mocks={[removeFindingMock, deleteMutationMock]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={FindingContent}
              path={"/:groupName/vulns/:findingId/description"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.delete.btn.text")
      ).not.toBeDisabled();
    });

    userEvent.click(screen.getByText("searchFindings.delete.btn.text"));

    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.delete.title")
      ).toBeInTheDocument();
    });
    userEvent.selectOptions(
      screen.getByRole("combobox", { name: "justification" }),
      ["DUPLICATED"]
    );

    userEvent.click(screen.getByText("confirmmodal.proceed"));

    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledTimes(1);
    });
  });
});
