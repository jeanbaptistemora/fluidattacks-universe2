import { configure, mount, ReactWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import { GraphQLError } from "graphql";
// tslint:disable-next-line: no-import-side-effect
import "isomorphic-fetch";
import * as React from "react";
// tslint:disable-next-line: no-submodule-imports
import { MockedProvider, MockedResponse } from "react-apollo/test-utils";
import { Provider } from "react-redux";
import { RouteComponentProps } from "react-router";
import wait from "waait";
import store from "../../../../store/index";
import { SeverityView } from "./index";
import { GET_SEVERITY } from "./queries";

configure({ adapter: new ReactSixteenAdapter() });

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
            __typename: "Finding",
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
        <MockedProvider mocks={mocks} addTypename={true}>
          <SeverityView {...mockProps} />
        </MockedProvider>
      </Provider>,
    );
    await wait(0);
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render an error in component", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mockError} addTypename={true}>
          <SeverityView {...mockProps} />
        </MockedProvider>
      </Provider>,
    );
    await wait(0);
    expect(wrapper)
      .toHaveLength(1);
  });

});
