import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import React from "react";

import { OrganizationOverview } from ".";
import { GET_ORGANIZATION_BILLING } from "../queries";

describe("OrganizationOverview", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof OrganizationOverview).toBe("function");
  });

  it("should display the organization billing overview", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedQueries: MockedResponse[] = [
      {
        request: {
          query: GET_ORGANIZATION_BILLING,
          variables: {
            organizationId: "ORG#15eebe68-e9ce-4611-96f5-13d6562687e1",
          },
        },
        result: {
          data: {
            organization: {
              __typename: "Organization",
              billing: {
                costsTotal: 1,
                numberAuthorsMachine: 1,
                numberAuthorsSquad: 1,
                numberGroupsMachine: 1,
                numberGroupsSquad: 1,
                organizationName: "org-test",
              },
              name: "org-test",
            },
          },
        },
      },
    ];

    render(
      <MockedProvider addTypename={false} mocks={mockedQueries}>
        <OrganizationOverview
          costsTotal={1}
          numberAuthorsMachine={1}
          numberAuthorsSquad={1}
          numberGroupsMachine={1}
          numberGroupsSquad={1}
          organizationName={"org-test"}
        />
      </MockedProvider>
    );
    await waitFor((): void => {
      expect(
        screen.getByText("organization.tabs.billing.overview.title.text")
      ).toBeInTheDocument();

      expect(
        screen.getByText("organization.tabs.billing.overview.costsTotal.title")
      ).toBeInTheDocument();
      expect(
        screen.getByText(
          "organization.tabs.billing.overview.numberAuthorsMachine.title"
        )
      ).toBeInTheDocument();
      expect(
        screen.getByText(
          "organization.tabs.billing.overview.numberAuthorsSquad.title"
        )
      ).toBeInTheDocument();

      expect(
        screen.getByText(
          "organization.tabs.billing.overview.numberGroupsMachine.title"
        )
      ).toBeInTheDocument();
      expect(
        screen.getByText(
          "organization.tabs.billing.overview.numberGroupsSquad.title"
        )
      ).toBeInTheDocument();
    });
  });
});
