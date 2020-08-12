import { MockedProvider, MockedResponse, wait } from "@apollo/react-testing";
import { PureAbility } from "@casl/ability";
import { mount, ReactWrapper } from "enzyme";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { MemoryRouter, Route } from "react-router";
import store from "../../../../store/index";
import { authzPermissionsContext } from "../../../../utils/authz/config";
import { OrganizationGroups } from "./index";
import { GET_ORGANIZATION_GROUPS } from "./queries";
import { IOrganizationGroupsProps } from "./types";

describe("Organization groups view", () => {
  const mockProps: IOrganizationGroupsProps = {
    organizationId: "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
  };

  const mocks: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: GET_ORGANIZATION_GROUPS,
        variables: {
          organizationId: mockProps.organizationId,
        },
      },
      result: {
        data: {
          organization: {
            projects: [
              {
                description: "Continuous type test project",
                hasDrills: true,
                hasForces: true,
                name: "unittesting",
                userRole: "customer",
              },
              {
                description: "One-shot type test project",
                hasDrills: true,
                hasForces: false,
                name: "oneshottest",
                userRole: "customeradmin",
              },
            ],
          },
        },
      },
    },
  ];

  it("should return a function", () => {
    expect(typeof OrganizationGroups)
      .toEqual("function");
  });

  it("should render a component", async (): Promise<void> => {
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_project__do_create_project" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/imamura/groups"]}>
        <Provider store={store}>
          <MockedProvider mocks={mocks} addTypename={false} >
            <Route path="/orgs/:organizationName/groups">
              <authzPermissionsContext.Provider value={mockedPermissions}>
                <OrganizationGroups {...mockProps} />
              </authzPermissionsContext.Provider>
            </Route>
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );

    expect(wrapper)
      .toHaveLength(1);

    await act(async () => {
      await wait(0);
      wrapper.update();
    });

    const newGroupButton: ReactWrapper = wrapper
      .find("button")
      .first();
    const oneshottestRow: ReactWrapper = wrapper
      .find("tr")
      .at(1);
    const unittestingRow: ReactWrapper = wrapper
      .find("tr")
      .at(2);

    expect(newGroupButton.text())
      .toMatch(/New/);

    expect(oneshottestRow.text())
      .toContain("ONESHOTTEST");
    expect(oneshottestRow.text())
      .toContain("User Manager");
    expect(
        oneshottestRow
          .find("span")
          .filterWhere((element: ReactWrapper) => element.contains("Enabled")))
      .toHaveLength(1);
    expect(
        oneshottestRow
          .find("span")
          .filterWhere((element: ReactWrapper) => element.contains("Disabled")))
      .toHaveLength(1);

    expect(unittestingRow.text())
      .toContain("UNITTESTING");
    expect(unittestingRow.text())
      .toContain("User");
    expect(
        unittestingRow
          .find("span")
          .filterWhere((element: ReactWrapper) => element.contains("Enabled")))
      .toHaveLength(2);
  });
});
