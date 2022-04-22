import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { GraphQLError } from "graphql";
import moment from "moment";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

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
  const mockedNotifications: Dictionary<() => Dictionary> = jest.requireActual(
    "../../../../utils/notifications"
  );
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

describe("Organization users view", (): void => {
  const mockProps: IOrganizationStakeholders = {
    organizationId: "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
  };

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof OrganizationStakeholders).toBe("function");
  });

  it("should render component", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

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
                  invitationState: "CONFIRMED",
                  lastLogin: "2020-09-01",
                  role: "customer_manager",
                },
                {
                  email: "testuser2@gmail.com",
                  firstLogin: "2020-08-01",
                  invitationState: "CONFIRMED",
                  lastLogin: "-",
                  role: "user_manager",
                },
              ],
            },
          },
        },
      },
    ];
    render(
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

    const RENDER_TEST_LENGTH = 3;
    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(RENDER_TEST_LENGTH);
    });

    expect(
      screen.getByText("organization.tabs.users.addButton.text")
    ).not.toBeDisabled();
    expect(
      screen.getByText("organization.tabs.users.editButton.text")
    ).toBeDisabled();
    expect(
      screen.getByText("organization.tabs.users.removeButton.text")
    ).toBeDisabled();

    expect(screen.getByText("testuser1@gmail.com")).toBeInTheDocument();
    expect(screen.getByText("Customer Manager")).toBeInTheDocument();
    expect(screen.getByText("2020-06-01")).toBeInTheDocument();
    expect(
      screen.getByText(moment("2020-09-01", "YYYY-MM-DD hh:mm:ss").fromNow())
    ).toBeInTheDocument();

    expect(screen.getByText("testuser2@gmail.com")).toBeInTheDocument();
    expect(screen.getByText("User Manager")).toBeInTheDocument();
    expect(screen.getByText("2020-08-01")).toBeInTheDocument();
    expect(
      within(screen.queryAllByRole("row")[2]).getByRole("cell", { name: "-" })
    ).toBeInTheDocument();

    userEvent.click(screen.queryAllByRole("row")[1]);

    await waitFor((): void => {
      expect(
        screen.getByText("organization.tabs.users.editButton.text")
      ).not.toBeDisabled();
    });

    expect(
      screen.getByText("organization.tabs.users.removeButton.text")
    ).not.toBeDisabled();
  });

  it("should add a user", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

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
                  invitationState: "CONFIRMED",
                  lastLogin: "2020-10-29 13:40:37",
                  role: "customer_manager",
                },
              ],
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
            role: "USER",
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
                  firstLogin: "2020-06-01 13:40:37",
                  invitationState: "CONFIRMED",
                  lastLogin: "2020-10-29 13:40:37",
                  role: "customer_manager",
                },
                {
                  email: "testuser2@gmail.com",
                  firstLogin: "2020-08-01 13:40:37",
                  invitationState: "CONFIRMED",
                  lastLogin: "2020-10-29 13:40:37",
                  role: "user",
                },
              ],
            },
          },
        },
      },
    ];
    render(
      <MemoryRouter initialEntries={["/orgs/okada/stakeholders"]}>
        <MockedProvider
          addTypename={false}
          mocks={[mocks[0], mocks[1], mocks[2]]}
        >
          <Route path={"/orgs/:organizationName/stakeholders"}>
            <OrganizationStakeholders
              organizationId={mockProps.organizationId}
            />
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(
        screen.getByText("organization.tabs.users.addButton.text")
      ).not.toBeDisabled();
    });

    expect(
      screen.queryByText("organization.tabs.users.modalAddTitle")
    ).not.toBeInTheDocument();

    userEvent.click(screen.getByText("organization.tabs.users.addButton.text"));
    await waitFor((): void => {
      expect(screen.getByText("confirmmodal.proceed")).toBeInTheDocument();
    });
    userEvent.type(
      screen.getByRole("textbox", { name: "email" }),
      "testuser2@gmail.com"
    );
    userEvent.selectOptions(screen.getByRole("combobox", { name: "role" }), [
      "USER",
    ]);
    await waitFor((): void => {
      expect(screen.getByText("confirmmodal.proceed")).not.toBeDisabled();
    });

    userEvent.click(screen.getByText("confirmmodal.proceed"));
    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledWith(
        "testuser2@gmail.comsearchFindings.tabUsers.success",
        "organization.tabs.users.successTitle"
      );
    });
    const TEST_LENGTH = 3;

    expect(screen.getAllByRole("row")).toHaveLength(TEST_LENGTH);
    expect(
      screen.queryByText("organization.tabs.users.modalAddTitle")
    ).not.toBeInTheDocument();
  });

  it("should edit a user", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

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
                  invitationState: "CONFIRMED",
                  lastLogin: "[10, 35207]",
                  role: "user",
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
            role: "USER_MANAGER",
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
                  invitationState: "CONFIRMED",
                  lastLogin: "[10, 35207]",
                  role: "user_manager",
                },
              ],
            },
          },
        },
      },
    ];
    render(
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
    await waitFor((): void => {
      expect(
        screen.getByText("organization.tabs.users.editButton.text")
      ).toBeDisabled();
    });
    userEvent.click(screen.queryAllByRole("row")[1]);
    await waitFor((): void => {
      expect(
        screen.getByText("organization.tabs.users.editButton.text")
      ).not.toBeDisabled();
    });
    userEvent.click(
      screen.getByText("organization.tabs.users.editButton.text")
    );

    await waitFor((): void => {
      expect(screen.getByRole("textbox", { name: "email" })).toHaveValue(
        "testuser1@gmail.com"
      );
    });

    expect(screen.getByRole("textbox", { name: "email" })).toBeDisabled();
    expect(screen.getByRole("combobox", { name: "role" })).toHaveValue("USER");

    userEvent.selectOptions(screen.getByRole("combobox", { name: "role" }), [
      "USER_MANAGER",
    ]);

    userEvent.click(screen.getByText("confirmmodal.proceed"));
    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledWith(
        "testuser1@gmail.com organization.tabs.users.editButton.success",
        "organization.tabs.users.successTitle"
      );
    });

    expect(
      screen.queryByText("organization.tabs.users.modalEditTitle")
    ).not.toBeInTheDocument();
    expect(screen.getAllByRole("row")).toHaveLength(2);
  });

  it("should remove a user", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

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
                  invitationState: "CONFIRMED",
                  lastLogin: "[10, 35207]",
                  role: "customer_manager",
                },
                {
                  email: "testuser2@gmail.com",
                  firstLogin: "2020-08-01",
                  invitationState: "CONFIRMED",
                  lastLogin: "[-1, -1]",
                  role: "user_manager",
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
                  invitationState: "CONFIRMED",
                  lastLogin: "[10, 35207]",
                  role: "customer_manager",
                },
              ],
            },
          },
        },
      },
    ];
    render(
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
    const TEST_LENGTH = 3;
    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(TEST_LENGTH);
    });

    expect(screen.queryAllByRole("radio")[0]).not.toBeChecked();
    expect(screen.queryAllByRole("radio")[1]).not.toBeChecked();
    expect(
      screen.getByText("organization.tabs.users.removeButton.text")
    ).toBeDisabled();

    userEvent.click(screen.queryAllByRole("radio")[1]);

    await waitFor((): void => {
      expect(
        screen.getByText("organization.tabs.users.removeButton.text")
      ).not.toBeDisabled();
    });

    expect(screen.queryAllByRole("radio")[1]).toBeChecked();

    userEvent.click(
      screen.getByText("organization.tabs.users.removeButton.text")
    );
    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledTimes(1);
    });

    expect(screen.queryAllByRole("row")).toHaveLength(2);
    expect(screen.queryAllByRole("radio")[0]).not.toBeChecked();
  });

  it("should handle query errors", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

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
    render(
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

    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith("groupAlerts.errorTextsad");
    });

    expect(screen.queryByText("table.noDataIndication")).toBeInTheDocument();
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
                  invitationState: "CONFIRMED",
                  lastLogin: "[10, 35207]",
                  role: "customer_manager",
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
            role: "USER_MANAGER",
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
            role: "USER_MANAGER",
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
            role: "USER_MANAGER",
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
            role: "USER_MANAGER",
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
            role: "USER_MANAGER",
          },
        },
        result: {
          errors: [new GraphQLError("Access denied")],
        },
      },
    ];
    render(
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

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(2);
    });

    expect(
      screen.getByText("organization.tabs.users.editButton.text")
    ).toBeDisabled();

    userEvent.click(screen.queryAllByRole("row")[1]);
    await waitFor((): void => {
      expect(
        screen.getByText("organization.tabs.users.editButton.text")
      ).not.toBeDisabled();
    });

    expect(
      screen.queryByText("organization.tabs.users.modalEditTitle")
    ).not.toBeInTheDocument();

    const openModal = async (): Promise<void> => {
      userEvent.click(
        screen.getByText("organization.tabs.users.editButton.text")
      );
      await waitFor((): void => {
        expect(
          screen.queryByText("organization.tabs.users.modalEditTitle")
        ).toBeInTheDocument();
      });
    };
    const editStakeholder = async (): Promise<void> => {
      await openModal();
      userEvent.selectOptions(screen.getByRole("combobox", { name: "role" }), [
        "USER_MANAGER",
      ]);
      userEvent.click(screen.getByText("confirmmodal.proceed"));
    };
    await editStakeholder();
    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith(translate.t("validations.email"));
    });

    await editStakeholder();
    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith(
        translate.t("validations.invalidValueInField")
      );
    });

    await editStakeholder();
    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith(
        translate.t("validations.invalidChar")
      );
    });

    await editStakeholder();
    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith(
        translate.t("validations.invalidEmailInField")
      );
    });
    await editStakeholder();
    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith(
        translate.t("groupAlerts.errorTextsad")
      );
    });
  });
});
