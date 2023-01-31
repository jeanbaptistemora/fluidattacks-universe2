import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React, { useCallback } from "react";

import { GET_STAKEHOLDER_PHONE, VERIFY_STAKEHOLDER_MUTATION } from "./queries";
import type { IVerifyFn } from "./types";

import { VerifyDialog } from ".";
import { Button } from "components/Button";

describe("VerifyDialog", (): void => {
  const verifyCallback: jest.Mock = jest.fn();
  const cancelCallback: jest.Mock = jest.fn();
  const mockQuery: MockedResponse[] = [
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
  const mocksMutation: readonly MockedResponse[] = [
    {
      request: {
        query: VERIFY_STAKEHOLDER_MUTATION,
      },
      result: { data: { verifyStakeholder: { success: true } } },
    },
  ];
  const TestComponent: React.FC = (): JSX.Element => {
    const handleClick = useCallback(
      (setVerifyCallbacks: IVerifyFn): (() => void) =>
        (): void => {
          setVerifyCallbacks(verifyCallback, cancelCallback);
        },
      []
    );

    return (
      <MockedProvider
        addTypename={false}
        mocks={mockQuery.concat(mocksMutation)}
      >
        <VerifyDialog isOpen={true}>
          {(setVerifyCallbacks): React.ReactNode => {
            return (
              <Button
                onClick={handleClick(setVerifyCallbacks)}
                variant={"primary"}
              >
                {"Button Test"}
              </Button>
            );
          }}
        </VerifyDialog>
      </MockedProvider>
    );
  };

  it("should return a fuction", (): void => {
    expect.hasAssertions();
    expect(typeof VerifyDialog).toBe("function");
  });

  it("should handle stakeholder verification", async (): Promise<void> => {
    expect.hasAssertions();

    render(<TestComponent />);
    await waitFor((): void => {
      expect(screen.queryByText("verifyDialog.verify")).toBeInTheDocument();
    });

    expect(screen.queryByText("Button Test")).toBeInTheDocument();
    expect(screen.queryByText("verifyDialog.title")).toBeInTheDocument();

    await userEvent.click(screen.getByText("Button Test"));
    await userEvent.type(
      screen.getByRole("textbox", {
        name: "verificationCode",
      }),
      "1234"
    );
    await userEvent.click(screen.getByText("verifyDialog.verify"));

    await waitFor((): void => {
      expect(verifyCallback).toHaveBeenCalledTimes(1);
      expect(verifyCallback).toHaveBeenCalledWith("1234");
    });
  });
});
