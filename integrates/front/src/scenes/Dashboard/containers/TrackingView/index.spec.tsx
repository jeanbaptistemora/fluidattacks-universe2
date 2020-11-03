import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { mount, ReactWrapper } from "enzyme";
import React from "react";
import { Provider } from "react-redux";
import { MemoryRouter, Route } from "react-router";

import { TrackingView } from "scenes/Dashboard/containers/TrackingView";
import { GET_FINDING_VULN_INFO } from "scenes/Dashboard/containers/TrackingView/queries";

import store from "store/index";

describe("FindingExploitView", (): void => {

  const mocks: ReadonlyArray<MockedResponse> = [{
    request: {
      query: GET_FINDING_VULN_INFO,
      variables: { findingId: "422286126", groupName: "test" },
    },
    result: {
      data: {
        finding: {
          id: "413372600",
          newRemediated: false,
          state: "open",
          verified: true,
        },
        project: {
          subscription: "continuous",
        },
      },
    },
  }];

  it("should return a function", (): void => {
    expect(typeof (TrackingView))
      .toEqual("function");
  });

  it("should render", (): void => {
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/testorg/groups/testgroup/vulns/422286126/tracking"]}>
        <Provider store={store}>
          <MockedProvider mocks={mocks} addTypename={false}>
            <Route
              path="/orgs/:organizationName/groups/:groupName/vulns/:findingId/tracking"
              component={TrackingView}
            />
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    expect(wrapper)
      .toHaveLength(1);
  });
});
