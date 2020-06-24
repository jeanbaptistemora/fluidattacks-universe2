import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { PureAbility } from "@casl/ability";
import { mount, ReactWrapper } from "enzyme";
import { GraphQLError } from "graphql";
import * as React from "react";
import { Provider } from "react-redux";
import { MemoryRouter } from "react-router-dom";
import store from "../../../../store/index";
import { authzPermissionsContext } from "../../../../utils/authz/config";
import { HomeView } from "./index";
import { PROJECTS_QUERY } from "./queries";
import { IHomeViewProps } from "./types";

describe("HomeView", () => {
  const setUserRoleCallback: jest.Mock = jest.fn();
  const mocks: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: PROJECTS_QUERY,
      },
      result: {
        data: {
          me: {
            __typename: "Me",
            projects: [{
              __typename: "Project",
              description: "Project description",
              name: "TEST",
            }],
          },
        },
      },
    }];

  const mockError: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: PROJECTS_QUERY,
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
    }];

  it("should return an object", () => {
    expect(typeof (HomeView))
      .toEqual("function");
  });

  it("should render an error in component", () => {
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/home"]}>
        <Provider store={store}>
          <MockedProvider mocks={mockError} addTypename={true}>
            <HomeView setUserRole={setUserRoleCallback}/>
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render a component", () => {
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/home"]}>
        <Provider store={store}>
          <MockedProvider mocks={mocks} addTypename={true}>
            <HomeView setUserRole={setUserRoleCallback}/>
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    expect(wrapper)
      .toHaveLength(1);
  });
  it("should render new project button", () => {
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_project__do_create_project" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/home"]}>
        <Provider store={store}>
          <MockedProvider mocks={mocks} addTypename={true}>
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <HomeView setUserRole={setUserRoleCallback}/>
            </authzPermissionsContext.Provider>
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    const displayList: ReactWrapper = wrapper.find("input[value=\"list\"]");
    displayList.simulate("change", { target: { checked: true } });
    const projectButton: ReactWrapper = wrapper
      .find("Button")
      .filterWhere((element: ReactWrapper) => element.contains("New"));
    projectButton.simulate("click");
    expect(projectButton)
      .toHaveLength(1);
    expect(wrapper)
      .toHaveLength(1);
  });
});
