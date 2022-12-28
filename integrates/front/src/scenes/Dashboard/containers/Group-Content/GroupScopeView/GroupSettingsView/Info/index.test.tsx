import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { GroupInformation } from "scenes/Dashboard/containers/Group-Content/GroupScopeView/GroupSettingsView/Info";
import { GET_GROUP_DATA } from "scenes/Dashboard/containers/Group-Content/GroupScopeView/GroupSettingsView/queries";

describe("Info", (): void => {
  const labels = [
    "organization.tabs.groups.newGroup.businessId.text",
    "organization.tabs.groups.newGroup.businessName.text",
    "organization.tabs.groups.newGroup.description.text",
    "organization.tabs.groups.newGroup.language.text",
    "organization.tabs.groups.newGroup.sprintDuration.text",
    "organization.tabs.groups.editGroup.sprintStartDate.text",
    "organization.tabs.groups.newGroup.managed.text",
  ];

  const mocksInfo: readonly MockedResponse[] = [
    {
      request: {
        query: GET_GROUP_DATA,
        variables: {
          groupName: "TEST",
        },
      },
      result: {
        data: {
          group: {
            businessId: "1444",
            businessName: "Testing Company and Mocks",
            description: "group description",
            hasMachine: true,
            hasSquad: true,
            language: "EN",
            name: "TEST",
            service: "WHITE",
            sprintDuration: "2",
            sprintStartDate: "2022-06-06T00:00:00",
            subscription: "TEST",
          },
        },
      },
    },
  ];

  it("should return a function group info", (): void => {
    expect.hasAssertions();
    expect(typeof GroupInformation).toBe("function");
  });

  it("should show group info", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MockedProvider addTypename={false} mocks={mocksInfo}>
        <MemoryRouter initialEntries={["/orgs/okada/groups/TEST/scope"]}>
          <Route
            component={GroupInformation}
            path={"/orgs/:organizationName/groups/:groupName/scope"}
          />
        </MemoryRouter>
      </MockedProvider>
    );

    await waitFor((): void => {
      expect(
        screen.queryByText("table.noDataIndication")
      ).not.toBeInTheDocument();

      labels.forEach((label): void => {
        expect(screen.queryByText(label)).toBeInTheDocument();
      });
    });
  });
});
