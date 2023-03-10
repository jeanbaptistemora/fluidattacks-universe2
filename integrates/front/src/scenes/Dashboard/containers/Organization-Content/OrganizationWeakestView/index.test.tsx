import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { GET_ORGANIZATION_CREDENTIALS } from "scenes/Dashboard/containers/Organization-Content/OrganizationCredentialsView/queries";
import { OrganizationWeakest } from "scenes/Dashboard/containers/Organization-Content/OrganizationWeakestView/index";
import {
  GET_ORGANIZATION_GROUPS,
  GET_ORGANIZATION_INTEGRATION_REPOSITORIES,
} from "scenes/Dashboard/containers/Organization-Content/OrganizationWeakestView/queries";
import { authzGroupContext, authzPermissionsContext } from "utils/authz/config";

const mockHistoryPush: jest.Mock = jest.fn();
jest.mock("react-router-dom", (): Record<string, unknown> => {
  const mockedRouter: Record<string, () => Record<string, unknown>> =
    jest.requireActual("react-router-dom");

  return {
    ...mockedRouter,
    useHistory: (): Record<string, unknown> => ({
      ...mockedRouter.useHistory(),
      push: mockHistoryPush,
    }),
  };
});

describe("OrganizationWeakestView", (): void => {
  const mocksOrgRepositories: MockedResponse = {
    request: {
      query: GET_ORGANIZATION_INTEGRATION_REPOSITORIES,
      variables: {
        first: 150,
        organizationId: "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
      },
    },
    result: {
      data: {
        organization: {
          __typename: "Organization",
          integrationRepositoriesConnection: {
            __typename: "IntegrationRepositoriesConnection",
            edges: [
              {
                __typename: "IntegrationRepositoriesEdge",
                node: {
                  __typename: "OrganizationIntegrationRepositories",
                  defaultBranch: "main",
                  lastCommitDate: "2022-11-09 02:34:40+00:00",
                  url: "https://testrepo.com/testorg1/testproject1/_git/testrepo",
                },
              },
              {
                __typename: "IntegrationRepositoriesEdge",
                node: {
                  __typename: "OrganizationIntegrationRepositories",
                  defaultBranch: "main",
                  lastCommitDate: "2022-10-19 02:34:40+00:00",
                  url: "https://testrepo.com/testorg1/testproject1/_git/testsecondrepo",
                },
              },
            ],
            pageInfo: {
              endCursor: "bnVsbA==",
              hasNextPage: false,
            },
          },
          name: "orgtest",
        },
      },
    },
  };

  const mocksOrganizationGroups: MockedResponse = {
    request: {
      query: GET_ORGANIZATION_GROUPS,
      variables: {
        organizationId: "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
      },
    },
    result: {
      data: {
        organization: {
          __typename: "Organization",
          groups: [
            {
              __typename: "Group",
              name: "group1",
              permissions: [
                "api_mutations_add_git_root_mutate",
                "api_mutations_update_git_root_mutate",
              ],
              serviceAttributes: ["has_service_white"],
            },
            {
              __typename: "Group",
              name: "group2",
              permissions: ["api_mutations_add_git_root_mutate"],
              serviceAttributes: ["has_service_black"],
            },
          ],
          name: "orgtest",
          permissions: ["api_mutations_add_credentials_mutate"],
        },
      },
    },
  };

  const mockedOrgCredentials: MockedResponse = {
    request: {
      query: GET_ORGANIZATION_CREDENTIALS,
      variables: {
        organizationId: "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
      },
    },
    result: {
      data: {
        organization: {
          __typename: "Organization",
          credentials: [
            {
              __typename: "Credentials",
              azureOrganization: "testorg1",
              id: "6e52c11c-abf7-4ca3-b7d0-635e394f41c1",
              isPat: true,
              isToken: true,
              name: "Credentials test",
              owner: "owner@test.com",
              type: "HTTPS",
            },
          ],
          name: "orgtest",
        },
      },
    },
  };

  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof OrganizationWeakest).toBe("function");
  });

  it("should handle select group to add", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const { container } = render(
      <MemoryRouter initialEntries={["/orgs/orgtest/outside"]}>
        <MockedProvider
          addTypename={true}
          mocks={[
            mockedOrgCredentials,
            mocksOrganizationGroups,
            mocksOrgRepositories,
          ]}
        >
          <authzPermissionsContext.Provider value={new PureAbility<string>([])}>
            <authzGroupContext.Provider value={new PureAbility<string>([])}>
              <Route path={"/orgs/:organizationName/outside"}>
                <OrganizationWeakest
                  organizationId={"ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"}
                />
              </Route>
            </authzGroupContext.Provider>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(
        screen.queryByRole("cell", {
          name: "https://testrepo.com/testorg1/testproject1/_git/testrepo",
        })
      ).toBeInTheDocument();
    });

    expect(container.querySelector(".fa-plus")).toBeInTheDocument();
    expect(
      screen.queryByRole("combobox", { name: "groupName" })
    ).not.toBeInTheDocument();

    fireEvent.click(screen.getAllByRole("button")[1]);

    await waitFor((): void => {
      expect(screen.getByRole("combobox")).toBeInTheDocument();
    });

    expect(
      screen.queryByText("group.scope.common.add")
    ).not.toBeInTheDocument();

    expect(
      screen.queryByRole("option", {
        name: "group1",
      })
    ).toBeInTheDocument();
    expect(
      screen.queryByRole("option", {
        name: "group2",
      })
    ).not.toBeInTheDocument();

    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "groupName" }),
      ["group1"]
    );
    await userEvent.click(screen.getByText("components.modal.confirm"));
    await waitFor((): void => {
      expect(screen.getByRole("textbox", { name: "url" })).toHaveValue(
        "https://testrepo.com/testorg1/testproject1/_git/testrepo"
      );
    });

    expect(screen.getByRole("textbox", { name: "branch" })).toHaveValue("main");
    expect(screen.getAllByRole("textbox")).toHaveLength(5);
    expect(screen.getAllByRole("button")).toHaveLength(7);
    expect(
      screen.getByRole("combobox", { name: "credentials.typeCredential" })
    ).not.toBeDisabled();
  });

  it("should handle select group to add many", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    render(
      <MemoryRouter initialEntries={["/orgs/orgtest/outside"]}>
        <MockedProvider
          addTypename={true}
          mocks={[
            mockedOrgCredentials,
            mocksOrganizationGroups,
            mocksOrgRepositories,
          ]}
        >
          <authzPermissionsContext.Provider value={new PureAbility<string>([])}>
            <authzGroupContext.Provider value={new PureAbility<string>([])}>
              <Route path={"/orgs/:organizationName/outside"}>
                <OrganizationWeakest
                  organizationId={"ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"}
                />
              </Route>
            </authzGroupContext.Provider>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(
        screen.queryByRole("cell", {
          name: "https://testrepo.com/testorg1/testproject1/_git/testrepo",
        })
      ).toBeInTheDocument();
    });

    expect(
      screen.queryByRole("combobox", { name: "groupName" })
    ).not.toBeInTheDocument();
    expect(screen.getAllByRole("button")[0]).toBeDisabled();

    await userEvent.click(screen.getAllByRole("checkbox")[0]);

    await waitFor((): void => {
      expect(screen.getAllByRole("button")[0]).not.toBeDisabled();
    });

    await userEvent.click(screen.getAllByRole("button")[0]);

    await waitFor((): void => {
      expect(screen.getByRole("combobox")).toBeInTheDocument();
    });

    expect(
      screen.queryByText("group.scope.common.add")
    ).not.toBeInTheDocument();

    expect(
      screen.queryByRole("option", {
        name: "group1",
      })
    ).toBeInTheDocument();
    expect(
      screen.queryByRole("option", {
        name: "group2",
      })
    ).not.toBeInTheDocument();

    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "groupName" }),
      ["group1"]
    );
    await userEvent.click(screen.getByText("components.modal.confirm"));

    await waitFor((): void => {
      expect(screen.getByRole("textbox", { name: "branch" })).toHaveValue(
        "main"
      );
    });

    expect(
      screen.queryByRole("textbox", { name: "url" })
    ).not.toBeInTheDocument();
    expect(screen.getAllByRole("textbox")).toHaveLength(4);
    expect(screen.getAllByRole("button")).toHaveLength(7);
    expect(
      screen.getByRole("combobox", { name: "credentials.typeCredential" })
    ).toBeDisabled();
  });

  it("should handle empty", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const mocksRepositories: MockedResponse = {
      request: {
        query: GET_ORGANIZATION_INTEGRATION_REPOSITORIES,
        variables: {
          first: 150,
          organizationId: "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
        },
      },
      result: {
        data: {
          organization: {
            __typename: "Organization",
            integrationRepositoriesConnection: {
              __typename: "IntegrationRepositoriesConnection",
              edges: [],
              pageInfo: {
                endCursor: "bnVsbA==",
                hasNextPage: false,
              },
            },
            name: "orgtest",
          },
        },
      },
    };

    const mockedCredentials: MockedResponse = {
      request: {
        query: GET_ORGANIZATION_CREDENTIALS,
        variables: {
          organizationId: "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
        },
      },
      result: {
        data: {
          organization: {
            __typename: "Organization",
            credentials: [],
            name: "orgtest",
          },
        },
      },
    };

    render(
      <MemoryRouter initialEntries={["/orgs/orgtest/outside"]}>
        <MockedProvider
          addTypename={true}
          mocks={[
            mockedCredentials,
            mocksOrganizationGroups,
            mocksRepositories,
          ]}
        >
          <authzPermissionsContext.Provider value={new PureAbility<string>([])}>
            <authzGroupContext.Provider value={new PureAbility<string>([])}>
              <Route path={"/orgs/:organizationName/outside"}>
                <OrganizationWeakest
                  organizationId={"ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"}
                />
              </Route>
            </authzGroupContext.Provider>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.queryByRole("button")).toBeInTheDocument();
    });

    await userEvent.click(screen.getByRole("button"));

    await waitFor((): void => {
      expect(mockHistoryPush).toHaveBeenCalledTimes(1);
    });

    expect(mockHistoryPush).toHaveBeenCalledWith("/orgs/orgtest/credentials");
  });
});
