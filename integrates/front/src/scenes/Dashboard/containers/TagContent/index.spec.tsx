import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { mount, ReactWrapper } from "enzyme";
import React from "react";
import { Provider } from "react-redux";
import { Route } from "react-router";
import { MemoryRouter } from "react-router-dom";
import { GET_ORGANIZATION_ID } from "scenes/Dashboard/containers/OrganizationContent/queries";
import { TagContent } from "scenes/Dashboard/containers/TagContent";
import store from "store";

describe("TagContent", () => {

  const mocks: MockedResponse = {
    request: {
      query: GET_ORGANIZATION_ID,
      variables: {
        organizationName: "testorg",
      },
    },
    result: {
      data: {
        organizationId: {
          id: "ORG#eb50af04-4d50-4e40-bab1-a3fe9f672f9d",
        },
      },
    },
  };

  it("should return a function", () => {
    expect(typeof (TagContent))
      .toEqual("function");
  });

  it("should render a component", () => {
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/testorg/portfolios/test-projects/indicators"]}>
        <Provider store={store}>
          <MockedProvider mocks={[mocks]} addTypename={false}>
            <Route path="/orgs/:organizationName/portfolios/:tagName/indicators" component={TagContent} />
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );

    expect(wrapper)
      .toHaveLength(1);
  });
});
