import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { TrackingView } from "scenes/Dashboard/containers/TrackingView";
import { GET_FINDING_TRACKING } from "scenes/Dashboard/containers/TrackingView/queries";

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
              closed: 0,
              cycle: 0,
              date: "2018-09-28",
              justification: null,
              open: 1,
            },
            {
              accepted: 1,
              acceptedUndefined: 0,
              assigned: "test@test.test",
              closed: 0,
              cycle: 1,
              date: "2019-01-08",
              justification: testJustification,
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

  it("should render timeline", async (): Promise<void> => {
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
    const numberOfCycles: number = 2;

    expect(screen.getAllByRole("listitem")).toHaveLength(numberOfCycles);
    expect(screen.getAllByRole("listitem")[0].textContent).toContain(
      testJustification
    );
    expect(screen.getAllByRole("listitem")[1].textContent).not.toContain(
      testJustification
    );
  });
});
