import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { GraphQLError } from "graphql";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { UNSUBSCRIBE_FROM_GROUP_MUTATION } from "./UnsubscribeModal/queries";

import { Unsubscribe } from ".";
import { msgError, msgSuccess } from "utils/notifications";

jest.mock(
  "../../../../../../../utils/notifications",
  (): Record<string, unknown> => {
    const mockedNotifications: Record<string, () => Record<string, unknown>> =
      jest.requireActual("../../../../../../../utils/notifications");
    jest.spyOn(mockedNotifications, "msgError").mockImplementation();
    jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

    return mockedNotifications;
  }
);

describe("Unsubscribe from group", (): void => {
  const btnConfirm = "components.modal.confirm";

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Unsubscribe).toBe("function");
  });

  it("should unsubscribe from a group", async (): Promise<void> => {
    expect.hasAssertions();

    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: UNSUBSCRIBE_FROM_GROUP_MUTATION,
          variables: {
            groupName: "test",
          },
        },
        result: { data: { unsubscribeFromGroup: { success: true } } },
      },
    ];
    render(
      <MemoryRouter initialEntries={["/test"]}>
        <MockedProvider addTypename={true} mocks={mocksMutation}>
          <Route component={Unsubscribe} path={"/:groupName"} />
        </MockedProvider>
      </MemoryRouter>
    );

    expect(
      screen.queryByText("searchFindings.servicesTable.unsubscribe.button")
    ).toBeInTheDocument();

    await userEvent.click(
      screen.getByText("searchFindings.servicesTable.unsubscribe.button")
    );
    await waitFor((): void => {
      expect(
        screen.getByRole("textbox", { name: "confirmation" })
      ).toBeInTheDocument();
    });

    expect(screen.getByText(btnConfirm)).toBeDisabled();

    await userEvent.type(
      screen.getByRole("textbox", { name: "confirmation" }),
      "test"
    );
    await waitFor((): void => {
      expect(screen.getByText(btnConfirm)).not.toBeDisabled();
    });
    await userEvent.click(screen.getByText(btnConfirm));
    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledWith(
        "searchFindings.servicesTable.unsubscribe.success",
        "searchFindings.servicesTable.unsubscribe.successTitle"
      );
    });
  });

  it("shouldn't unsubscribe from a group", async (): Promise<void> => {
    expect.hasAssertions();

    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: UNSUBSCRIBE_FROM_GROUP_MUTATION,
          variables: {
            groupName: "test",
          },
        },
        result: {
          errors: [new GraphQLError("Access denied")],
        },
      },
    ];
    render(
      <MemoryRouter initialEntries={["/test"]}>
        <MockedProvider addTypename={true} mocks={mocksMutation}>
          <Route component={Unsubscribe} path={"/:groupName"} />
        </MockedProvider>
      </MemoryRouter>
    );

    expect(
      screen.queryByText("searchFindings.servicesTable.unsubscribe.button")
    ).toBeInTheDocument();

    await userEvent.click(
      screen.getByText("searchFindings.servicesTable.unsubscribe.button")
    );
    await waitFor((): void => {
      expect(
        screen.getByRole("textbox", { name: "confirmation" })
      ).toBeInTheDocument();
    });

    expect(screen.getByText(btnConfirm)).toBeDisabled();

    await userEvent.type(
      screen.getByRole("textbox", { name: "confirmation" }),
      "test"
    );
    await userEvent.click(screen.getByText(btnConfirm));
    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith("groupAlerts.errorTextsad");
    });
  });
});
