import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { mount, ReactWrapper } from "enzyme";
import { GraphQLError } from "graphql";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { MemoryRouter, Route } from "react-router";
import waitForExpect from "wait-for-expect";
import store from "../../../../store";
import { msgError } from "../../../../utils/notifications";
import { OrganizationPolicies } from "./index";
import { GET_ORGANIZATION_POLICIES } from "./queries";
import { IOrganizationPolicies } from "./types";

jest.mock("../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary = jest.requireActual("../../../../utils/notifications");
  mockedNotifications.msgError = jest.fn();

  return mockedNotifications;
});

describe("Organization policies view", () => {
  const mockProps: IOrganizationPolicies = { organizationId: "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3" };

  it("should return a  function", () => {
    expect(typeof OrganizationPolicies)
      .toEqual("function");
  });

  it("should render component", async (): Promise<void> => {
    const mocks: ReadonlyArray<MockedResponse> = [
      {
        request: {
          query: GET_ORGANIZATION_POLICIES,
          variables: {
            organizationId: mockProps.organizationId,
          },
        },
        result: {
          data: {
            organization: {
              maxAcceptanceDays: 5,
              maxAcceptanceSeverity: 7.5,
              // tslint:disable-next-line: no-null-keyword
              maxNumberAcceptations: null,
              minAcceptanceSeverity: 3,
            },
          },
        },
      },
    ];
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/imamura/policies"]}>
        <Provider store={store}>
          <MockedProvider mocks={mocks} addTypename={false}>
            <Route path="/orgs/:organizationName/policies">
              <OrganizationPolicies {...mockProps} />
            </Route>
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );

    await act(async () => {
      await waitForExpect(() => {
        wrapper.update();

        expect(wrapper)
          .toHaveLength(1);
        expect(wrapper.find("tr"))
          .toHaveLength(4);
      });
    });

    expect(
      wrapper
        .find({ name: "maxAcceptanceDays" })
        .find("input")
        .prop("value"))
      .toBe("5");

    expect(
      wrapper
        .find({ name: "maxAcceptanceSeverity" })
        .find("input")
        .prop("value"))
      .toBe("7.5");

    expect(
      wrapper
        .find({ name: "maxNumberAcceptations" })
        .find("input")
        .prop("value"))
      .toBe("");

    expect(
      wrapper
        .find({ name: "minAcceptanceSeverity" })
        .find("input")
        .prop("value"))
      .toBe("3.0");
  });

  it("should render an error message", async () => {
    const mocks: ReadonlyArray<MockedResponse> = [
      {
        request: {
          query: GET_ORGANIZATION_POLICIES,
          variables: {
            organizationId: mockProps.organizationId,
          },
        },
        result: {
          errors: [new GraphQLError("An error occurred")],
        },
      },
    ];
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/imamura/policies"]}>
        <Provider store={store}>
          <MockedProvider mocks={mocks} addTypename={false}>
            <Route path="/orgs/:organizationName/policies">
              <OrganizationPolicies {...mockProps} />
            </Route>
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );

    await act(async () => {
      await waitForExpect(() => {
        wrapper.update();

        expect(msgError)
          .toHaveBeenCalled();
        expect(wrapper.find("table"))
          .toHaveLength(0);
      });
    });
  });
});
