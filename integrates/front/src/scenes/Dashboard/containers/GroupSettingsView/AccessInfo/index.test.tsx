import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { AccessInfo } from "scenes/Dashboard/containers/GroupSettingsView/AccessInfo";
import { GET_GROUP_ACCESS_INFO } from "scenes/Dashboard/containers/GroupSettingsView/queries";
import { authzPermissionsContext } from "utils/authz/config";

describe("AccessInfo", (): void => {
  const mockResponse: readonly MockedResponse[] = [
    {
      request: {
        query: GET_GROUP_ACCESS_INFO,
        variables: {
          groupName: "TEST",
        },
      },
      result: {
        data: {
          group: {
            disambiguation: "-",
            groupContext: "-",
          },
        },
      },
    },
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof AccessInfo).toStrictEqual("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_resolvers_group_disambiguation_resolve" },
      { action: "api_mutations_update_group_disambiguation_mutate" },
    ]);
    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <MemoryRouter initialEntries={["/orgs/okada/groups/TEST/scope"]}>
          <MockedProvider addTypename={false} mocks={mockResponse}>
            <Route
              component={AccessInfo}
              path={"/orgs/:organizationName/groups/:groupName/scope"}
            />
          </MockedProvider>
        </MemoryRouter>
      </authzPermissionsContext.Provider>
    );

    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.tabDescription.editable.text")
      ).toBeInTheDocument();
    });

    expect(
      screen.queryByText("searchFindings.groupAccessInfoSection.disambiguation")
    ).toBeInTheDocument();
  });
});
