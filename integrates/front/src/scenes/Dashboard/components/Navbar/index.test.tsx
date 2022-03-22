import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import React from "react";
import { MemoryRouter } from "react-router-dom";

import { Navbar } from "scenes/Dashboard/components/Navbar";
import {
  GET_FINDING_TITLE,
  GET_USER_ORGANIZATIONS,
} from "scenes/Dashboard/components/Navbar/Breadcrumb/queries";
import { GET_VULNS_GROUPS } from "scenes/Dashboard/queries";
import { authContext } from "utils/auth";
import { authzPermissionsContext } from "utils/authz/config";

describe("Navbar", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Navbar).toStrictEqual("function");
  });

  it("should render", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "front_can_use_groups_searchbar" },
    ]);
    const organizationsQuery: Readonly<MockedResponse> = {
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
    };
    const mocksQueryGroupVulns: MockedResponse = {
      request: {
        query: GET_VULNS_GROUPS,
        variables: {
          groupName: "testgroup",
        },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            name: "testgroup",
            vulnerabilitiesAssigned: [
              {
                __typename: "Vulnerability",
                currentState: "open",
                externalBugTrackingSystem: null,
                findingId: "422286126",
                id: "89521e9a-b1a3-4047-a16e-15d530dc1340",
                lastTreatmentDate: "2019-07-05 09:56:40",
                lastVerificationDate: null,
                remediated: true,
                reportDate: "2019-07-05 09:56:40",
                severity: "",
                specific: "specific-1",
                stream: "home > blog > articulo",
                tag: "tag-1, tag-2",
                treatment: "IN_PROGRESS",
                treatmentAcceptanceDate: "",
                treatmentAcceptanceStatus: "",
                treatmentAssigned: "assigned-user-1",
                treatmentDate: "2019-07-05 09:56:40",
                treatmentJustification: "test progress justification",
                verification: "Requested",
                vulnerabilityType: "inputs",
                where: "https://example.com/inputs",
                zeroRisk: null,
              },
            ],
          },
        },
      },
    };

    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <MemoryRouter initialEntries={["/orgs/okada"]}>
          <MockedProvider
            addTypename={true}
            mocks={[organizationsQuery, mocksQueryGroupVulns]}
          >
            <authContext.Provider
              value={{ userEmail: "test@fluidattacks.com", userName: "" }}
            >
              <Navbar
                meVulnerabilitiesAssigned={{
                  me: {
                    userEmail: "",
                    vulnerabilitiesAssigned: [],
                  },
                }}
                userData={{
                  me: {
                    organizations: [
                      {
                        groups: [
                          {
                            name: "testgroup",
                            permissions: ["valid_assigned"],
                            serviceAttributes: [],
                          },
                        ],
                        name: "okada",
                      },
                    ],
                    userEmail: "",
                  },
                }}
                userRole={"user"}
              />
            </authContext.Provider>
          </MockedProvider>
        </MemoryRouter>
      </authzPermissionsContext.Provider>
    );

    await waitFor((): void => {
      expect(
        screen.getByPlaceholderText("navbar.searchPlaceholder")
      ).toBeInTheDocument();
    });

    expect(screen.getAllByRole("button")[0].textContent).toBe("okada");
  });

  it("should display draft title", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "front_can_use_groups_searchbar" },
    ]);
    const organizationsQuery: Readonly<MockedResponse> = {
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
    };
    const findingTitleQuery: Readonly<MockedResponse> = {
      request: {
        query: GET_FINDING_TITLE,
        variables: {
          findingId: "F3F42d73-c1bf-47c5-954e-FFFFFFFFFFFF",
        },
      },
      result: {
        data: {
          finding: {
            title: "001. Test draft title",
          },
        },
      },
    };

    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <MemoryRouter
          initialEntries={[
            "/orgs/okada/groups/unittesting/drafts/F3F42d73-c1bf-47c5-954e-FFFFFFFFFFFF/locations",
          ]}
        >
          <MockedProvider
            addTypename={true}
            mocks={[findingTitleQuery, organizationsQuery]}
          >
            <authContext.Provider
              value={{ userEmail: "test@fluidattacks.com", userName: "" }}
            >
              <Navbar
                meVulnerabilitiesAssigned={undefined}
                userData={undefined}
                userRole={"user"}
              />
            </authContext.Provider>
          </MockedProvider>
        </MemoryRouter>
      </authzPermissionsContext.Provider>
    );

    await waitFor((): void => {
      expect(screen.getByText("001. Test draft title")).toHaveAttribute(
        "href",
        "/orgs/okada/groups/unittesting/drafts/F3F42d73-c1bf-47c5-954e-FFFFFFFFFFFF"
      );
    });
  });

  it("should display finding title", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "front_can_use_groups_searchbar" },
    ]);
    const organizationsQuery: Readonly<MockedResponse> = {
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
    };
    const findingTitleQuery: Readonly<MockedResponse> = {
      request: {
        query: GET_FINDING_TITLE,
        variables: {
          findingId: "436992569",
        },
      },
      result: {
        data: {
          finding: {
            title: "001. Test finding title",
          },
        },
      },
    };
    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <MemoryRouter
          initialEntries={[
            "/orgs/okada/groups/unittesting/vulns/436992569/description",
          ]}
        >
          <MockedProvider
            addTypename={true}
            mocks={[findingTitleQuery, organizationsQuery]}
          >
            <authContext.Provider
              value={{ userEmail: "test@fluidattacks.com", userName: "" }}
            >
              <Navbar
                meVulnerabilitiesAssigned={undefined}
                userData={undefined}
                userRole={"user"}
              />
            </authContext.Provider>
          </MockedProvider>
        </MemoryRouter>
      </authzPermissionsContext.Provider>
    );

    await waitFor((): void => {
      expect(screen.getByText("001. Test finding title")).toHaveAttribute(
        "href",
        "/orgs/okada/groups/unittesting/vulns/436992569"
      );
    });
  });
});
