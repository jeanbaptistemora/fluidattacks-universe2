import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { UNSUBSCRIBE_FROM_GROUP_MUTATION } from "./UnsubscribeModal/queries";

import { Unsubscribe } from ".";
import { msgSuccess } from "utils/notifications";

jest.mock("../../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary<() => Dictionary> = jest.requireActual(
    "../../../../../utils/notifications"
  );
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

describe("Unsubscribe from group", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Unsubscribe).toStrictEqual("function");
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

    userEvent.click(
      screen.getByText("searchFindings.servicesTable.unsubscribe.button")
    );
    await waitFor((): void => {
      expect(
        screen.getByRole("textbox", { name: "confirmation" })
      ).toBeInTheDocument();
    });

    expect(screen.getByText("confirmmodal.proceed")).toBeDisabled();

    userEvent.type(
      screen.getByRole("textbox", { name: "confirmation" }),
      "test"
    );
    await waitFor((): void => {
      expect(screen.getByText("confirmmodal.proceed")).not.toBeDisabled();
    });
    userEvent.click(screen.getByText("confirmmodal.proceed"));
    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledWith(
        "searchFindings.servicesTable.unsubscribe.success",
        "searchFindings.servicesTable.unsubscribe.successTitle"
      );
    });
  });
});
