import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import dayjs from "dayjs";
import React from "react";

import { APITokenModal } from "scenes/Dashboard/components/Navbar/UserProfile/APITokenModal";
import {
  GET_ACCESS_TOKEN,
  UPDATE_ACCESS_TOKEN_MUTATION,
} from "scenes/Dashboard/components/Navbar/UserProfile/APITokenModal/queries";
import type {
  IGetAccessTokenDictAttr,
  IUpdateAccessTokenAttr,
} from "scenes/Dashboard/components/Navbar/UserProfile/APITokenModal/types";
import { msgError, msgSuccess } from "utils/notifications";

jest.mock(
  "../../../../../../utils/notifications",
  (): Record<string, unknown> => {
    const mockedNotifications: Record<string, () => Record<string, unknown>> =
      jest.requireActual("../../../../../../utils/notifications");
    jest.spyOn(mockedNotifications, "msgError").mockImplementation();
    jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

    return mockedNotifications;
  }
);

describe("Update access token modal", (): void => {
  const handleOnClose: jest.Mock = jest.fn();

  const msToSec: number = 1000;
  const yyyymmdd: number = 10;

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof APITokenModal).toBe("function");
  });

  it("should render an add access token modal", async (): Promise<void> => {
    expect.hasAssertions();

    const noAccessToken: IGetAccessTokenDictAttr = {
      hasAccessToken: false,
      issuedAt: "",
      lastAccessTokenUse: null,
    };
    const mockQueryFalse: MockedResponse[] = [
      {
        request: {
          query: GET_ACCESS_TOKEN,
        },
        result: {
          data: {
            me: {
              accessToken: JSON.stringify(noAccessToken),
              userEmail: "test@fluidattacks.com",
            },
          },
        },
      },
    ];

    render(
      <MockedProvider addTypename={false} mocks={mockQueryFalse}>
        <APITokenModal onClose={handleOnClose} open={true} />
      </MockedProvider>
    );

    expect(screen.getByText("updateAccessToken.title")).toBeInTheDocument();
    expect(screen.getByText("components.modal.confirm")).not.toBeDisabled();
    expect(
      screen.getByText("updateAccessToken.expirationTime")
    ).toBeInTheDocument();

    await userEvent.click(screen.getByText("components.modal.cancel"));

    expect(handleOnClose).toHaveBeenCalledTimes(1);
  });

  it("should render a token creation date", async (): Promise<void> => {
    expect.hasAssertions();

    const accessToken: IGetAccessTokenDictAttr = {
      hasAccessToken: true,
      issuedAt: Date.now().toString(),
      lastAccessTokenUse: Date.now().toString(),
    };
    const mockQueryTrue: MockedResponse[] = [
      {
        request: {
          query: GET_ACCESS_TOKEN,
        },
        result: {
          data: {
            me: {
              accessToken: JSON.stringify(accessToken),
              userEmail: "test@fluidattacks.com",
            },
          },
        },
      },
    ];

    render(
      <MockedProvider addTypename={false} mocks={mockQueryTrue}>
        <APITokenModal onClose={handleOnClose} open={true} />
      </MockedProvider>
    );

    await waitFor((): void => {
      expect(
        screen.getByText("updateAccessToken.tokenCreated")
      ).toBeInTheDocument();
    });

    expect(
      screen.queryAllByText("updateAccessToken.expirationTime")
    ).toHaveLength(0);

    await userEvent.click(screen.getByText("updateAccessToken.invalidate"));

    expect(handleOnClose).toHaveBeenCalledTimes(1);
  });

  it("should render a new access token", async (): Promise<void> => {
    expect.hasAssertions();

    const expirationTime: string = dayjs()
      .add(1, "month")
      .toISOString()
      .substring(0, yyyymmdd);
    const updatedAccessToken: IUpdateAccessTokenAttr = {
      updateAccessToken: {
        sessionJwt: "dummyJwt",
        success: true,
      },
    };
    const noAccessToken: IGetAccessTokenDictAttr = {
      hasAccessToken: false,
      issuedAt: "",
      lastAccessTokenUse: null,
    };
    const accessToken: IGetAccessTokenDictAttr = {
      hasAccessToken: true,
      issuedAt: Date.now().toString(),
      lastAccessTokenUse: Date.now().toString(),
    };
    const mockMutation: MockedResponse[] = [
      {
        request: {
          query: GET_ACCESS_TOKEN,
        },
        result: {
          data: {
            me: {
              accessToken: JSON.stringify(noAccessToken),
              userEmail: "test@fluidattacks.com",
            },
          },
        },
      },
      {
        request: {
          query: UPDATE_ACCESS_TOKEN_MUTATION,
          variables: {
            expirationTime: Math.floor(
              new Date(expirationTime).getTime() / msToSec
            ),
          },
        },
        result: {
          data: {
            ...updatedAccessToken,
          },
        },
      },
      {
        request: {
          query: GET_ACCESS_TOKEN,
        },
        result: {
          data: {
            me: {
              accessToken: JSON.stringify(accessToken),
              userEmail: "test@fluidattacks.com",
            },
          },
        },
      },
    ];

    render(
      <MockedProvider addTypename={false} mocks={mockMutation}>
        <APITokenModal onClose={handleOnClose} open={true} />
      </MockedProvider>
    );

    await userEvent.type(
      screen.getByLabelText("expirationTime"),
      expirationTime
    );
    await userEvent.click(screen.getByText("components.modal.confirm"));

    await waitFor((): void => {
      expect(screen.getByText("updateAccessToken.message")).toBeInTheDocument();
    });

    expect(msgSuccess).toHaveBeenCalledWith(
      "updateAccessToken.successfully",
      "updateAccessToken.success"
    );

    await userEvent.click(screen.getByText("updateAccessToken.copy.copy"));

    expect(msgError).toHaveBeenCalledWith("updateAccessToken.copy.failed");
  });
});
