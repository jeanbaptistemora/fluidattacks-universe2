import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { mount, ReactWrapper } from "enzyme";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { MemoryRouter, Route } from "react-router";
import waitForExpect from "wait-for-expect";
import store from "../../../../store";
import { msgSuccess } from "../../../../utils/notifications";
import { addUserModal } from "../../components/AddUserModal/index";
import { GET_USER } from "../../components/AddUserModal/queries";
import { OrganizationStakeholders } from "./index";
import { ADD_STAKEHOLDER_MUTATION, GET_ORGANIZATION_STAKEHOLDERS } from "./queries";
import { IOrganizationStakeholders } from "./types";

jest.mock("../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary = jest.requireActual("../../../../utils/notifications");
  mockedNotifications.msgSuccess = jest.fn();

  return mockedNotifications;
});

describe("Organization users view", () => {
  const mockProps: IOrganizationStakeholders = { organizationId: "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3" };

  it("should return a function", () => {
    expect(typeof OrganizationStakeholders)
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
              <OrganizationStakeholders {...mockProps} />
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

  it("should add a user", async () => {
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
                  phoneNumber: "+573100000000",
                  role: "group_manager",
                },
              ],
            },
          },
        },
      },
      {
        request: {
          query: GET_USER,
          variables: {
            entity: "ORGANIZATION",
            organizationId: mockProps.organizationId,
            projectName: "-",
            userEmail: "testuser2@gmail.com",
          },
        },
        result: {
          data: {
            stakeholder: {
              email: "testuser2@gmail.com",
              phoneNumber: "+573104448888",
              responsibility: "",
            },
          },
        },
      },
      {
        request: {
          query: ADD_STAKEHOLDER_MUTATION,
          variables: {
            email: "testuser2@gmail.com",
            organizationId: mockProps.organizationId,
            phoneNumber: "+573104448888",
            responsibility: "",
            role: "CUSTOMER",
          },
        },
        result: {
          data: {
            grantStakeholderOrganizationAccess: {
              grantedStakeholder: {
                email: "testuser2@gmail.com",
              },
              success: true,
            },
          },
        },
      },
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
                  phoneNumber: "+573100000000",
                  role: "group_manager",
                },
                {
                  email: "testuser2@gmail.com",
                  firstLogin: "2020-08-01",
                  lastLogin: "[-1, -1]",
                  phoneNumber: "+573104448888",
                  role: "customer",
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
              <OrganizationStakeholders {...mockProps} />
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
          .toHaveLength(2);
      });
    });

    expect(
      wrapper
        .find(addUserModal)
        .prop("open"))
      .toBe(false);

    const addUserButton: ReactWrapper = wrapper
      .find("button#addUser")
      .first();

    addUserButton.simulate("click");

    expect(
      wrapper
        .find(addUserModal)
        .prop("open"))
      .toBe(true);

    const form: ReactWrapper = wrapper
      .find(addUserModal)
      .find("genericForm");
    const emailField: ReactWrapper = wrapper
      .find(addUserModal)
      .find({ name: "email" })
      .find("input");
    const roleField: ReactWrapper = wrapper
      .find(addUserModal)
      .find({ name: "role" })
      .find("select");

    emailField.simulate("change", { target: { value: "testuser2@gmail.com" } });
    emailField.simulate("blur");

    await act(async () => {
      await waitForExpect(() => {
        wrapper.update();

        expect(
          wrapper
            .find(addUserModal)
            .find({ name: "phoneNumber" })
            .find("input")
            .prop("value"))
          .toBe("+57 (310) 444 8888");
      });
    });

    roleField.simulate("change", { target: { value: "CUSTOMER" } });
    form.simulate("submit");

    await act(async () => {
      await waitForExpect(() => {
        wrapper.update();

        expect(
          wrapper
            .find(addUserModal)
            .prop("open"))
          .toBe(false);
        expect(msgSuccess)
          .toHaveBeenCalled();
        expect(wrapper.find("tr"))
          .toHaveLength(3);
      });
    });
  });
});
