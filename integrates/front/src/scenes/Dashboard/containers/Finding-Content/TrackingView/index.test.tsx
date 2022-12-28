import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { TrackingView } from "scenes/Dashboard/containers/Finding-Content/TrackingView";
import { GET_FINDING_TRACKING } from "scenes/Dashboard/containers/Finding-Content/TrackingView/queries";

describe("TrackingView", (): void => {
  const testJustification: string = "test justification accepted treatment";
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
              assigned: null,
              cycle: 0,
              date: "2018-09-28",
              justification: null,
              safe: 0,
              vulnerable: 1,
            },
            {
              accepted: 1,
              acceptedUndefined: 0,
              assigned: "test@test.test",
              cycle: 1,
              date: "2019-01-08",
              justification: testJustification,
              safe: 0,
              vulnerable: 0,
            },
          ],
        },
      },
    },
  };

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof TrackingView).toBe("function");
  });

  it("should render", async (): Promise<void> => {
    expect.hasAssertions();

    render(
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

    await waitFor((): void => {
      expect(
        screen.queryByText(/searchFindings.tabTracking.cycle/u)
      ).toBeInTheDocument();
    });
  });
});
