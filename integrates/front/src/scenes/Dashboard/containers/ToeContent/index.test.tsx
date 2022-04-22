import { MockedProvider } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { ToeContent } from ".";
import { authzPermissionsContext } from "utils/authz/config";

describe("ToeContent", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof ToeContent).toBe("function");
  });

  it("should display toe tabs", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_resolvers_group_toe_lines_resolve" },
      { action: "api_resolvers_group_toe_inputs_resolve" },
    ]);
    render(
      <MemoryRouter initialEntries={["/unittesting/surface/lines"]}>
        <MockedProvider addTypename={false} mocks={[]}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route path={"/:groupName/surface"}>
              <ToeContent isInternal={true} />
            </Route>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryAllByRole("link")).toHaveLength(2);
    });

    expect(
      screen.getByRole("link", { name: "group.toe.tabs.lines.text" })
    ).toBeInTheDocument();
    expect(
      screen.getByRole("link", { name: "group.toe.tabs.inputs.text" })
    ).toBeInTheDocument();
    expect(
      screen.getByRole("link", { name: "group.toe.tabs.lines.text" })
    ).toHaveClass("active");
    expect(
      screen.getByRole("link", { name: "group.toe.tabs.inputs.text" })
    ).not.toHaveClass("active");

    jest.clearAllMocks();
  });
});
