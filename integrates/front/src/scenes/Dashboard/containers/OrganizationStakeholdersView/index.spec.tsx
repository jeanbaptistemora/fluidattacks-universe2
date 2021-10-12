// Needed to lazy test formik components
/* eslint-disable @typescript-eslint/no-unsafe-return */
import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import { GraphQLError } from "graphql";
import moment from "moment";
import React from "react";
import { act } from "react-dom/test-utils";
import { MemoryRouter, Route } from "react-router-dom";
import wait from "waait";
import waitForExpect from "wait-for-expect";

import { AddUserModal } from "scenes/Dashboard/components/AddUserModal/index";
import { GET_STAKEHOLDER } from "scenes/Dashboard/components/AddUserModal/queries";
import { OrganizationStakeholders } from "scenes/Dashboard/containers/OrganizationStakeholdersView";
import {
  ADD_STAKEHOLDER_MUTATION,
  GET_ORGANIZATION_STAKEHOLDERS,
  REMOVE_STAKEHOLDER_MUTATION,
  UPDATE_STAKEHOLDER_MUTATION,
} from "scenes/Dashboard/containers/OrganizationStakeholdersView/queries";
import type { IOrganizationStakeholders } from "scenes/Dashboard/containers/OrganizationStakeholdersView/types";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

jest.mock("../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary = jest.requireActual(
    "../../../../utils/notifications"
  );
  mockedNotifications.msgError = jest.fn(); // eslint-disable-line fp/no-mutation, jest/prefer-spy-on
  mockedNotifications.msgSuccess = jest.fn(); // eslint-disable-line fp/no-mutation, jest/prefer-spy-on

  return mockedNotifications;
});

describe("Organization users view", (): void => {
  const mockProps: IOrganizationStakeholders = {
    organizationId: "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
  };

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof OrganizationStakeholders).toStrictEqual("function");
  });

  it("should render component", async (): Promise<void> => {
    expect.hasAssertions();

    const mocks: readonly MockedResponse[] = [
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
              name: "okada",
              stakeholders: [
                {
                  email: "testuser1@gmail.com",
                  firstLogin: "2020-06-01",
                  lastLogin: "2020-09-01",
                  role: "system_owner",
                },
                {
                  email: "testuser2@gmail.com",
                  firstLogin: "2020-08-01",
                  lastLogin: "-",
                  role: "customeradmin",
                },
              ],
            },
          },
        },
      },
    ];
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/okada/stakeholders"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route path={"/orgs/:organizationName/stakeholders"}>
            <OrganizationStakeholders
              organizationId={mockProps.organizationId}
            />
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper).toHaveLength(1);

        const RENDER_TEST_LENGTH = 3;

        expect(wrapper.find("tr")).toHaveLength(RENDER_TEST_LENGTH);
      });
    });

    const addButton: ReactWrapper = wrapper.find("button#addUser").first();
    const editButton: ReactWrapper = wrapper.find("button#editUser").first();
    const removeButton: ReactWrapper = wrapper
      .find("button#removeUser")
      .first();

    expect(addButton.prop("disabled")).toBeUndefined();
    expect(editButton.prop("disabled")).toBe(true);
    expect(removeButton.prop("disabled")).toBe(true);

    const user1Cells: ReactWrapper = wrapper.find("tr").at(1).find("td");
    const user2Cells: ReactWrapper = wrapper.find("tr").at(2).find("td");

    const RENDER_TEST_AT5 = 5;

    expect(user1Cells.at(1).text()).toBe("testuser1@gmail.com");
    expect(user1Cells.at(2).text()).toBe("System Owner");
    expect(user1Cells.at(4).text()).toBe("2020-06-01");
    expect(user1Cells.at(RENDER_TEST_AT5).text()).toBe(
      moment("2020-09-01", "YYYY-MM-DD hh:mm:ss").fromNow()
    );

    expect(user2Cells.at(1).text()).toBe("testuser2@gmail.com");
    expect(user2Cells.at(2).text()).toBe("User Manager");
    expect(user2Cells.at(4).text()).toBe("2020-08-01");
    expect(user2Cells.at(RENDER_TEST_AT5).text()).toBe("-");

    wrapper.find("tr").at(1).simulate("click");

    expect(wrapper.find("button#editUser").first().prop("disabled")).toBe(
      false
    );
    expect(wrapper.find("button#removeUser").first().prop("disabled")).toBe(
      false
    );
  });

  // Temporarily disabled until it gets properly refactored to use Formik
  // eslint-disable-next-line jest/no-disabled-tests
  it.skip("should add a user", async (): Promise<void> => {
    expect.hasAssertions();

    const mocks: readonly MockedResponse[] = [
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
              name: "okada",
              stakeholders: [
                {
                  email: "testuser1@gmail.com",
                  firstLogin: "2020-06-01",
                  lastLogin: "[10, 35207]",
                  role: "system_owner",
                },
              ],
            },
          },
        },
      },
      {
        request: {
          query: GET_STAKEHOLDER,
          variables: {
            entity: "ORGANIZATION",
            groupName: "-",
            organizationId: mockProps.organizationId,
            userEmail: "testuser2@gmail.com",
          },
        },
        result: {
          data: {
            stakeholder: {
              email: "testuser2@gmail.com",
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
              name: "okada",
              stakeholders: [
                {
                  email: "testuser1@gmail.com",
                  firstLogin: "2020-06-01",
                  lastLogin: "[10, 35207]",
                  role: "system_owner",
                },
                {
                  email: "testuser2@gmail.com",
                  firstLogin: "2020-08-01",
                  lastLogin: "[-1, -1]",
                  role: "customer",
                },
              ],
            },
          },
        },
      },
    ];
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/okada/stakeholders"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route path={"/orgs/:organizationName/stakeholders"}>
            <OrganizationStakeholders
              organizationId={mockProps.organizationId}
            />
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );

    await act(async (): Promise<void> => {
      wrapper.update();
      await wait(0);
    });

    expect(wrapper).toHaveLength(1);
    expect(wrapper.find("tr")).toHaveLength(2);
    expect(wrapper.find(AddUserModal).prop("open")).toBe(false);

    const addUserButton = (): ReactWrapper =>
      wrapper.find("button#addUser").first();

    addUserButton().simulate("click");

    expect(wrapper.find(AddUserModal).prop("open")).toBe(true);

    const form = (): ReactWrapper => wrapper.find(AddUserModal).find("Formik");
    const emailField = (): ReactWrapper =>
      wrapper.find(AddUserModal).find({ name: "email" }).find("input");
    const roleField = (): ReactWrapper =>
      wrapper.find(AddUserModal).find({ name: "role" }).find("select");

    emailField().simulate("change", {
      target: { name: "email", value: "testuser2@gmail.com" },
    });
    emailField().simulate("blur", {
      target: { name: "email" },
    });
    roleField().simulate("change", {
      target: { name: "role", value: "CUSTOMER" },
    });
    form().simulate("submit");

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper.find(AddUserModal).prop("open")).toBe(false);

        expect(msgSuccess).toHaveBeenCalled(); // eslint-disable-line jest/prefer-called-with
        expect(wrapper.find("tr")).toHaveLength(2);
      });
    });
  });

  it("should edit a user", async (): Promise<void> => {
    expect.hasAssertions();

    const mocks: readonly MockedResponse[] = [
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
              name: "okada",
              stakeholders: [
                {
                  email: "testuser1@gmail.com",
                  firstLogin: "2020-06-01",
                  lastLogin: "[10, 35207]",
                  role: "customer",
                },
              ],
            },
          },
        },
      },
      {
        request: {
          query: UPDATE_STAKEHOLDER_MUTATION,
          variables: {
            email: "testuser1@gmail.com",
            organizationId: mockProps.organizationId,
            responsibility: "",
            role: "CUSTOMERADMIN",
          },
        },
        result: {
          data: {
            updateOrganizationStakeholder: {
              modifiedStakeholder: {
                email: "testuser1@gmail.com",
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
              name: "okada",
              stakeholders: [
                {
                  email: "testuser1@gmail.com",
                  firstLogin: "2020-06-01",
                  lastLogin: "[10, 35207]",
                  role: "customeradmin",
                },
              ],
            },
          },
        },
      },
    ];
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/okada/stakeholders"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route path={"/orgs/:organizationName/stakeholders"}>
            <OrganizationStakeholders
              organizationId={mockProps.organizationId}
            />
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );

    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    expect(wrapper).toHaveLength(1);
    expect(wrapper.find("tr")).toHaveLength(2);

    expect(wrapper.find(AddUserModal).prop("open")).toBe(false);

    wrapper.find("tr").at(1).simulate("click");

    wrapper.find("button#editUser").first().simulate("click");

    expect(wrapper.find(AddUserModal).prop("open")).toBe(true);
    expect(
      wrapper
        .find(AddUserModal)
        .find({ name: "email" })
        .find("input")
        .prop("value")
    ).toBe("testuser1@gmail.com");
    expect(
      wrapper
        .find(AddUserModal)
        .find({ name: "email" })
        .find("input")
        .prop("disabled")
    ).toBe(true);
    expect(
      wrapper
        .find(AddUserModal)
        .find({ name: "role" })
        .find("select")
        .prop("value")
    ).toBe("CUSTOMER");

    const form: ReactWrapper = wrapper.find(AddUserModal).find("Formik");
    const roleField: ReactWrapper = wrapper
      .find(AddUserModal)
      .find({ name: "role" })
      .find("select");

    roleField.simulate("change", {
      target: { name: "role", value: "CUSTOMERADMIN" },
    });
    form.simulate("submit");

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper.find(AddUserModal).prop("open")).toBe(false);
        expect(msgSuccess).toHaveBeenCalled(); // eslint-disable-line jest/prefer-called-with
        expect(wrapper.find("tr")).toHaveLength(2);
      });
    });
  });

  it("should remove a user", async (): Promise<void> => {
    expect.hasAssertions();

    const mocks: readonly MockedResponse[] = [
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
              name: "okada",
              stakeholders: [
                {
                  email: "testuser1@gmail.com",
                  firstLogin: "2020-06-01",
                  lastLogin: "[10, 35207]",
                  role: "system_owner",
                },
                {
                  email: "testuser2@gmail.com",
                  firstLogin: "2020-08-01",
                  lastLogin: "[-1, -1]",
                  role: "customeradmin",
                },
              ],
            },
          },
        },
      },
      {
        request: {
          query: REMOVE_STAKEHOLDER_MUTATION,
          variables: {
            organizationId: mockProps.organizationId,
            userEmail: "testuser2@gmail.com",
          },
        },
        result: {
          data: {
            removeStakeholderOrganizationAccess: {
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
              name: "okada",
              stakeholders: [
                {
                  email: "testuser1@gmail.com",
                  firstLogin: "2020-06-01",
                  lastLogin: "[10, 35207]",
                  role: "system_owner",
                },
              ],
            },
          },
        },
      },
    ];
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/okada/stakeholders"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route path={"/orgs/:organizationName/stakeholders"}>
            <OrganizationStakeholders
              organizationId={mockProps.organizationId}
            />
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        const TEST_LENGTH = 3;

        expect(wrapper).toHaveLength(1);
        expect(wrapper.find("tr")).toHaveLength(TEST_LENGTH);
      });
    });

    wrapper.find("tr").at(2).simulate("click");

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper.find("button#removeUser").first().prop("disabled")).toBe(
          false
        );
      });
    });

    wrapper.find("button#removeUser").first().simulate("click");

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(msgSuccess).toHaveBeenCalled(); // eslint-disable-line jest/prefer-called-with
        expect(wrapper.find("tr")).toHaveLength(2);
      });
    });
  });

  it("should handle query errors", async (): Promise<void> => {
    expect.hasAssertions();

    const mocks: readonly MockedResponse[] = [
      {
        request: {
          query: GET_ORGANIZATION_STAKEHOLDERS,
          variables: {
            organizationId: mockProps.organizationId,
          },
        },
        result: {
          errors: [
            new GraphQLError("An error occurred fetching organization users"),
          ],
        },
      },
    ];
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/okada/stakeholders"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route path={"/orgs/:organizationName/stakeholders"}>
            <OrganizationStakeholders
              organizationId={mockProps.organizationId}
            />
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(msgError).toHaveBeenCalled(); // eslint-disable-line jest/prefer-called-with
        expect(wrapper.find("tr").at(1).find("td").at(0).text()).toBe(
          "dataTableNext.noDataIndication"
        );
      });
    });
  });

  it("should handle mutation errors", async (): Promise<void> => {
    expect.hasAssertions();

    const mocks: readonly MockedResponse[] = [
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
              name: "okada",
              stakeholders: [
                {
                  email: "testuser1@gmail.com",
                  firstLogin: "2020-06-01",
                  lastLogin: "[10, 35207]",
                  role: "system_owner",
                },
              ],
            },
          },
        },
      },
      {
        request: {
          query: UPDATE_STAKEHOLDER_MUTATION,
          variables: {
            email: "testuser1@gmail.com",
            organizationId: mockProps.organizationId,
            responsibility: "",
            role: "CUSTOMERADMIN",
          },
        },
        result: {
          errors: [new GraphQLError("Exception - Email is not valid")],
        },
      },
      {
        request: {
          query: UPDATE_STAKEHOLDER_MUTATION,
          variables: {
            email: "testuser1@gmail.com",
            organizationId: mockProps.organizationId,
            responsibility: "",
            role: "CUSTOMERADMIN",
          },
        },
        result: {
          errors: [new GraphQLError("Exception - Invalid field in form")],
        },
      },
      {
        request: {
          query: UPDATE_STAKEHOLDER_MUTATION,
          variables: {
            email: "testuser1@gmail.com",
            organizationId: mockProps.organizationId,
            responsibility: "",
            role: "CUSTOMERADMIN",
          },
        },
        result: {
          errors: [new GraphQLError("Exception - Invalid characters")],
        },
      },
      {
        request: {
          query: UPDATE_STAKEHOLDER_MUTATION,
          variables: {
            email: "testuser1@gmail.com",
            organizationId: mockProps.organizationId,
            responsibility: "",
            role: "CUSTOMERADMIN",
          },
        },
        result: {
          errors: [
            new GraphQLError("Exception - Invalid phone number in form"),
          ],
        },
      },
      {
        request: {
          query: UPDATE_STAKEHOLDER_MUTATION,
          variables: {
            email: "testuser1@gmail.com",
            organizationId: mockProps.organizationId,
            responsibility: "",
            role: "CUSTOMERADMIN",
          },
        },
        result: {
          errors: [
            new GraphQLError("Exception - Invalid email address in form"),
          ],
        },
      },
      {
        request: {
          query: UPDATE_STAKEHOLDER_MUTATION,
          variables: {
            email: "testuser1@gmail.com",
            organizationId: mockProps.organizationId,
            responsibility: "",
            role: "CUSTOMERADMIN",
          },
        },
        result: {
          errors: [new GraphQLError("Access denied")],
        },
      },
    ];
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/okada/stakeholders"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route path={"/orgs/:organizationName/stakeholders"}>
            <OrganizationStakeholders
              organizationId={mockProps.organizationId}
            />
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );

    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    expect(wrapper).toHaveLength(1);
    expect(wrapper.find("tr")).toHaveLength(2);

    wrapper.find("tr").at(1).simulate("click");

    const openModal: () => void = (): void => {
      wrapper.find("button#editUser").first().simulate("click");
    };

    const getForm: () => ReactWrapper = (): ReactWrapper =>
      // eslint-disable-next-line @typescript-eslint/no-unsafe-return
      wrapper.find(AddUserModal).find("Formik");
    const getRoleField: () => ReactWrapper = (): ReactWrapper =>
      // eslint-disable-next-line @typescript-eslint/no-unsafe-return
      wrapper.find(AddUserModal).find({ name: "role" }).find("select");
    const submit: () => void = (): void => {
      openModal();

      expect(wrapper.find(AddUserModal).prop("open")).toBe(true);

      getRoleField().simulate("change", {
        target: { name: "role", value: "CUSTOMERADMIN" },
      });
      getForm().simulate("submit");
    };

    submit();

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(msgError).toHaveBeenCalledWith(translate.t("validations.email"));
      });
    });

    submit();

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(msgError).toHaveBeenCalledWith(
          translate.t("validations.invalidValueInField")
        );
      });
    });

    submit();

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(msgError).toHaveBeenCalledWith(
          translate.t("validations.invalidChar")
        );
      });
    });

    submit();

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(msgError).toHaveBeenCalledWith(
          translate.t("validations.invalidPhoneNumberInField")
        );
      });
    });

    submit();

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(msgError).toHaveBeenCalledWith(
          translate.t("validations.invalidEmailInField")
        );
      });
    });

    submit();

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(msgError).toHaveBeenCalledWith(
          translate.t("groupAlerts.errorTextsad")
        );
      });
    });
  });
});
