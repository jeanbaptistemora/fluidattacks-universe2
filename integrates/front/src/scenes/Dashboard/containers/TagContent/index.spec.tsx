import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { GET_ORGANIZATION_ID } from "scenes/Dashboard/containers/OrganizationContent/queries";
import { TagContent } from "scenes/Dashboard/containers/TagContent";

describe("TagContent", (): void => {
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
          name: "testorg",
        },
      },
    },
  };

  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof TagContent).toStrictEqual("function");
  });

  it("should render a component", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter
        initialEntries={["/orgs/testorg/portfolios/test-projects/analytics"]}
      >
        <MockedProvider addTypename={false} mocks={[mocks]}>
          <Route
            component={TagContent}
            path={"/orgs/:organizationName/portfolios/:tagName/analytics"}
          />
        </MockedProvider>
      </MemoryRouter>
    );

    expect(wrapper).toHaveLength(1);
  });
});
