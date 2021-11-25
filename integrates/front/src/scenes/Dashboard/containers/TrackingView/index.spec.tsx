import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { act } from "react-dom/test-utils";
import { MemoryRouter, Route } from "react-router-dom";
import wait from "waait";

import { TrackingView } from "scenes/Dashboard/containers/TrackingView";
import { GET_FINDING_TRACKING } from "scenes/Dashboard/containers/TrackingView/queries";

describe("TrackingView", (): void => {
  const mocks: MockedResponse = {
    request: {
      query: GET_FINDING_TRACKING,
      variables: { findingId: "422286126" },
    },
    result: {
      data: {
        finding: {
          id: "422286126",
          tracking: [
            {
              accepted: 0,
              acceptedUndefined: 0,
              closed: 0,
              cycle: 0,
              date: "2018-09-28",
              open: 1,
            },
            {
              accepted: 1,
              acceptedUndefined: 0,
              closed: 0,
              cycle: 1,
              date: "2019-01-08",
              justification: "test justification accepted treatment",
              manager: "test@test.test",
              open: 0,
            },
          ],
        },
      },
    },
  };

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof TrackingView).toStrictEqual("function");
  });

  it("should render", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter
        initialEntries={["/orgs/aorg/groups/agroup/vulns/422286126/tracking"]}
      >
        <MockedProvider addTypename={false} mocks={[mocks]}>
          <Route
            component={TrackingView}
            path={
              "/orgs/:organizationName/groups/:groupName/vulns/:findingId/tracking"
            }
          />
        </MockedProvider>
      </MemoryRouter>
    );

    expect(wrapper).toHaveLength(1);
  });

  it("should render timeline", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter
        initialEntries={["/orgs/aorg/groups/agroup/vulns/422286126/tracking"]}
      >
        <MockedProvider addTypename={false} mocks={[mocks]}>
          <Route
            component={TrackingView}
            path={
              "/orgs/:organizationName/groups/:groupName/vulns/:findingId/tracking"
            }
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    const numberOfCycles: number = 2;

    expect(wrapper.find("li").last().text()).not.toContain("Justification");
    expect(wrapper.find("li").first().text()).toContain("Justification");
    expect(wrapper.find("li")).toHaveLength(numberOfCycles);
  });
});
