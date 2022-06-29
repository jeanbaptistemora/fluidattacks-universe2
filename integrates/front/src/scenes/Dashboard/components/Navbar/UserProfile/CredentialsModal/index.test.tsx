import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import React from "react";

import {
  GET_STAKEHOLDER_CREDENTIALS,
  GET_STAKEHOLDER_ORGANIZATIONS,
} from "./queries";

import { CredentialsModal } from ".";
import { authzPermissionsContext } from "utils/authz/config";

jest.mock("../../../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary<() => Dictionary> = jest.requireActual(
    "../../../../../../utils/notifications"
  );
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

describe("credentials modal", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof CredentialsModal).toBe("function");
  });

  it("should list stakeholder's credentials", async (): Promise<void> => {
    expect.hasAssertions();

    const handleOnClose: jest.Mock = jest.fn();

    const mockQuery: MockedResponse[] = [
      {
        request: {
          query: GET_STAKEHOLDER_CREDENTIALS,
        },
        result: {
          data: {
            me: {
              __typename: "Me",
              credentials: [
                {
                  __typename: "Credentials",
                  id: "6e52c11c-abf7-4ca3-b7d0-635e394f41c1",
                  name: "Credentials test",
                  organization: {
                    __typename: "Organization",
                    id: "c966d57a-adde-43c3-bd47-1770002aa122",
                    name: "Organization name",
                  },
                  type: "HTTPS",
                },
              ],
              userEmail: "test@fluidattacks.com",
            },
          },
        },
      },
      {
        request: {
          query: GET_STAKEHOLDER_ORGANIZATIONS,
        },
        result: {
          data: {
            me: {
              __typename: "Me",
              organizations: [
                {
                  __typename: "Organization",
                  id: "c966d57a-adde-43c3-bd47-1770002aa122",
                  name: "Organization name",
                },
              ],
              userEmail: "test@fluidattacks.com",
            },
          },
        },
      },
    ];

    render(
      <MockedProvider addTypename={false} mocks={mockQuery}>
        <authzPermissionsContext.Provider value={new PureAbility([])}>
          <CredentialsModal onClose={handleOnClose} />
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );
    await waitFor((): void => {
      expect(screen.getByText("Credentials test")).toBeInTheDocument();
      expect(screen.getByText("Organization name")).toBeInTheDocument();
    });
  });
});
