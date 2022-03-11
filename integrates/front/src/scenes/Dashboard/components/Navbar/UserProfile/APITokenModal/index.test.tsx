import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import moment from "moment";
import React from "react";
import { useTranslation } from "react-i18next";

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

jest.mock("../../../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary<() => Dictionary> = jest.requireActual(
    "../../../../../../utils/notifications"
  );
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

describe("Update access token modal", (): void => {
  const handleOnClose: jest.Mock = jest.fn();

  const msToSec: number = 1000;
  const yyyymmdd: number = 10;

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof APITokenModal).toStrictEqual("function");
  });

  it("should render an add access token modal", (): void => {
    expect.hasAssertions();

    const { t } = useTranslation();

    const noAccessToken: IGetAccessTokenDictAttr = {
      hasAccessToken: false,
      issuedAt: "",
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

    expect(
      screen.getByText(t("updateAccessToken.title").toString())
    ).toBeInTheDocument();
    expect(
      screen.getByText(t("confirmmodal.proceed").toString())
    ).not.toBeDisabled();
    expect(
      screen.getByText(t("updateAccessToken.expirationTime").toString())
    ).toBeInTheDocument();

    userEvent.click(screen.getByText(t("updateAccessToken.close").toString()));

    expect(handleOnClose).toHaveBeenCalledTimes(1);
  });

  it("should render a token creation date", async (): Promise<void> => {
    expect.hasAssertions();

    const { t } = useTranslation();

    const accessToken: IGetAccessTokenDictAttr = {
      hasAccessToken: true,
      issuedAt: Date.now().toString(),
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
        screen.getByText(t("updateAccessToken.tokenCreated").toString())
      ).toBeInTheDocument();
    });

    expect(
      screen.getByText(t("confirmmodal.proceed").toString())
    ).toBeDisabled();
    expect(
      screen.queryAllByText(t("updateAccessToken.expirationTime").toString())
    ).toHaveLength(0);

    userEvent.click(
      screen.getByText(t("updateAccessToken.invalidate").toString())
    );

    expect(handleOnClose).toHaveBeenCalledTimes(1);
  });

  it("should render a new access token", async (): Promise<void> => {
    expect.hasAssertions();

    const { t } = useTranslation();

    const expirationTime: string = moment()
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
    };
    const accessToken: IGetAccessTokenDictAttr = {
      hasAccessToken: true,
      issuedAt: Date.now().toString(),
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

    userEvent.type(screen.getByTestId("expiration-time-input"), expirationTime);
    userEvent.click(screen.getByText(t("confirmmodal.proceed").toString()));

    await waitFor((): void => {
      expect(
        screen.getByText(t("updateAccessToken.accessToken").toString())
      ).toBeInTheDocument();
    });

    expect(msgSuccess).toHaveBeenCalledWith(
      t("updateAccessToken.successfully"),
      t("updateAccessToken.success")
    );

    userEvent.click(
      screen.getByText(t("updateAccessToken.copy.copy").toString())
    );

    expect(msgError).toHaveBeenCalledWith(t("updateAccessToken.copy.failed"));
  });
});
