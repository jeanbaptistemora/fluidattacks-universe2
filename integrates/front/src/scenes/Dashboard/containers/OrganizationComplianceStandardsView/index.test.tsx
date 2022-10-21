/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import React from "react";

import {
  GET_GROUP_UNFULFILLED_STANDARDS,
  GET_ORGANIZATION_GROUP_NAME,
} from "./queries";

import { OrganizationComplianceStandardsView } from ".";

describe("OrganizationComplianceStandardsView", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof OrganizationComplianceStandardsView).toBe("function");
  });

  it("should display the unfulfilled standards", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedQueries: MockedResponse[] = [
      {
        request: {
          query: GET_ORGANIZATION_GROUP_NAME,
          variables: {
            organizationId: "ORG#15eebe68-e9ce-4611-96f5-13d6562687e1",
          },
        },
        result: {
          data: {
            organization: {
              __typename: "Organization",
              groups: [
                {
                  name: "group1",
                },
                {
                  name: "group2",
                },
              ],
              name: "org-test",
            },
          },
        },
      },
      {
        request: {
          query: GET_GROUP_UNFULFILLED_STANDARDS,
          variables: {
            groupName: "group1",
          },
        },
        result: {
          data: {
            group: {
              __typename: "Group",
              compliance: {
                unfulfilledStandards: [
                  {
                    title: "standardname1",
                    unfulfilledRequirements: [
                      {
                        id: "001",
                        title: "requirement1",
                      },
                      {
                        id: "002",
                        title: "requirement2",
                      },
                    ],
                  },
                  {
                    title: "standardname2",
                    unfulfilledRequirements: [
                      {
                        id: "001",
                        title: "requirement1",
                      },
                      {
                        id: "003",
                        title: "requirement3",
                      },
                    ],
                  },
                ],
              },
              name: "group1",
            },
          },
        },
      },
    ];

    render(
      <MockedProvider addTypename={false} mocks={mockedQueries}>
        <OrganizationComplianceStandardsView
          organizationId={"ORG#15eebe68-e9ce-4611-96f5-13d6562687e1"}
        />
      </MockedProvider>
    );
    await waitFor((): void => {
      expect(
        screen.getByText(
          "organization.tabs.compliance.tabs.standards.unfulfilledStandards.title (2)"
        )
      ).toBeInTheDocument();
      expect(screen.getByText("Group 1")).toBeInTheDocument();
      expect(screen.getByText("STANDARDNAME1")).toBeInTheDocument();
      expect(screen.getAllByText("001 requirement1")[0]).toBeInTheDocument();
      expect(screen.getByText("002 requirement2")).toBeInTheDocument();
      expect(screen.getByText("STANDARDNAME2")).toBeInTheDocument();
      expect(screen.getAllByText("001 requirement1")[1]).toBeInTheDocument();
      expect(screen.getByText("003 requirement3")).toBeInTheDocument();
    });
  });
});
