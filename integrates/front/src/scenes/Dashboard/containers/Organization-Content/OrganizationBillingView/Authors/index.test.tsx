import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import { set } from "mockdate";
import React from "react";

import { OrganizationAuthors } from ".";
import { GET_ORGANIZATION_AUTHORS_BILLING } from "../queries";

describe("OrganizationOverview", (): void => {
  const TEST_DATE = 2020;
  const date: Date = new Date(TEST_DATE, 0);
  set(date);

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof OrganizationAuthors).toBe("function");
  });

  it("should display the organization billing overview", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedQueries: MockedResponse[] = [
      {
        request: {
          query: GET_ORGANIZATION_AUTHORS_BILLING,
          variables: {
            date: date.toISOString(),
            organizationId: "ORG#15eebe68-e9ce-4611-96f5-13d6562687e1",
          },
        },
        result: {
          data: {
            organization: {
              __typename: "Organization",
              billing: {
                authors: [
                  {
                    activeGroups: [
                      {
                        name: "continuoustesting",
                        tier: "SQUAD",
                      },
                      {
                        name: "unittesting",
                        tier: "SQUAD",
                      },
                    ],
                    actor: "Dev 1 <dev1@fluidattacks.com>",
                  },
                  {
                    activeGroups: [
                      {
                        name: "unittesting",
                        tier: "SQUAD",
                      },
                    ],
                    actor: "Dev 2 <dev2@fluidattacks.com>",
                  },
                ],
              },
            },
          },
        },
      },
    ];

    render(
      <MockedProvider addTypename={false} mocks={mockedQueries}>
        <OrganizationAuthors
          organizationId={"ORG#15eebe68-e9ce-4611-96f5-13d6562687e1"}
        />
      </MockedProvider>
    );
    await waitFor((): void => {
      expect(
        screen.getByText("organization.tabs.billing.authors.title")
      ).toBeInTheDocument();

      expect(
        screen.getByText(
          "organization.tabs.billing.authors.headers.authorEmail"
        )
      ).toBeInTheDocument();
      expect(
        screen.getByText("organization.tabs.billing.authors.headers.authorName")
      ).toBeInTheDocument();
      expect(
        screen.getByText(
          "organization.tabs.billing.authors.headers.activeGroups"
        )
      ).toBeInTheDocument();

      expect(screen.getByText("Dev 1")).toBeInTheDocument();
      expect(
        screen.getByText("continuoustesting, unittesting")
      ).toBeInTheDocument();

      expect(screen.getByText("Dev 2")).toBeInTheDocument();
      expect(screen.getByText("unittesting")).toBeInTheDocument();
    });
  });
});
