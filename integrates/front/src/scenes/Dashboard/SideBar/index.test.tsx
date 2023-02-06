import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import React from "react";
import { MemoryRouter } from "react-router-dom";

import { DashboardSideBar } from ".";
import { Dashboard } from "scenes/Dashboard";
import { GET_USER_ORGANIZATIONS } from "scenes/Dashboard/components/Navbar/Breadcrumb/queries";
import { GET_USER } from "scenes/Dashboard/queries";
import type { IUser } from "scenes/Dashboard/types";
import { featurePreviewContext } from "utils/featurePreview";

describe("Dashboard", (): void => {
  const permissionsResult: IUser = {
    me: {
      isConcurrentSession: false,
      permissions: ["dummyPermission", "dummyPermissionBrother"],
      phone: null,
      remember: false,
      sessionExpiration: "2021-01-20 21:37:37.944176",
      tours: {
        newGroup: true,
        newRiskExposure: true,
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

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof DashboardSideBar).toBe("function");
  });

  it("should render sidebar component", async (): Promise<void> => {
    expect.hasAssertions();

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

    expect(screen.getByRole("link", { name: "App logo" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "App logo" })).toHaveAttribute(
      "href",
      "/home"
    );
  });

  it("should render sidebar fp component", async (): Promise<void> => {
    expect.hasAssertions();

    const { container } = render(
      <featurePreviewContext.Provider value={{ featurePreview: true }}>
        <MemoryRouter initialEntries={["/orgs/okada"]}>
          <MockedProvider mocks={mocks}>
            <Dashboard />
          </MockedProvider>
        </MemoryRouter>
      </featurePreviewContext.Provider>
    );

    await waitFor((): void => {
      expect(container.querySelector("#navbar")).toBeInTheDocument();
    });

    const appLogo = screen.getAllByRole("link");

    expect(appLogo[1]).toBeInTheDocument();
    expect(appLogo[1]).toHaveAttribute("href", "/home");
    expect(appLogo[2]).toHaveAttribute("href", "/orgs/okada/groups");
    expect(appLogo[3]).toHaveAttribute("href", "/orgs/okada/analytics");
    expect(appLogo[4]).toHaveAttribute("href", "/orgs/okada/policies");
    expect(appLogo[5]).toHaveAttribute("href", "/orgs/okada/stakeholders");
    expect(appLogo[6]).toHaveAttribute("href", "/orgs/okada/portfolios");
    expect(appLogo[7]).toHaveAttribute("href", "/orgs/okada/outofscope");
    expect(appLogo[8]).toHaveAttribute("href", "/orgs/okada/credentials");
    expect(appLogo[9]).toHaveAttribute("href", "/orgs/okada/compliance");
  });
});
