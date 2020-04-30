import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { PureAbility } from "@casl/ability";
import { mount, ReactWrapper, shallow, ShallowWrapper } from "enzyme";
import { GraphQLError } from "graphql";
import * as React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { MemoryRouter } from "react-router-dom";
import wait from "waait";
import store from "../../../../store";
import { authzContext } from "../../../../utils/authz/config";
import { msgError, msgSuccess } from "../../../../utils/notifications";
import { FindingContent } from "./index";
import {
  APPROVE_DRAFT_MUTATION, DELETE_FINDING_MUTATION, GET_FINDING_HEADER, REJECT_DRAFT_MUTATION, SUBMIT_DRAFT_MUTATION,
} from "./queries";
import { IFindingContentProps } from "./types";

jest.mock("../../../../utils/notifications", () => {
  const mockedNotifications: Dictionary = jest.requireActual("../../../../utils/notifications");
  mockedNotifications.msgError = jest.fn();
  mockedNotifications.msgSuccess = jest.fn();

  return mockedNotifications;
});

describe("FindingContent", () => {

  const mockProps: IFindingContentProps = {
    history: {
      action: "PUSH",
      block: (): (() => void) => (): void => undefined,
      createHref: (): string => "",
      go: (): void => undefined,
      goBack: (): void => undefined,
      goForward: (): void => undefined,
      length: 1,
      listen: (): (() => void) => (): void => undefined,
      location: { hash: "", pathname: "/", search: "", state: {} },
      push: (): void => undefined,
      replace: (): void => undefined,
    },
    location: { hash: "", pathname: "/", search: "", state: {} },
    match: {
      isExact: true,
      params: { findingId: "438679960", projectName: "TEST" },
      path: "/",
      url: "",
    },
  };

  const findingMock: Readonly<MockedResponse> = (
    {
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
            title: "FIN.S.0050. Weak passwords discovered",
          },
        },
      },
    }
  );

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
          releaseDate: "",
          reportDate: "2017-12-04 09:04:13",
          severityScore: 2.6,
          state: "open",
          title: "FIN.S.0050. Weak passwords discovered",
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

  it("should return a object", () => {
    expect(typeof (FindingContent))
      .toEqual("function");
  });

  it("should render a component", async () => {
    const wrapper: ShallowWrapper = shallow(
      <MockedProvider mocks={[findingMock]} addTypename={false}>
        <FindingContent {...mockProps} />
      </MockedProvider>,
    );
    await act(async () => { await wait(0); });
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render header", async () => {
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_dataloaders_finding__get_historic_state" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/project/TEST/findings/438679960/description"]}>
        <Provider store={store}>
          <MockedProvider mocks={[findingMock]} addTypename={false}>
            <authzContext.Provider value={mockedPermissions}>
              <FindingContent {...mockProps} />
            </authzContext.Provider>
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper.text())
      .toContain("FIN.S.0050. Weak passwords discovered");
  });

  it("should render unsubmitted draft actions", async () => {
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_dataloaders_finding__get_historic_state" },
      { action: "backend_api_resolvers_finding__do_submit_draft" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/project/TEST/findings/438679960/description"]}>
        <Provider store={store}>
          <MockedProvider mocks={[draftMock]} addTypename={false}>
            <authzContext.Provider value={mockedPermissions}>
              <FindingContent {...mockProps} />
            </authzContext.Provider>
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    const submitButton: ReactWrapper = wrapper.find("ButtonToolbar")
      .at(0)
      .find("Button")
      .filterWhere((element: ReactWrapper) => element.text()
        .includes("Submit"));
    expect(submitButton)
      .toHaveLength(1);
  });

  it("should prompt delete justification", async () => {
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_dataloaders_finding__get_historic_state" },
      { action: "backend_api_resolvers_finding__do_delete_finding" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/project/TEST/findings/438679960/description"]}>
        <Provider store={store}>
          <MockedProvider mocks={[findingMock]} addTypename={false}>
            <authzContext.Provider value={mockedPermissions}>
              <FindingContent {...mockProps} />
            </authzContext.Provider>
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
      .prop("show"))
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
      { action: "backend_api_dataloaders_finding__get_historic_state" },
      { action: "backend_api_resolvers_finding__do_submit_draft" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/project/TEST/findings/438679960/description"]}>
        <Provider store={store}>
          <MockedProvider mocks={[draftMock, submitMutationMock, submittedDraftMock]} addTypename={false}>
            <authzContext.Provider value={mockedPermissions}>
              <FindingContent {...mockProps} />
            </authzContext.Provider>
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(50); wrapper.update(); });
    let submitButton: ReactWrapper = wrapper.find("ButtonToolbar")
      .at(0)
      .find("Button")
      .filterWhere((element: ReactWrapper) => element.text()
        .includes("Submit"));
    submitButton.simulate("click");
    await act(async () => { await wait(0); });
    submitButton = wrapper.find("ButtonToolbar")
      .at(0)
      .find("Button")
      .filterWhere((element: ReactWrapper) => element.text()
        .includes("Submit"));
    expect(submitButton.prop("disabled"))
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
      { action: "backend_api_dataloaders_finding__get_historic_state" },
      { action: "backend_api_resolvers_finding__do_submit_draft" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/project/TEST/findings/438679960/description"]}>
        <Provider store={store}>
          <MockedProvider mocks={[draftMock, submitErrorMock, draftMock]} addTypename={false}>
            <authzContext.Provider value={mockedPermissions}>
              <FindingContent {...mockProps} />
            </authzContext.Provider>
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    const submitButton: ReactWrapper = wrapper.find("ButtonToolbar")
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
      { action: "backend_api_dataloaders_finding__get_historic_state" },
      { action: "backend_api_resolvers_finding__do_approve_draft" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/project/TEST/findings/438679960/description"]}>
        <Provider store={store}>
          <MockedProvider mocks={[submittedDraftMock, approveMutationMock, findingMock]} addTypename={false}>
            <authzContext.Provider value={mockedPermissions}>
              <FindingContent {...mockProps} />
            </authzContext.Provider>
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(50); wrapper.update(); });
    let approveButton: ReactWrapper = wrapper.find("ButtonToolbar")
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
    await act(async () => { await wait(50); wrapper.update(); });
    approveButton = wrapper.find("ButtonToolbar")
      .at(0)
      .find("Button")
      .filterWhere((element: ReactWrapper) => element.text()
        .includes("Approve"));
    expect(approveButton)
      .toHaveLength(0);
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
      { action: "backend_api_dataloaders_finding__get_historic_state" },
      { action: "backend_api_resolvers_finding__do_approve_draft" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/project/TEST/findings/438679960/description"]}>
        <Provider store={store}>
          <MockedProvider mocks={[submittedDraftMock, approveErrorMock, submittedDraftMock]} addTypename={false}>
            <authzContext.Provider value={mockedPermissions}>
              <FindingContent {...mockProps} />
            </authzContext.Provider>
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    const approveButton: ReactWrapper = wrapper.find("ButtonToolbar")
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
      { action: "backend_api_dataloaders_finding__get_historic_state" },
      { action: "backend_api_resolvers_finding__do_reject_draft" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/project/TEST/findings/438679960/description"]}>
        <Provider store={store}>
          <MockedProvider mocks={[submittedDraftMock, rejectMutationMock, findingMock]} addTypename={false}>
            <authzContext.Provider value={mockedPermissions}>
              <FindingContent {...mockProps} />
            </authzContext.Provider>
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(50); wrapper.update(); });
    let rejectButton: ReactWrapper = wrapper.find("ButtonToolbar")
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
    await act(async () => { await wait(100); wrapper.update(); });
    rejectButton = wrapper.find("ButtonToolbar")
      .at(0)
      .find("Button")
      .filterWhere((element: ReactWrapper) => element.text()
        .includes("Reject"));
    expect(rejectButton)
      .toHaveLength(0);
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
      { action: "backend_api_dataloaders_finding__get_historic_state" },
      { action: "backend_api_resolvers_finding__do_reject_draft" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/project/TEST/findings/438679960/description"]}>
        <Provider store={store}>
          <MockedProvider mocks={[submittedDraftMock, rejectErrorMock, submittedDraftMock]} addTypename={false}>
            <authzContext.Provider value={mockedPermissions}>
              <FindingContent {...mockProps} />
            </authzContext.Provider>
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    const rejectButton: ReactWrapper = wrapper.find("ButtonToolbar")
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
      { action: "backend_api_dataloaders_finding__get_historic_state" },
      { action: "backend_api_resolvers_finding__do_delete_finding" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/project/TEST/findings/438679960/description"]}>
        <Provider store={store}>
          <MockedProvider mocks={[findingMock, deleteMutationMock]} addTypename={false}>
            <authzContext.Provider value={mockedPermissions}>
              <FindingContent {...mockProps} />
            </authzContext.Provider>
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
    expect(window.location.hash)
      .toEqual("#!/project/TEST/findings");
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
      { action: "backend_api_dataloaders_finding__get_historic_state" },
      { action: "backend_api_resolvers_finding__do_delete_finding" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/project/TEST/findings/438679960/description"]}>
        <Provider store={store}>
          <MockedProvider mocks={[findingMock, deleteMutationMock]} addTypename={false}>
            <authzContext.Provider value={mockedPermissions}>
              <FindingContent {...mockProps} />
            </authzContext.Provider>
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
