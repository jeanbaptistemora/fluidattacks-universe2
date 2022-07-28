import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import React from "react";

import { GET_ORGANIZATION_CREDENTIALS } from "./queries";

import { OrganizationCredentials } from ".";
import { authzPermissionsContext } from "utils/authz/config";

jest.mock("../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary<() => Dictionary> = jest.requireActual(
    "../../../../utils/notifications"
  );
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

describe("organization credentials view", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof OrganizationCredentials).toBe("function");
  });

  it("should list organization's credentials", async (): Promise<void> => {
    expect.hasAssertions();

    const mockQuery: MockedResponse[] = [
      {
        request: {
          query: GET_ORGANIZATION_CREDENTIALS,
          variables: {
            organizationId: "ORG#15eebe68-e9ce-4611-96f5-13d6562687e1",
          },
        },
        result: {
          data: {
            organization: {
              __typename: "Me",
              credentials: [
                {
                  __typename: "Credentials",
                  id: "6e52c11c-abf7-4ca3-b7d0-635e394f41c1",
                  name: "Credentials test",
                  owner: "owner@test.com",
                  type: "HTTPS",
                },
              ],
              name: "org-test",
            },
          },
        },
      },
    ];

    render(
      <MockedProvider addTypename={false} mocks={mockQuery}>
        <authzPermissionsContext.Provider value={new PureAbility([])}>
          <OrganizationCredentials
            organizationId={"ORG#15eebe68-e9ce-4611-96f5-13d6562687e1"}
          />
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );
    await waitFor((): void => {
      expect(screen.getByText("Credentials test")).toBeInTheDocument();
      expect(screen.getByText("HTTPS")).toBeInTheDocument();
      expect(screen.getByText("owner@test.com")).toBeInTheDocument();
    });
  });
});
