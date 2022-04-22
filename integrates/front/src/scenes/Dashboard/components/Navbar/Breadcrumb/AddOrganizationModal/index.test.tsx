import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";

import { AddOrganizationModal } from "scenes/Dashboard/components/Navbar/Breadcrumb/AddOrganizationModal";
import {
  ADD_NEW_ORGANIZATION,
  GET_AVAILABLE_ORGANIZATION_NAME,
} from "scenes/Dashboard/components/Navbar/Breadcrumb/AddOrganizationModal/queries";

const handleCloseModal: jest.Mock = jest.fn();
const mockHistoryPush: jest.Mock = jest.fn();
jest.mock("react-router-dom", (): Dictionary => {
  const mockedRouter: Dictionary<() => Dictionary> =
    jest.requireActual("react-router-dom");

  return {
    ...mockedRouter,
    useHistory: (): Dictionary => ({
      ...mockedRouter.useHistory(),
      push: mockHistoryPush,
    }),
  };
});

describe("Add organization modal", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof AddOrganizationModal).toBe("function");
  });

  it("should render component", async (): Promise<void> => {
    expect.hasAssertions();

    const mocks: MockedResponse[] = [
      {
        request: {
          query: GET_AVAILABLE_ORGANIZATION_NAME,
        },
        result: {
          data: {
            internalNames: {
              name: "ESDEATH",
            },
          },
        },
      },
    ];

    render(
      <MockedProvider addTypename={false} mocks={mocks}>
        <AddOrganizationModal onClose={handleCloseModal} open={true} />
      </MockedProvider>
    );

    await waitFor((): void => {
      expect(screen.getByRole("textbox")).toHaveAttribute("value", "Esdeath");
    });

    expect(screen.getByRole("textbox")).toBeDisabled();

    userEvent.click(screen.getByText("confirmmodal.cancel"));

    await waitFor((): void => {
      expect(handleCloseModal).toHaveBeenCalledTimes(1);
    });
  });

  it("should create an organization", async (): Promise<void> => {
    expect.hasAssertions();

    const mocks: MockedResponse[] = [
      {
        request: {
          query: GET_AVAILABLE_ORGANIZATION_NAME,
        },
        result: {
          data: {
            internalNames: {
              name: "ESDEATH",
            },
          },
        },
      },
      {
        request: {
          query: ADD_NEW_ORGANIZATION,
          variables: {
            name: "ESDEATH",
          },
        },
        result: {
          data: {
            addOrganization: {
              organization: {
                id: "ORG#eb50af04-4d50-4e40-bab1-a3fe9f672f9d",
                name: "esdeath",
              },
              success: true,
            },
          },
        },
      },
    ];
    render(
      <MockedProvider addTypename={false} mocks={mocks}>
        <AddOrganizationModal onClose={handleCloseModal} open={true} />
      </MockedProvider>
    );

    await waitFor((): void => {
      expect(screen.getByRole("textbox")).toHaveAttribute("value", "Esdeath");
    });

    expect(screen.getByRole("textbox")).toBeDisabled();

    userEvent.click(screen.getByText("confirmmodal.proceed"));

    await waitFor((): void => {
      expect(handleCloseModal).toHaveBeenCalledTimes(1);
    });
    await waitFor((): void => {
      expect(mockHistoryPush).toHaveBeenCalledWith("/orgs/esdeath/");
    });
  });
});
