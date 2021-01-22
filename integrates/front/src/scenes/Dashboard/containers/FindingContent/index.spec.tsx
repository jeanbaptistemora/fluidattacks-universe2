import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { PureAbility } from "@casl/ability";
import { mount, ReactWrapper, shallow, ShallowWrapper } from "enzyme";
import { GraphQLError } from "graphql";
import * as React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { MemoryRouter, Route } from "react-router-dom";
import wait from "waait";
import waitForExpect from "wait-for-expect";

import { FindingContent } from "scenes/Dashboard/containers/FindingContent";
import {
  APPROVE_DRAFT_MUTATION, DELETE_FINDING_MUTATION, GET_FINDING_HEADER, REJECT_DRAFT_MUTATION, SUBMIT_DRAFT_MUTATION,
} from "scenes/Dashboard/containers/FindingContent/queries";
import store from "store";
import { authzGroupContext, authzPermissionsContext } from "utils/authz/config";
import { msgError, msgSuccess } from "utils/notifications";

jest.mock("../../../../utils/notifications", () => {
  const mockedNotifications: Dictionary = jest.requireActual("../../../../utils/notifications");
  mockedNotifications.msgError = jest.fn();
  mockedNotifications.msgSuccess = jest.fn();

  return mockedNotifications;
});
const mockHistoryReplace: jest.Mock = jest.fn();

jest.mock("react-router-dom", () => ({
  ...jest.requireActual<Dictionary>("react-router-dom"),
  useHistory: (): { replace(path: string): void } => ({
    replace: mockHistoryReplace,
  }),
}));

describe("FindingContent", () => {
  const findingMock: Readonly<MockedResponse> = (
    {
      request: {
        query: GET_FINDING_HEADER,
        variables: {
          canGetExploit: true,
          canGetHistoricState: true,
          findingId: "438679960",
        },
      },
      result: {
        data: {
          finding: {
            closedVulns: 0,
            exploit: "Asserts Code",
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
            title: "FIN.S.0050. Weak passwords discovered",
            tracking: [{
              closed: 0,
              cycle: 0,
              date: "2019-08-30",
              effectiveness: 0,
              open: 1,
            }],
          },
        },
      },
    }
  );

  const draftMock: Readonly<MockedResponse> = {
    request: {
      query: GET_FINDING_HEADER,
      variables: {
        canGetExploit: true,
        canGetHistoricState: true,
        findingId: "438679960",
      },
    },
    result: {
      data: {
        finding: {
          closedVulns: 0,
          exploit: "",
          historicState: [
            {
              analyst: "someone@fluidattacks.com",
              date: "2019-10-31 10:00:53",
              state: "CREATED",
            },
          ],
          id: "438679960",
          openVulns: 3,
          releaseDate: "",
          reportDate: "2017-12-04 09:04:13",
          severityScore: 2.6,
          state: "open",
          title: "FIN.S.0050. Weak passwords discovered",
          tracking: [{
            closed: 0,
            cycle: 0,
            date: "2019-08-30",
            effectiveness: 0,
            open: 1,
          }],
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

  it("should return a function", () => {
    expect(typeof (FindingContent))
      .toEqual("function");
  });

  it("should render a component", async () => {
    const wrapper: ShallowWrapper = shallow(
      <MemoryRouter initialEntries={["/TEST/vulns/438679960/description"]}>
        <MockedProvider mocks={[findingMock]} addTypename={false}>
          <Route path={"/:projectName/vulns/:findingId/description"} component={FindingContent} />
        </MockedProvider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); });
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render header", async () => {
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_finding_historic_state_resolve" },
    ]);
    const mockedGroupPermissions: PureAbility<string> = new PureAbility([
      { action: "has_forces" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/vulns/438679960/description"]}>
        <Provider store={store}>
          <MockedProvider mocks={[findingMock]} addTypename={false}>
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <authzGroupContext.Provider value={mockedGroupPermissions}>
              <Route path={"/:projectName/vulns/:findingId/description"} component={FindingContent} />
              </authzGroupContext.Provider>
            </authzPermissionsContext.Provider>
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper.text())
      .toContain("FIN.S.0050. Weak passwords discovered");
  });

  it("should render header with Exploit tab", async () => {
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_finding_historic_state_resolve" },
    ]);
    const mockedGroupPermissions: PureAbility<string> = new PureAbility([
      { action: "has_forces" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/vulns/438679960/description"]}>
        <Provider store={store}>
          <MockedProvider mocks={[findingMock]} addTypename={false}>
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <authzGroupContext.Provider value={mockedGroupPermissions}>
                <Route path={"/:projectName/vulns/:findingId/description"} component={FindingContent} />
              </authzGroupContext.Provider>
            </authzPermissionsContext.Provider>
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper.find("#exploitItem")
      .hostNodes())
      .toHaveLength(1);
  });

  it("should render header without Exploit tab", async () => {
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_finding_historic_state_resolve" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/vulns/438679960/description"]}>
        <Provider store={store}>
          <MockedProvider mocks={[draftMock]} addTypename={false}>
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <Route path={"/:projectName/vulns/:findingId/description"} component={FindingContent} />
            </authzPermissionsContext.Provider>
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper.find("#exploitItem"))
      .toHaveLength(0);
  });

  it("should render empty Exploit tab for analyst", async () => {
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_finding_historic_state_resolve" },
      { action: "backend_api_mutations_update_evidence_mutate" },
    ]);
    const mockedGroupPermissions: PureAbility<string> = new PureAbility([
      { action: "has_forces" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/vulns/438679960/description"]}>
        <Provider store={store}>
          <MockedProvider mocks={[draftMock]} addTypename={false}>
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <authzGroupContext.Provider value={mockedGroupPermissions}>
                <Route path={"/:projectName/vulns/:findingId/description"} component={FindingContent} />
              </authzGroupContext.Provider>
            </authzPermissionsContext.Provider>
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper.find("#exploitItem")
      .hostNodes())
      .toHaveLength(1);
  });

  it("should render unsubmitted draft actions", async () => {
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_finding_historic_state_resolve" },
      { action: "backend_api_mutations_submit_draft_mutate" },
    ]);
    const mockedGroupPermissions: PureAbility<string> = new PureAbility([
      { action: "has_forces" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/vulns/438679960/description"]}>
        <Provider store={store}>
          <MockedProvider mocks={[draftMock]} addTypename={false}>
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <authzGroupContext.Provider value={mockedGroupPermissions}>
                <Route path={"/:projectName/vulns/:findingId/description"} component={FindingContent} />
              </authzGroupContext.Provider>
            </authzPermissionsContext.Provider>
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    const submitButton: ReactWrapper = wrapper.find("findingContent")
      .at(0)
      .find("Button")
      .filterWhere((element: ReactWrapper) => element.text()
        .includes("Submit"));
    expect(submitButton)
      .toHaveLength(1);
  });

  it("should prompt delete justification", async () => {
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_finding_historic_state_resolve" },
      { action: "backend_api_mutations_delete_finding_mutate" },
    ]);
    const mockedGroupPermissions: PureAbility<string> = new PureAbility([
      { action: "has_forces" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/vulns/438679960/description"]}>
        <Provider store={store}>
          <MockedProvider mocks={[findingMock]} addTypename={false}>
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <authzGroupContext.Provider value={mockedGroupPermissions}>
                <Route path={"/:projectName/vulns/:findingId/description"} component={FindingContent} />
              </authzGroupContext.Provider>
            </authzPermissionsContext.Provider>
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    const deleteButton: ReactWrapper = wrapper.find("button")
      .at(0);
    expect(deleteButton)
      .toHaveLength(1);
    deleteButton.simulate("click");
    expect(wrapper.text())
      .toContain("Delete Finding");
    await act(async () => { wrapper.update(); });
    expect(wrapper.text())
      .toContain("It is a false positive");
    const cancelButton: ReactWrapper = wrapper.find("Modal")
      .find("button")
      .at(0);
    expect(cancelButton)
      .toHaveLength(1);
    cancelButton.simulate("click");
    await act(async () => { wrapper.update(); });
    expect(wrapper.find("Modal")
      .at(0)
      .prop("open"))
      .toEqual(false);
  });

  it("should submit draft", async () => {
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
      { action: "backend_api_resolvers_finding_historic_state_resolve" },
      { action: "backend_api_mutations_submit_draft_mutate" },
    ]);
    const mockedGroupPermissions: PureAbility<string> = new PureAbility([
      { action: "has_forces" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/vulns/438679960/description"]}>
        <Provider store={store}>
          <MockedProvider mocks={[draftMock, submitMutationMock, submittedDraftMock]} addTypename={false}>
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <authzGroupContext.Provider value={mockedGroupPermissions}>
                <Route path={"/:projectName/vulns/:findingId/description"} component={FindingContent} />
              </authzGroupContext.Provider>
            </authzPermissionsContext.Provider>
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await act(async () => {
      await waitForExpect(() => {
        wrapper.update();
        const submitButton: ReactWrapper = wrapper.find("findingContent")
          .at(0)
          .find("Button")
          .filterWhere((element: ReactWrapper) => element.text()
            .includes("Submit"));
        submitButton.simulate("click");
      });
    });
    await act(async () => { await wait(0); });
    const submitButtonAfterSubmit: ReactWrapper = wrapper.find("findingContent")
      .at(0)
      .find("Button")
      .filterWhere((element: ReactWrapper) => element.text()
        .includes("Submit"));
    expect(submitButtonAfterSubmit.prop("disabled"))
      .toEqual(true);
  });

  it("should handle submit errors", async () => {
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
      { action: "backend_api_resolvers_finding_historic_state_resolve" },
      { action: "backend_api_mutations_submit_draft_mutate" },
    ]);
    const mockedGroupPermissions: PureAbility<string> = new PureAbility([
      { action: "has_forces" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/vulns/438679960/description"]}>
        <Provider store={store}>
          <MockedProvider mocks={[draftMock, submitErrorMock, draftMock]} addTypename={false}>
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <authzGroupContext.Provider value={mockedGroupPermissions}>
                <Route path={"/:projectName/vulns/:findingId/description"} component={FindingContent} />
              </authzGroupContext.Provider>
            </authzPermissionsContext.Provider>
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    const submitButton: ReactWrapper = wrapper.find("findingContent")
      .at(0)
      .find("Button")
      .filterWhere((element: ReactWrapper) => element.text()
        .includes("Submit"));
    submitButton.simulate("click");
    await act(async () => { await wait(0); });
    expect(msgError)
      .toHaveBeenCalled();
  });

  it("should approve draft", async () => {
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
      { action: "backend_api_resolvers_finding_historic_state_resolve" },
      { action: "backend_api_mutations_approve_draft_mutate" },
    ]);
    const mockedGroupPermissions: PureAbility<string> = new PureAbility([
      { action: "has_forces" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/vulns/438679960/description"]}>
        <Provider store={store}>
          <MockedProvider mocks={[submittedDraftMock, approveMutationMock, findingMock]} addTypename={false}>
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <authzGroupContext.Provider value={mockedGroupPermissions}>
                <Route path={"/:projectName/vulns/:findingId/description"} component={FindingContent} />
              </authzGroupContext.Provider>
            </authzPermissionsContext.Provider>
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await act(async () => {
      await waitForExpect(() => {
        wrapper.update();
        const approveButton: ReactWrapper = wrapper.find("findingContent")
          .at(0)
          .find("Button")
          .filterWhere((element: ReactWrapper) => element.text()
            .includes("Approve"));
        approveButton.simulate("click");
      });
    });
    await act(async () => { wrapper.update(); });
    const confirmDialog: ReactWrapper = wrapper.find("findingActions")
      .find("Modal")
      .at(0);
    expect(confirmDialog)
      .toHaveLength(1);
    const proceedButton: ReactWrapper = confirmDialog
      .find("Button")
      .at(1);
    proceedButton.simulate("click");
    await act(async () => {
      await waitForExpect(() => {
        wrapper.update();
        const approveButtonAfterProceed: ReactWrapper = wrapper.find("findingContent")
          .at(0)
          .find("Button")
          .filterWhere((element: ReactWrapper) => element.text()
            .includes("Approve"));
        expect(approveButtonAfterProceed)
          .toHaveLength(0);
      });
    });
  });

  it("should handle approval errors", async () => {
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
      { action: "backend_api_resolvers_finding_historic_state_resolve" },
      { action: "backend_api_mutations_approve_draft_mutate" },
    ]);
    const mockedGroupPermissions: PureAbility<string> = new PureAbility([
      { action: "has_forces" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/vulns/438679960/description"]}>
        <Provider store={store}>
          <MockedProvider mocks={[submittedDraftMock, approveErrorMock, submittedDraftMock]} addTypename={false}>
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <authzGroupContext.Provider value={mockedGroupPermissions}>
                <Route path={"/:projectName/vulns/:findingId/description"} component={FindingContent} />
              </authzGroupContext.Provider>
            </authzPermissionsContext.Provider>
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    const approveButton: ReactWrapper = wrapper.find("findingContent")
      .at(0)
      .find("Button")
      .filterWhere((element: ReactWrapper) => element.text()
        .includes("Approve"));
    approveButton.simulate("click");
    await act(async () => { wrapper.update(); });
    const confirmDialog: ReactWrapper = wrapper.find("findingActions")
      .find("Modal")
      .at(0);
    expect(confirmDialog)
      .toHaveLength(1);
    const proceedButton: ReactWrapper = confirmDialog
      .find("Button")
      .at(1);
    proceedButton.simulate("click");
    await act(async () => { await wait(0); });
    expect(msgError)
      .toHaveBeenCalled();
  });

  it("should reject draft", async () => {
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
      { action: "backend_api_resolvers_finding_historic_state_resolve" },
      { action: "backend_api_mutations_reject_draft_mutate" },
    ]);
    const mockedGroupPermissions: PureAbility<string> = new PureAbility([
      { action: "has_forces" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/vulns/438679960/description"]}>
        <Provider store={store}>
          <MockedProvider mocks={[submittedDraftMock, rejectMutationMock, findingMock]} addTypename={false}>
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <authzGroupContext.Provider value={mockedGroupPermissions}>
                <Route path={"/:projectName/vulns/:findingId/description"} component={FindingContent} />
              </authzGroupContext.Provider>
            </authzPermissionsContext.Provider>
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await act(async () => {
      await waitForExpect(() => {
        wrapper.update();
        const rejectButton: ReactWrapper = wrapper.find("findingContent")
          .at(0)
          .find("Button")
          .filterWhere((element: ReactWrapper) => element.text()
            .includes("Reject"));
        rejectButton.simulate("click");
      });
    });
    await act(async () => { wrapper.update(); });
    const confirmDialog: ReactWrapper = wrapper.find("findingActions")
      .find("Modal")
      .at(0);
    expect(confirmDialog)
      .toHaveLength(1);
    const proceedButton: ReactWrapper = confirmDialog
      .find("Button")
      .at(1);
    proceedButton.simulate("click");
    await act(async () => {
      await waitForExpect(() => {
        wrapper.update();
        const rejectButtonAfterProceed: ReactWrapper = wrapper.find("findingContent")
          .at(0)
          .find("Button")
          .filterWhere((element: ReactWrapper) => element.text()
            .includes("Reject"));
        expect(rejectButtonAfterProceed)
          .toHaveLength(0);
      });
    });
  });

  it("should handle rejection errors", async () => {
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
      { action: "backend_api_resolvers_finding_historic_state_resolve" },
      { action: "backend_api_mutations_reject_draft_mutate" },
    ]);
    const mockedGroupPermissions: PureAbility<string> = new PureAbility([
      { action: "has_forces" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/vulns/438679960/description"]}>
        <Provider store={store}>
          <MockedProvider mocks={[submittedDraftMock, rejectErrorMock, submittedDraftMock]} addTypename={false}>
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <authzGroupContext.Provider value={mockedGroupPermissions}>
                <Route path={"/:projectName/vulns/:findingId/description"} component={FindingContent} />
              </authzGroupContext.Provider>
            </authzPermissionsContext.Provider>
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    const rejectButton: ReactWrapper = wrapper.find("findingContent")
      .at(0)
      .find("Button")
      .filterWhere((element: ReactWrapper) => element.text()
        .includes("Reject"));
    rejectButton.simulate("click");
    await act(async () => { wrapper.update(); });
    const confirmDialog: ReactWrapper = wrapper.find("findingActions")
      .find("Modal")
      .at(0);
    expect(confirmDialog)
      .toHaveLength(1);
    const proceedButton: ReactWrapper = confirmDialog
      .find("Button")
      .at(1);
    proceedButton.simulate("click");
    await act(async () => { await wait(0); });
    expect(msgError)
      .toHaveBeenCalled();
  });

  it("should delete finding", async () => {
    const deleteMutationMock: Readonly<MockedResponse> = {
      request: {
        query: DELETE_FINDING_MUTATION,
        variables: {
          findingId: "438679960",
          justification: "DUPLICATED",
        },
      },
      result: {
        data: {
          deleteFinding: {
            success: true,
          },
        },
      },
    };

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_finding_historic_state_resolve" },
      { action: "backend_api_mutations_delete_finding_mutate" },
    ]);
    const mockedGroupPermissions: PureAbility<string> = new PureAbility([
      { action: "has_forces" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/vulns/438679960/description"]}>
        <Provider store={store}>
          <MockedProvider mocks={[findingMock, deleteMutationMock]} addTypename={false}>
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <authzGroupContext.Provider value={mockedGroupPermissions}>
                <Route path={"/:projectName/vulns/:findingId/description"} component={FindingContent} />
              </authzGroupContext.Provider>
            </authzPermissionsContext.Provider>
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    const deleteButton: ReactWrapper = wrapper.find("button")
      .at(0);
    expect(deleteButton)
      .toHaveLength(1);
    deleteButton.simulate("click");
    await act(async () => { wrapper.update(); });
    wrapper.find("select")
      .simulate("change", { target: { value: "DUPLICATED" } });
    const justificationForm: ReactWrapper = wrapper.find("genericForm")
      .find({ name: "deleteFinding" });
    justificationForm.simulate("submit");
    await act(async () => { await wait(0); wrapper.update(); });
    expect(msgSuccess)
      .toHaveBeenCalled();
    expect(mockHistoryReplace)
      .toHaveBeenCalledWith("/groups/TEST/vulns");
  });

  it("should handle deletion errors", async () => {
    const deleteMutationMock: Readonly<MockedResponse> = {
      request: {
        query: DELETE_FINDING_MUTATION,
        variables: {
          findingId: "438679960",
          justification: "DUPLICATED",
        },
      },
      result: {
        errors: [
          new GraphQLError("Unexpected error"),
        ],
      },
    };

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_finding_historic_state_resolve" },
      { action: "backend_api_mutations_delete_finding_mutate" },
    ]);
    const mockedGroupPermissions: PureAbility<string> = new PureAbility([
      { action: "has_forces" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/vulns/438679960/description"]}>
        <Provider store={store}>
          <MockedProvider mocks={[findingMock, deleteMutationMock]} addTypename={false}>
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <authzGroupContext.Provider value={mockedGroupPermissions}>
                <Route path={"/:projectName/vulns/:findingId/description"} component={FindingContent} />
              </authzGroupContext.Provider>
            </authzPermissionsContext.Provider>
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    const deleteButton: ReactWrapper = wrapper.find("button")
      .at(0);
    expect(deleteButton)
      .toHaveLength(1);
    deleteButton.simulate("click");
    await act(async () => { wrapper.update(); });
    wrapper.find("select")
      .simulate("change", { target: { value: "DUPLICATED" } });
    const justificationForm: ReactWrapper = wrapper.find("genericForm")
      .find({ name: "deleteFinding" });
    justificationForm.simulate("submit");
    await act(async () => { await wait(0); });
    expect(msgError)
      .toHaveBeenCalled();
  });
});
