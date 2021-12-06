import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import type { ReactWrapper, ShallowWrapper } from "enzyme";
import { mount, shallow } from "enzyme";
import { GraphQLError } from "graphql";
import React from "react";
import { act } from "react-dom/test-utils";
import { MemoryRouter, Route } from "react-router-dom";
import wait from "waait";
import waitForExpect from "wait-for-expect";

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

    const wrapper: ShallowWrapper = shallow(
      <MemoryRouter initialEntries={["/TEST/vulns/438679960/description"]}>
        <MockedProvider addTypename={false} mocks={[findingMock]}>
          <Route
            component={FindingContent}
            path={"/:groupName/vulns/:findingId/description"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      await wait(0);
    });

    expect(wrapper).toHaveLength(1);
  });

  it("should render header", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_resolvers_finding_historic_state_resolve" },
    ]);
    const wrapper: ReactWrapper = mount(
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
    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper.text()).toContain("050. Guessed weak credentials");
      });
    });
  });

  it("should render unsubmitted draft actions", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_resolvers_finding_historic_state_resolve" },
      { action: "api_mutations_submit_draft_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
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
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });
    const submitButton: ReactWrapper = wrapper
      .find("findingContent")
      .at(0)
      .find("Button")
      .filterWhere((element: ReactWrapper): boolean =>
        element.text().includes("Submit")
      );

    expect(submitButton).toHaveLength(1);
  });

  it("should prompt delete justification", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_resolvers_finding_historic_state_resolve" },
      { action: "api_mutations_remove_finding_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
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
    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper.find("button").at(0)).toHaveLength(1);
      });
    });

    const deleteButton: ReactWrapper = wrapper.find("button").at(0);
    deleteButton.simulate("click");

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper.find("Modal").find("button").at(0)).toHaveLength(1);
      });
    });
    const cancelButton: ReactWrapper = wrapper
      .find("Modal")
      .find("button")
      .at(0);

    cancelButton.simulate("click");
    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper.find("Modal").find("button").at(0)).toHaveLength(0);
      });
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
    const wrapper: ReactWrapper = mount(
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
    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();
        const submitButton: ReactWrapper = wrapper
          .find("findingContent")
          .at(0)
          .find("Button")
          .filterWhere((element: ReactWrapper): boolean =>
            element.text().includes("Submit")
          );
        submitButton.simulate("click");
      });
    });
    await act(async (): Promise<void> => {
      await wait(0);
    });
    const submitButtonAfterSubmit: ReactWrapper = wrapper
      .find("findingContent")
      .at(0)
      .find("Button")
      .filterWhere((element: ReactWrapper): boolean =>
        element.text().includes("Submit")
      );

    expect(submitButtonAfterSubmit.prop("disabled")).toStrictEqual(true);
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
    const wrapper: ReactWrapper = mount(
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
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });
    const submitButton: ReactWrapper = wrapper
      .find("findingContent")
      .at(0)
      .find("Button")
      .filterWhere((element: ReactWrapper): boolean =>
        element.text().includes("Submit")
      );
    submitButton.simulate("click");
    await act(async (): Promise<void> => {
      await wait(0);
    });

    expect(msgError).toHaveBeenCalledTimes(4);
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
    const wrapper: ReactWrapper = mount(
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
    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();
        const approveButton: ReactWrapper = wrapper
          .find("findingContent")
          .at(0)
          .find("Button")
          .filterWhere((element: ReactWrapper): boolean =>
            element.text().includes("Approve")
          );
        approveButton.simulate("click");
      });
    });
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });
    const confirmDialog: ReactWrapper = wrapper
      .find("findingActions")
      .find("Modal")
      .at(0);

    expect(confirmDialog).toHaveLength(1);

    const proceedButton: ReactWrapper = confirmDialog.find("Button").at(1);
    proceedButton.simulate("click");
    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();
        const approveButtonAfterProceed: ReactWrapper = wrapper
          .find("findingContent")
          .at(0)
          .find("Button")
          .filterWhere((element: ReactWrapper): boolean =>
            element.text().includes("Approve")
          );

        expect(approveButtonAfterProceed).toHaveLength(0);
      });
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
    const wrapper: ReactWrapper = mount(
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
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });
    const approveButton: ReactWrapper = wrapper
      .find("findingContent")
      .at(0)
      .find("Button")
      .filterWhere((element: ReactWrapper): boolean =>
        element.text().includes("Approve")
      );
    approveButton.simulate("click");
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });
    const confirmDialog: ReactWrapper = wrapper
      .find("findingActions")
      .find("Modal")
      .at(0);

    expect(confirmDialog).toHaveLength(1);

    const proceedButton: ReactWrapper = confirmDialog.find("Button").at(1);
    proceedButton.simulate("click");
    await act(async (): Promise<void> => {
      await wait(0);
    });

    expect(msgError).toHaveBeenCalledTimes(4);
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
    const wrapper: ReactWrapper = mount(
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
    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();
        const rejectButton: ReactWrapper = wrapper
          .find("findingContent")
          .at(0)
          .find("Button")
          .filterWhere((element: ReactWrapper): boolean =>
            element.text().includes("Reject")
          );
        rejectButton.simulate("click");
      });
    });
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });
    const confirmDialog: ReactWrapper = wrapper
      .find("findingActions")
      .find("Modal")
      .at(0);

    expect(confirmDialog).toHaveLength(1);

    const proceedButton: ReactWrapper = confirmDialog.find("Button").at(1);
    proceedButton.simulate("click");
    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();
        const rejectButtonAfterProceed: ReactWrapper = wrapper
          .find("findingContent")
          .at(0)
          .find("Button")
          .filterWhere((element: ReactWrapper): boolean =>
            element.text().includes("Reject")
          );

        expect(rejectButtonAfterProceed).toHaveLength(0);
      });
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
    const wrapper: ReactWrapper = mount(
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

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(
          wrapper
            .find("findingContent")
            .at(0)
            .find("Button")
            .filterWhere((element: ReactWrapper): boolean =>
              element.text().includes("Reject")
            )
        ).toHaveLength(1);
      });
    });
    const rejectButton: ReactWrapper = wrapper
      .find("findingContent")
      .at(0)
      .find("Button")
      .filterWhere((element: ReactWrapper): boolean =>
        element.text().includes("Reject")
      );
    rejectButton.simulate("click");
    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(
          wrapper.find("findingActions").find("Modal").first()
        ).toHaveLength(1);
      });
    });

    const confirmDialog: ReactWrapper = wrapper
      .find("findingActions")
      .find("Modal")
      .first();
    const proceedButton: ReactWrapper = confirmDialog.find("Button").at(1);
    const numberOfErrors: number = 3;
    proceedButton.simulate("click");
    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(msgError).toHaveBeenCalledTimes(numberOfErrors);
      });
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
    const wrapper: ReactWrapper = mount(
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
    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper.find("button").at(0)).toHaveLength(1);
      });
    });
    const deleteButton: ReactWrapper = wrapper.find("button").at(0);
    deleteButton.simulate("click");

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper.find("Modal").first()).toHaveLength(1);
      });
    });
    wrapper.find("select").simulate("change", {
      target: { name: "justification", value: "DUPLICATED" },
    });

    const justificationForm: ReactWrapper = wrapper
      .find("Formik")
      .find({ name: "removeFinding" });
    justificationForm.simulate("submit");

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(msgSuccess).toHaveBeenCalledTimes(1);
      });
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
    const wrapper: ReactWrapper = mount(
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
    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper.find("button").at(0)).toHaveLength(1);
      });
    });

    const deleteButton: ReactWrapper = wrapper.find("button").at(0);
    deleteButton.simulate("click");

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper.find("Modal").first()).toHaveLength(1);
      });
    });

    wrapper.find("select").simulate("change", {
      target: { name: "justification", value: "DUPLICATED" },
    });
    const justificationForm: ReactWrapper = wrapper
      .find("Formik")
      .find({ name: "removeFinding" });
    justificationForm.simulate("submit");

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(msgError).toHaveBeenCalledTimes(1);
      });
    });
  });
});
