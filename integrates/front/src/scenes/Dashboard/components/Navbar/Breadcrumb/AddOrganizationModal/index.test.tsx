/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";

import { AddOrganizationModal } from "scenes/Dashboard/components/Navbar/Breadcrumb/AddOrganizationModal";
import { ADD_NEW_ORGANIZATION } from "scenes/Dashboard/components/Navbar/Breadcrumb/AddOrganizationModal/queries";

const handleCloseModal: jest.Mock = jest.fn();
const mockHistoryPush: jest.Mock = jest.fn();
jest.mock("react-router-dom", (): Record<string, unknown> => {
  const mockedRouter: Record<string, () => Record<string, unknown>> =
    jest.requireActual("react-router-dom");

  return {
    ...mockedRouter,
    useHistory: (): Record<string, unknown> => ({
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

    const mocks: MockedResponse[] = [];

    render(
      <MockedProvider addTypename={false} mocks={mocks}>
        <AddOrganizationModal onClose={handleCloseModal} open={true} />
      </MockedProvider>
    );

    expect(screen.getAllByRole("textbox")).toHaveLength(2);

    userEvent.click(screen.getByText("components.modal.cancel"));

    await waitFor((): void => {
      expect(handleCloseModal).toHaveBeenCalledTimes(1);
    });
  });

  it("should create an organization", async (): Promise<void> => {
    expect.hasAssertions();

    const mocks: MockedResponse[] = [
      {
        request: {
          query: ADD_NEW_ORGANIZATION,
          variables: {
            country: "Colombia",
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

    userEvent.type(screen.getByLabelText("name"), "esdeath");
    userEvent.type(screen.getByLabelText("country"), "Colombia");

    userEvent.click(screen.getByText("components.modal.confirm"));

    await waitFor((): void => {
      expect(handleCloseModal).toHaveBeenCalledTimes(1);
    });
    await waitFor((): void => {
      expect(mockHistoryPush).toHaveBeenCalledWith("/orgs/esdeath/");
    });
  });
});
