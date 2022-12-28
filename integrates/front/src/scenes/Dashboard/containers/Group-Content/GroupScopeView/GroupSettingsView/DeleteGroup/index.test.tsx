import { MockedProvider } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { DeleteGroup } from "scenes/Dashboard/containers/Group-Content/GroupScopeView/GroupSettingsView/DeleteGroup";

describe("DeleteGroup", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof DeleteGroup).toBe("function");
  });

  it("should render", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MockedProvider>
        <MemoryRouter initialEntries={["/TEST"]}>
          <Route component={DeleteGroup} path={"/:groupName"} />
        </MemoryRouter>
      </MockedProvider>
    );

    expect(
      screen.queryByRole("button", {
        name: "searchFindings.servicesTable.deleteGroup.deleteGroup",
      })
    ).toBeInTheDocument();
    expect(
      screen.queryByText(
        "searchFindings.servicesTable.deleteGroup.warningTitle"
      )
    ).not.toBeInTheDocument();

    await userEvent.click(screen.getByRole("button"));
    await waitFor((): void => {
      expect(
        screen.queryByText(
          "searchFindings.servicesTable.deleteGroup.warningTitle"
        )
      ).toBeInTheDocument();
    });
  });
});
