import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { configure, mount, ReactWrapper, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import { GraphQLError } from "graphql";
// tslint:disable-next-line: no-import-side-effect
import "isomorphic-fetch";
import * as React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { MemoryRouter } from "react-router-dom";
import wait from "waait";
import store from "../../../../store";
import { msgError } from "../../../../utils/notifications";
import { GET_PROJECT_ALERT } from "../ProjectContent/queries";
import { FindingContent } from "./index";
import { GET_FINDING_HEADER, SUBMIT_DRAFT_MUTATION } from "./queries";
import { IFindingContentProps } from "./types";

configure({ adapter: new ReactSixteenAdapter() });

jest.mock("../../../../utils/notifications", () => {
  const mockedNotifications: Dictionary = jest.requireActual("../../../../utils/notifications");
  mockedNotifications.msgError = jest.fn();

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
          findingId: "438679960",
          submissionField: true,
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
        findingId: "438679960",
        submissionField: true,
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

  const alertMock: Readonly<MockedResponse> = {
    request: {
      query: GET_PROJECT_ALERT,
      variables: {
        organization: "Fluid",
        projectName: "TEST",
      },
    },
    result: {
      data: {
        alert: {
          message: "Hello world",
          status: 1,
        },
      },
    },
  };

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
    (window as typeof window & { userRole: string }).userRole = "analyst";
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/project/TEST/findings/438679960/description"]}>
        <Provider store={store}>
          <MockedProvider mocks={[findingMock]} addTypename={false}>
            <FindingContent {...mockProps} />
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper.text())
      .toContain("FIN.S.0050. Weak passwords discovered");
  });

  it("should render unsubmitted draft actions", async () => {
    (window as typeof window & { userRole: string }).userRole = "analyst";
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/project/TEST/findings/438679960/description"]}>
        <Provider store={store}>
          <MockedProvider mocks={[draftMock]} addTypename={false}>
            <FindingContent {...mockProps} />
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
    (window as typeof window & { userRole: string }).userRole = "analyst";
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/project/TEST/findings/438679960/description"]}>
        <Provider store={store}>
          <MockedProvider mocks={[findingMock]} addTypename={false}>
            <FindingContent {...mockProps} />
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

    (window as typeof window & { userRole: string }).userRole = "analyst";
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/project/TEST/findings/438679960/description"]}>
        <Provider store={store}>
          <MockedProvider mocks={[draftMock, submitMutationMock, submittedDraftMock]} addTypename={false}>
            <FindingContent {...mockProps} />
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
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
    (window as typeof window & { userRole: string }).userRole = "analyst";
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/project/TEST/findings/438679960/description"]}>
        <Provider store={store}>
          <MockedProvider mocks={[draftMock, submitErrorMock, findingMock]} addTypename={false}>
            <FindingContent {...mockProps} />
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
    await act(async () => { await wait(0); wrapper.update(); });
    expect(msgError)
      .toHaveBeenCalled();
  });

  it("should render alert", async () => {
    (window as typeof window & { userRole: string }).userRole = "analyst";
    (window as typeof window & { userOrganization: string }).userOrganization = "Fluid";
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/project/TEST/findings/438679960/description"]}>
        <Provider store={store}>
          <MockedProvider mocks={[findingMock, alertMock]} addTypename={false}>
            <FindingContent {...mockProps} />
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper.text())
      .toContain("Hello world");
  });
});
