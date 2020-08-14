import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { mount, ReactWrapper } from "enzyme";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { MemoryRouter, Route } from "react-router";
import waitForExpect from "wait-for-expect";
import store from "../../../../store";
import { OrganizationUsers } from "./index";
import { GET_ORGANIZATION_STAKEHOLDERS } from "./queries";
import { IOrganizationUsers } from "./types";

describe("Organization users view", () => {
  const mockProps: IOrganizationUsers = { organizationId: "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3" };

  it("should return a function", () => {
    expect(typeof OrganizationUsers)
      .toEqual("function");
  });

  it("should render component", async () => {
    const mocks: ReadonlyArray<MockedResponse> = [
      {
        request: {
          query: GET_ORGANIZATION_STAKEHOLDERS,
          variables: {
            organizationId: mockProps.organizationId,
          },
        },
        result: {
          data: {
            organization: {
              stakeholders: [
                {
                  email: "testuser1@gmail.com",
                  firstLogin: "2020-06-01",
                  lastLogin: "[10, 35207]",
                  phoneNumber: "3100000000",
                  role: "group_manager",
                },
                {
                  email: "testuser2@gmail.com",
                  firstLogin: "2020-08-01",
                  lastLogin: "[-1, -1]",
                  phoneNumber: "3140000000",
                  role: "customeradmin",
                },
              ],
            },
          },
        },
      },
    ];
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/imamura/stakeholders"]} >
        <Provider store={store}>
          <MockedProvider mocks={mocks} addTypename={false} >
            <Route path="/orgs/:organizationName/stakeholders" >
              <OrganizationUsers {...mockProps} />
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
          .toHaveLength(3);
      });
    });

    const addButton: ReactWrapper = wrapper
      .find("button#addUser")
      .first();
    const editButton: ReactWrapper = wrapper
      .find("button#editUser")
      .first();
    const removeButton: ReactWrapper = wrapper
      .find("button#removeUser")
      .first();

    expect(addButton.prop("disabled"))
      .toBeUndefined();
    expect(editButton.prop("disabled"))
      .toBe(true);
    expect(removeButton.prop("disabled"))
      .toBe(true);

    const user1Cells: ReactWrapper = wrapper
      .find("tr")
      .at(1)
      .find("td");
    const user2Cells: ReactWrapper = wrapper
      .find("tr")
      .at(2)
      .find("td");

    expect(
      user1Cells
        .at(1)
        .text())
      .toBe("testuser1@gmail.com");
    expect(
      user1Cells
        .at(2)
        .text())
      .toBe("Group Manager");
    expect(
      user1Cells
        .at(3)
        .text())
      .toBe("3100000000");
    expect(
      user1Cells
        .at(4)
        .text())
      .toBe("2020-06-01");
    expect(
      user1Cells
        .at(5)
        .text())
      .toBe("10 days ago");

    expect(
      user2Cells
        .at(1)
        .text())
      .toBe("testuser2@gmail.com");
    expect(
      user2Cells
        .at(2)
        .text())
      .toBe("User Manager");
    expect(
      user2Cells
        .at(3)
        .text())
      .toBe("3140000000");
    expect(
      user2Cells
        .at(4)
        .text())
      .toBe("-");
    expect(
      user2Cells
        .at(5)
        .text())
      .toBe("-");

    wrapper
      .find("tr")
      .at(1)
      .simulate("click");

    expect(
      wrapper
        .find("button#editUser")
        .first()
        .prop("disabled"))
      .toBe(false);
    expect(
      wrapper
        .find("button#removeUser")
        .first()
        .prop("disabled"))
      .toBe(false);
  });
});
