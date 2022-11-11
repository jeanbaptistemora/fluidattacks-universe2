/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { GET_ORGANIZATION_CREDENTIALS } from "../GroupScopeView/queries";
import { OrganizationWeakest } from "scenes/Dashboard/containers/OrganizationWeakestView/index";
import {
  GET_ORGANIZATION_GROUPS,
  GET_ORGANIZATION_INTEGRATION_REPOSITORIES,
} from "scenes/Dashboard/containers/OrganizationWeakestView/queries";
import { authzGroupContext, authzPermissionsContext } from "utils/authz/config";

describe("OrganizationWeakestView", (): void => {
  const mocksVulnerabilities: MockedResponse = {
    request: {
      query: GET_ORGANIZATION_INTEGRATION_REPOSITORIES,
      variables: {
        organizationId: "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
      },
    },
    result: {
      data: {
        organization: {
          __typename: "Organization",
          integrationRepositories: [
            {
              __typename: "IntegrationRepositories",
              defaultBranch: "main",
              lastCommitDate: "2022-11-09 02:34:40+00:00",
              url: "https://testrepo.com/testorg1/testproject1/_git/testrepo",
            },
          ],
          name: "orgtest",
        },
      },
    },
  };

  const mocksUserGroups: MockedResponse = {
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
          permissions: [],
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
              id: "6e52c11c-abf7-4ca3-b7d0-635e394f41c1",
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

  it("should handle reattack button basic", async (): Promise<void> => {
    expect.hasAssertions();

    const { container } = render(
      <MemoryRouter initialEntries={["/orgs/orgtest/weakest"]}>
        <MockedProvider
          addTypename={true}
          mocks={[mocksUserGroups, mocksVulnerabilities, mockedOrgCredentials]}
        >
          <authzPermissionsContext.Provider value={new PureAbility<string>([])}>
            <authzGroupContext.Provider value={new PureAbility<string>([])}>
              <Route path={"/orgs/:organizationName/weakest"}>
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

    fireEvent.click(screen.getByRole("button"));

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
  });
});