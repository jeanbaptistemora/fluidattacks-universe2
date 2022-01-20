import { PureAbility } from "@casl/ability";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { act } from "react-dom/test-utils";
import { MemoryRouter, Route } from "react-router-dom";
import waitForExpect from "wait-for-expect";

import { TasksContent } from "scenes/Dashboard/containers/Tasks";
import { AssignedVulnerabilitiesContext } from "scenes/Dashboard/context";
import { authzPermissionsContext } from "utils/authz/config";

describe("VulnerabilitiesView", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof TasksContent).toStrictEqual("function");
  });

  it("should render container", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_resolvers_vulnerability_hacker_resolve" },
    ]);

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/todos"]}>
        <AssignedVulnerabilitiesContext.Provider value={[[], jest.fn()]}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route path={"/todos"}>
              <TasksContent
                meVulnerabilitiesAssigned={{
                  me: {
                    userEmail: "",
                    vulnerabilitiesAssigned: [],
                  },
                }}
                refetchVulnerabilitiesAssigned={jest.fn()}
                setUserRole={jest.fn()}
                userData={{
                  me: {
                    organizations: [{ groups: [], name: "orgtest" }],
                    userEmail: "",
                  },
                }}
              />
            </Route>
          </authzPermissionsContext.Provider>
        </AssignedVulnerabilitiesContext.Provider>
      </MemoryRouter>
    );

    wrapper.update();

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper).toHaveLength(1);
        expect(wrapper.find("tr").at(1).find("td").at(0).text()).toBe(
          "dataTableNext.noDataIndication"
        );
      });
    });
  });
});
