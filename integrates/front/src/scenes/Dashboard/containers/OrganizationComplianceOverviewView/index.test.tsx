import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import React from "react";

import { GET_ORGANIZATION_COMPLIANCE } from "./queries";

import { OrganizationComplianceOverviewView } from ".";

describe("OrganizationComplianceOverviewView", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof OrganizationComplianceOverviewView).toBe("function");
  });

  it("should display the organization compliance indicators", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedQueries: MockedResponse[] = [
      {
        request: {
          query: GET_ORGANIZATION_COMPLIANCE,
          variables: {
            organizationId: "ORG#15eebe68-e9ce-4611-96f5-13d6562687e1",
          },
        },
        result: {
          data: {
            organization: {
              __typename: "Organization",
              compliance: {
                complianceLevel: 0.3,
                complianceWeeklyTrend: -0.02,
                estimatedDaysToFullCompliance: 10,
                standards: [
                  {
                    avgOrganizationComplianceLevel: 0.5,
                    bestOrganizationComplianceLevel: 0.99,
                    complianceLevel: 0.75,
                    standardTitle: "standardname1",
                    worstOrganizationComplianceLevel: 0.2,
                  },
                  {
                    avgOrganizationComplianceLevel: 0.6,
                    bestOrganizationComplianceLevel: 0.8,
                    complianceLevel: 0.88,
                    standardTitle: "standardname2",
                    worstOrganizationComplianceLevel: 0.0,
                  },
                ],
              },
              name: "org-test",
            },
          },
        },
      },
    ];

    render(
      <MockedProvider addTypename={false} mocks={mockedQueries}>
        <OrganizationComplianceOverviewView
          organizationId={"ORG#15eebe68-e9ce-4611-96f5-13d6562687e1"}
        />
      </MockedProvider>
    );
    await waitFor((): void => {
      expect(
        screen.getByText(
          "organization.tabs.compliance.tabs.overview.organizationCompliance.complianceLevel.title"
        )
      ).toBeInTheDocument();
      expect(screen.getByText("30%")).toBeInTheDocument();
      expect(
        screen.getByText(
          "organization.tabs.compliance.tabs.overview.organizationCompliance.complianceWeeklyTrend.title"
        )
      ).toBeInTheDocument();
      expect(screen.getByText("-0.02")).toBeInTheDocument();
      expect(
        screen.getByText(
          "organization.tabs.compliance.tabs.overview.organizationCompliance.etToFullCompliance.title"
        )
      ).toBeInTheDocument();
      expect(
        screen.getByText(
          "10 organization.tabs.compliance.tabs.overview.cards.days"
        )
      ).toBeInTheDocument();
      expect(
        screen.getByText(
          "organization.tabs.compliance.tabs.overview.standardWithLowestCompliance.complianceLevelOfStandard.title"
        )
      ).toBeInTheDocument();
      expect(screen.getAllByText("STANDARDNAME1")[0]).toBeInTheDocument();
      expect(screen.getAllByText("75%")[0]).toBeInTheDocument();
      expect(screen.getAllByText("STANDARDNAME1")[1]).toBeInTheDocument();
      expect(screen.getAllByText("75%")[1]).toBeInTheDocument();
      expect(screen.getByText("99%")).toBeInTheDocument();
      expect(screen.getByText("50%")).toBeInTheDocument();
      expect(screen.getByText("20%")).toBeInTheDocument();
      expect(screen.getByText("STANDARDNAME2")).toBeInTheDocument();
      expect(screen.getByText("88%")).toBeInTheDocument();
      expect(screen.getByText("80%")).toBeInTheDocument();
      expect(screen.getByText("60%")).toBeInTheDocument();
      expect(screen.getByText("0%")).toBeInTheDocument();
    });
  });
});
