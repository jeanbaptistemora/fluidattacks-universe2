import { configure, mount, ReactWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import { GraphQLError } from "graphql";
// tslint:disable-next-line: no-import-side-effect
import "isomorphic-fetch";
import * as React from "react";
// tslint:disable-next-line: no-submodule-imports
import { MockedProvider, MockedResponse } from "react-apollo/test-utils";
import { Provider } from "react-redux";
import wait from "waait";
import store from "../../../../store/index";
import { GET_VULNERABILITIES } from "../../components/Vulnerabilities/queries";
import {
  closing,
  trackingViewComponent as TrackingView,
} from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("Tracking view", () => {

  const mocks: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: GET_VULNERABILITIES,
        variables: {
          identifier: "438679960",
        },
      },
      result: {
        data: {
          finding: {
            __typename: "Finding",
            id: "438679960",
            inputsVulns: [{
              __typename: "Vulnerability",
              currentApprovalStatus: "",
              currentState: "open",
              externalBts: "",
              findingId: "438679960",
              id: "89521e9a-b1a3-4047-a16e-15d530dc1340",
              specific: "email",
              treatment: "New",
              treatmentJustification: "",
              treatmentManager: "user@test.com",
              vulnType: "inputs",
              where: "https://example.com/contact",
            }],
            linesVulns: [],
            pendingVulns: [],
            portsVulns: [],
            releaseDate: "2019-03-12 00:00:00",
            success: true,
          },
        },
      },
    },
  ];

  const mockError: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: GET_VULNERABILITIES,
        variables: {
          identifier: "438679960",
        },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
    },
  ];

  const testClosings: closing[] = [{
    closed: 0,
    cycle: 0,
    date: "2018-10-10",
    effectiveness: 0,
    open: 4,
  }];

  it("should return a function", () => {
    expect(typeof (TrackingView))
      .toEqual("function");
  });

  it("should render a component", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocks} addTypename={true}>
          <TrackingView
            closings={testClosings}
            findingId="438679960"
            userRole="admin"
          />
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
          <TrackingView
            closings={testClosings}
            findingId="438679960"
            userRole="admin"
          />
        </MockedProvider>
      </Provider>,
    );
    await wait(0);
    expect(wrapper)
      .toHaveLength(1);
  });
});
