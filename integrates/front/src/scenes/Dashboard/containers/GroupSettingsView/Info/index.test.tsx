import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { GroupInformation } from "scenes/Dashboard/containers/GroupSettingsView/Info";
import { GET_GROUP_DATA } from "scenes/Dashboard/containers/GroupSettingsView/queries";

describe("Info", (): void => {
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
            businessId: "",
            businessName: "",
            description: "group description",
            hasMachine: true,
            hasSquad: true,
            language: "EN",
            name: "TEST",
            service: "WHITE",
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
      expect(screen.getByRole("table")).toBeInTheDocument();
    });

    expect(
      screen.queryByText("table.noDataIndication")
    ).not.toBeInTheDocument();
    expect(screen.getAllByRole("row")[1].textContent).toBe("LanguageEnglish");
  });
});
