import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import React from "react";
import { MemoryRouter } from "react-router-dom";

import { Dashboard } from "scenes/Dashboard";
import { GET_USER_ORGANIZATIONS } from "scenes/Dashboard/components/Navbar/Breadcrumb/queries";
import { GET_USER } from "scenes/Dashboard/queries";
import type { IUser } from "scenes/Dashboard/types";

describe("Dashboard", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Dashboard).toBe("function");
  });

  it("should render dashboard component", async (): Promise<void> => {
    expect.hasAssertions();

    const permissionsResult: IUser = {
      me: {
        isConcurrentSession: false,
        permissions: ["dummyPermission", "dummyPermissionBrother"],
        phone: null,
        remember: false,
        sessionExpiration: "2021-01-20 21:37:37.944176",
        tours: {
          newGroup: true,
          newRoot: true,
        },
        userEmail: "",
        userName: "",
      },
    };
    const mocks: readonly MockedResponse[] = [
      {
        request: {
          query: GET_USER,
          variables: {
            groupName: "TEST",
          },
        },
        result: {
          data: permissionsResult,
        },
      },
      {
        request: {
          query: GET_USER_ORGANIZATIONS,
        },
        result: {
          data: {
            me: {
              __typename: "Me",
              organizations: [
                {
                  __typename: "Organization",
                  name: "okada",
                },
              ],
              userEmail: "test@fluidattacks.com",
            },
          },
        },
      },
      {
        request: {
          query: GET_USER_ORGANIZATIONS,
        },
        result: {
          data: {
            me: {
              __typename: "Me",
              organizations: [
                {
                  __typename: "Organization",
                  name: "okada",
                },
              ],
              userEmail: "test@fluidattacks.com",
            },
          },
        },
      },
    ];
    const { container } = render(
      <MemoryRouter initialEntries={["/orgs/okada"]}>
        <MockedProvider mocks={mocks}>
          <Dashboard />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(container.querySelector("#navbar")).toBeInTheDocument();
    });

    expect(container.querySelector("#scroll-up")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "App logo" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "App logo" })).toHaveAttribute(
      "href",
      "/home"
    );
  });
});
