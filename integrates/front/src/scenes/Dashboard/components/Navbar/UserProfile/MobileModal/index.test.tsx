import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import React from "react";

import { GET_STAKEHOLDER_PHONE } from "./queries";

import { MobileModal } from ".";

jest.mock("../../../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary<() => Dictionary> = jest.requireActual(
    "../../../../../../utils/notifications"
  );
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

describe("Mobile modal", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof MobileModal).toStrictEqual("function");
  });

  it("should display the stakeholder's mobile without edit permission", async (): Promise<void> => {
    expect.hasAssertions();

    const handleOnClose: jest.Mock = jest.fn();

    const mockQueryFalse: MockedResponse[] = [
      {
        request: {
          query: GET_STAKEHOLDER_PHONE,
        },
        result: {
          data: {
            me: {
              __typename: "Me",
              phone: {
                callingCountryCode: "1",
                countryCode: "US",
                nationalNumber: "1234545",
              },
              userEmail: "test@fluidattacks.com",
            },
          },
        },
      },
    ];

    render(
      <MockedProvider addTypename={false} mocks={mockQueryFalse}>
        <MobileModal onClose={handleOnClose} />
      </MockedProvider>
    );
    await waitFor((): void => {
      expect(screen.getByDisplayValue("+1 (123) 454-5")).toBeInTheDocument();
    });

    expect(
      screen.getByRole("button", { name: "profile.mobileModal.close" })
    ).toBeInTheDocument();
    expect(handleOnClose).toHaveBeenCalledTimes(0);
  });
});
