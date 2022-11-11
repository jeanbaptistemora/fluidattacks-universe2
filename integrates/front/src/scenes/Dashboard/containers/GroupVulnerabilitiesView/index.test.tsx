/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { GET_GROUP_VULNERABILITIES } from "./queries";
import type { IGroupVulnerabilities } from "./types";

import { GroupVulnerabilitiesView } from ".";
import { getCache } from "utils/apollo";

describe("GroupVulnerabilitiesView", (): void => {
  const mockGroupVulnerabilities: IGroupVulnerabilities = {
    group: {
      name: "unittesting",
      vulnerabilities: {
        edges: [
          {
            node: {
              assigned: "",
              currentState: "open",
              currentStateCapitalized: "Open",
              externalBugTrackingSystem: null,
              finding: {
                id: "438679960",
                severityScore: 2.7,
                title: "001. Test draft title",
              },
              findingId: "438679960",
              groupName: "unittesting",
              historicTreatment: [
                {
                  acceptanceDate: "",
                  acceptanceStatus: "",
                  assigned: "assigned-user-1",
                  date: "2019-07-05 09:56:40",
                  justification: "test progress justification",
                  treatment: "IN PROGRESS",
                  user: "usertreatment@test.test",
                },
              ],
              id: "89521e9a-b1a3-4047-a16e-15d530dc1340",
              lastTreatmentDate: "2019-07-05 09:56:40",
              lastVerificationDate: null,
              organizationName: "test",
              remediated: false,
              reportDate: "2019-05-23 21:19:29",
              rootNickname: "https:",
              severity: "2.7",
              snippet: null,
              specific: "specific-1",
              stream: null,
              tag: "tag-1, tag-2",
              treatment: "",
              treatmentAcceptanceDate: "",
              treatmentAcceptanceStatus: "",
              treatmentAssigned: "assigned-user-1",
              treatmentDate: "2019-07-05 09:56:40",
              treatmentJustification: "test progress justification",
              treatmentUser: "usertreatment@test.test",
              verification: "Requested",
              vulnerabilityType: "inputs",
              where: "https://example.com/inputs",
              zeroRisk: "Requested",
            },
          },
          {
            node: {
              assigned: "",
              currentState: "closed",
              currentStateCapitalized: "Closed",
              externalBugTrackingSystem: null,
              findingId: "438679960",
              groupName: "unittesting",
              historicTreatment: [
                {
                  acceptanceDate: "",
                  acceptanceStatus: "",
                  assigned: "assigned-user-3",
                  date: "2019-07-05 09:56:40",
                  justification: "test progress justification",
                  treatment: "IN PROGRESS",
                  user: "usertreatment@test.test",
                },
              ],
              id: "a09c79fc-33fb-4abd-9f20-f3ab1f500bd0",
              lastTreatmentDate: "2019-07-05 09:56:40",
              lastVerificationDate: null,
              organizationName: "test",
              remediated: false,
              reportDate: "",
              rootNickname: "https:",
              severity: "1",
              snippet: null,
              specific: "specific-2",
              stream: null,
              tag: "tag-3, tag-4",
              treatment: "",
              treatmentAcceptanceDate: "",
              treatmentAcceptanceStatus: "",
              treatmentAssigned: "assigned-user-2",
              treatmentDate: "2019-07-05 09:56:40",
              treatmentJustification: "test progress justification",
              treatmentUser: "usertreatment@test.test",
              verification: "Verified",
              vulnerabilityType: "lines",
              where: "https://example.com/lines",
              zeroRisk: null,
            },
          },
          {
            node: {
              assigned: "",
              currentState: "open",
              currentStateCapitalized: "Open",
              externalBugTrackingSystem: null,
              findingId: "438679960",
              groupName: "unittesting",
              historicTreatment: [
                {
                  acceptanceDate: "",
                  acceptanceStatus: "",
                  assigned: "assigned-user-4",
                  date: "2019-07-05 09:56:40",
                  justification: "test progress justification",
                  treatment: "IN PROGRESS",
                  user: "usertreatment@test.test",
                },
              ],
              id: "af7a48b8-d8fc-41da-9282-d424fff563f0",
              lastTreatmentDate: "2019-07-05 09:56:40",
              lastVerificationDate: "2019-07-05 09:56:40",
              organizationName: "test",
              remediated: false,
              reportDate: "",
              rootNickname: "https:",
              severity: "1",
              snippet: null,
              specific: "specific-3",
              stream: null,
              tag: "tag-5, tag-6",
              treatment: "IN_PROGRESS",
              treatmentAcceptanceDate: "",
              treatmentAcceptanceStatus: "",
              treatmentAssigned: "assigned-user-3",
              treatmentDate: "2019-07-05 09:56:40",
              treatmentJustification: "test progress justification",
              treatmentUser: "usertreatment@test.test",
              verification: "Verified",
              vulnerabilityType: "lines",
              where: "https://example.com/lines",
              zeroRisk: null,
            },
          },
        ],
        pageInfo: {
          endCursor: "bnVsbA==",
          hasNextPage: false,
        },
        total: 3,
      },
    },
  };

  const queryMock: readonly MockedResponse[] = [
    {
      request: {
        query: GET_GROUP_VULNERABILITIES,
        variables: {
          first: 100,
          groupName: "unittesting",
          search: "",
        },
      },
      result: {
        data: mockGroupVulnerabilities,
      },
    },
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GroupVulnerabilitiesView).toBe("function");
  });

  it("should render in group vulnerabilities", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/groups/unittesting/vulns"]}>
        <MockedProvider cache={getCache()} mocks={queryMock}>
          <Route
            component={GroupVulnerabilitiesView}
            path={"/groups/:groupName/vulns"}
          />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.queryByRole("table")).toBeInTheDocument();
    });

    jest.clearAllMocks();
  });

  it("should display all group vulnerabilities columns", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/groups/unittesting/vulns"]}>
        <MockedProvider cache={getCache()} mocks={queryMock}>
          <Route
            component={GroupVulnerabilitiesView}
            path={"/groups/:groupName/vulns"}
          />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.queryByRole("table")).toBeInTheDocument();
    });

    expect(screen.getByText("Vulnerability")).toBeInTheDocument();
    expect(screen.getByText("Type")).toBeInTheDocument();
    expect(screen.getByText("Status")).toBeInTheDocument();
    expect(screen.getByText("Treatment")).toBeInTheDocument();
    expect(screen.getByText("Reattack")).toBeInTheDocument();
    expect(screen.getByText("Found")).toBeInTheDocument();
    expect(screen.getByText("Severity")).toBeInTheDocument();
    expect(screen.getByText("Evidence")).toBeInTheDocument();
    expect(
      screen.getByText("https://example.com/inputs | specific-1")
    ).toBeInTheDocument();
    expect(screen.getByText("001. test draft title")).toBeInTheDocument();
    expect(screen.getAllByText("Open")[0]).toBeInTheDocument();
    expect(screen.getByText("In progress")).toBeInTheDocument();
    expect(screen.getByText("Requested")).toBeInTheDocument();
    expect(screen.getByText("2019-05-23")).toBeInTheDocument();
    expect(screen.getByText("2.7")).toBeInTheDocument();
    expect(screen.getAllByText("View")[0]).toBeInTheDocument();

    jest.clearAllMocks();
  });

  it("should have Filter button", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/groups/unittesting/vulns"]}>
        <MockedProvider cache={getCache()} mocks={queryMock}>
          <Route
            component={GroupVulnerabilitiesView}
            path={"/groups/:groupName/vulns"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryByRole("table")).toBeInTheDocument();
    });

    expect(screen.getByRole("button", { name: "Filter" })).toBeInTheDocument();

    jest.clearAllMocks();
  });
});
