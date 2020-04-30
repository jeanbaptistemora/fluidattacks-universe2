import { MockedProvider, MockedResponse, wait } from "@apollo/react-testing";
import { mount, ReactWrapper } from "enzyme";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import store from "../../../../store";
import { DescriptionView, DescriptionViewProps } from "./index";
import { GET_FINDING_DESCRIPTION } from "./queries";

describe("Finding Description", () => {

  const mockedProps: DescriptionViewProps = {
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
      params: { findingId: "413372600", projectName: "TEST" },
      path: "/",
      url: "",
    },
  };

  const descriptionQuery: Readonly<MockedResponse> = {
    request: {
      query: GET_FINDING_DESCRIPTION,
      variables: {
        canRetrieveAnalyst: false,
        findingId: "413372600",
        projectName: "TEST",
      },
    },
    result: {
      data: {
        finding: {
          actor: "ANY_EMPLOYEE",
          affectedSystems: "BWAPP Server",
          attackVectorDesc: "Run a reverse shell",
          btsUrl: "https://gitlab.com/fluidattacks/something/-/issues",
          compromisedAttributes: "Server files",
          compromisedRecords: 204,
          cweUrl: "94",
          description: "It's possible to execute shell commands from the site",
          historicTreatment: [],
          id: "413372600",
          newRemediated: false,
          openVulnerabilities: 0,
          recommendation: "Use good security practices and standards",
          requirements: "REQ.0265. System must restrict access",
          scenario: "ANONYMOUS_INTERNET",
          state: "open",
          threat: "External attack",
          title: "FIN.S.0004. Remote command execution",
          type: "SECURITY",
          verified: true,
        },
        project: {
          subscription: "continuous",
        },
      },
    },
  };

  it("should return a function", () => {
    expect(typeof (DescriptionView))
      .toEqual("function");
  });

  it("should render a component", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={[descriptionQuery]} addTypename={false}>
          <DescriptionView {...mockedProps} />
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(50); wrapper.update(); });
    expect(wrapper)
      .toHaveLength(1);
    expect(wrapper
      .find("Button")
      .filterWhere((button: ReactWrapper): boolean =>
        button
          .text()
          .includes("Edit")))
      .toHaveLength(1);
  });
});
