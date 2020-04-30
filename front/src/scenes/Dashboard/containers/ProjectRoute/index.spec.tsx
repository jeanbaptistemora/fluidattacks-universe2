import { MockedProvider, MockedResponse, wait } from "@apollo/react-testing";
import { PureAbility } from "@casl/ability";
import { mount, ReactWrapper, shallow, ShallowWrapper } from "enzyme";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { MemoryRouter, Route } from "react-router-dom";
import { authzContext } from "../../../../utils/authz/config";
import { ProjectRoute } from "./index";
import { GET_PROJECT_ALERT, GET_PROJECT_DATA } from "./queries";

describe("ProjectRoute", () => {

  const projectMock: Readonly<MockedResponse> = {
    request: {
      query: GET_PROJECT_DATA,
      variables: {
        projectName: "TEST",
      },
    },
    result: {
      data: {
        project: {
          deletionDate: "",
          userDeletion: "",
        },
      },
    },
  };

  const alertMock: Readonly<MockedResponse> = {
    request: {
      query: GET_PROJECT_ALERT,
      variables: {
        organization: "Fluid",
        projectName: "TEST",
      },
    },
    result: {
      data: {
        alert: {
          message: "Hello world",
          status: 1,
        },
      },
    },
  };

  it("should return a function", () => {
    expect(typeof (ProjectRoute))
      .toEqual("function");
  });

  it("should render a component", async () => {
    const wrapper: ShallowWrapper = shallow(
      <MockedProvider mocks={[projectMock]} addTypename={false}>
        <ProjectRoute />
      </MockedProvider>,
    );
    await act(async () => { await wait(0); });
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render alert", async () => {
    const mockedPermissions: PureAbility<string> = new PureAbility();
    (window as typeof window & Dictionary<string>).userOrganization = "Fluid";
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/project/TEST/indicators"]}>
        <MockedProvider mocks={[projectMock, alertMock]} addTypename={false}>
          <Route path="/project/:projectName">
            <authzContext.Provider value={mockedPermissions}>
              <ProjectRoute />
            </authzContext.Provider>
          </Route>
        </MockedProvider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper.text())
      .toContain("Hello world");
  });
});
