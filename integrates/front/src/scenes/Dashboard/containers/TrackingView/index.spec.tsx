import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { mount, ReactWrapper } from "enzyme";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { MemoryRouter, Route } from "react-router";
import wait from "waait";

import { TrackingView } from "scenes/Dashboard/containers/TrackingView";
import { GET_FINDING_TRACKING } from "scenes/Dashboard/containers/TrackingView/queries";

import store from "store/index";

describe("FindingExploitView", (): void => {

  const mocks: ReadonlyArray<MockedResponse> = [{
    request: {
      query: GET_FINDING_TRACKING,
      variables: { findingId: "422286126" },
    },
    result: {
      data: {
        finding: {
          id: "422286126",
          tracking: [
            { closed: 0, cycle: 0, date: "2018-09-28", effectiveness: 0, open: 1 },
            { closed: 1, cycle: 1, date: "2019-01-08", effectiveness: 100, open: 0 },
          ],
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

  it("should render timeline", async () => {
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/okada/groups/testgroup/vulns/422286126/tracking"]}>
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
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper.find("ul"))
      .toHaveLength(1);
    expect(wrapper.find("li"))
      .toHaveLength(2);
  });
});
