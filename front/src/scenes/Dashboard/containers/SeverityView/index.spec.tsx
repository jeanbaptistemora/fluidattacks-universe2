import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { PureAbility } from "@casl/ability";
import { mount, ReactWrapper } from "enzyme";
import { GraphQLError } from "graphql";
import * as React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { RouteComponentProps } from "react-router";
import wait from "waait";
import store from "../../../../store/index";
import { authzContext } from "../../../../utils/authz/config";
import { SeverityView } from "./index";
import { GET_SEVERITY } from "./queries";

describe("SeverityView", () => {

  const mockProps: RouteComponentProps<{ findingId: string }> = {
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
    match: { isExact: true, params: { findingId: "438679960" }, path: "/", url: "" },
  };

  const mocks: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: GET_SEVERITY,
        variables: {
          identifier: "438679960",
        },
      },
      result: {
        data: {
          finding: {
            cvssVersion: "3",
            id: "468603225",
            severity: {
              attackComplexity: 0.77,
              attackVector: 0.85,
              availabilityImpact: 0.56,
              availabilityRequirement: 1.5,
              confidentialityImpact: 0.56,
              confidentialityRequirement: 1.5,
              exploitability: 1,
              integrityImpact: 0.56,
              integrityRequirement: 1.5,
              modifiedAttackComplexity: 0.44,
              modifiedAttackVector: 0.62,
              modifiedAvailabilityImpact: 0,
              modifiedConfidentialityImpact: 0.22,
              modifiedIntegrityImpact: 0.22,
              modifiedPrivilegesRequired: 0.85,
              modifiedSeverityScope: 0,
              modifiedUserInteraction: 0.85,
              privilegesRequired: 0.85,
              remediationLevel: 1,
              reportConfidence: 1,
              severityScope: 1,
              userInteraction: 0.85,
            },
          },
        },
      },
    }];

  const mockError: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: GET_SEVERITY,
        variables: {
          identifier: "438679960",
        },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
    },
  ];

  it("should return a function", () => {
    expect(typeof (SeverityView))
      .toEqual("function");
  });

  it("should render a component", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocks} addTypename={false}>
          <SeverityView {...mockProps} />
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper)
      .toHaveLength(1);
    expect(wrapper.text())
      .toContain("1 | High: Exploit is not required or it can be automated");
  });

  it("should render an error in component", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mockError} addTypename={false}>
          <SeverityView {...mockProps} />
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render as editable", async () => {
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_finding__do_update_severity" },
    ]);
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocks} addTypename={false}>
          <authzContext.Provider value={mockedPermissions}>
            <SeverityView {...mockProps} />
          </authzContext.Provider>
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    const editButton: ReactWrapper = wrapper.find("button")
      .findWhere((element: ReactWrapper) => element.contains("Edit"))
      .at(0);
    expect(editButton)
      .toHaveLength(1);
    editButton.simulate("click");
    act(() => { wrapper.update(); });
    expect(wrapper.text())
      .toContain("Update");
  });

  it("should render as readonly", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocks} addTypename={false}>
          <SeverityView {...mockProps} />
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    const editButton: ReactWrapper = wrapper.find("button")
      .findWhere((element: ReactWrapper) => element.contains("Edit"))
      .at(0);
    expect(editButton)
      .toHaveLength(0);
  });
});
