import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";

import {
  GET_STAKEHOLDER_PHONE,
  UPDATE_STAKEHOLDER_PHONE_MUTATION,
  VERIFY_STAKEHOLDER_MUTATION,
} from "./queries";

import { MobileModal } from ".";
import { authzPermissionsContext } from "utils/authz/config";
import { msgSuccess } from "utils/notifications";

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

    render(
      <MockedProvider addTypename={false} mocks={mockQuery}>
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

  it("should add a new mobile", async (): Promise<void> => {
    expect.hasAssertions();

    const handleOnClose: jest.Mock = jest.fn();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_update_stakeholder_phone_mutate" },
    ]);
    const mockQuery: MockedResponse[] = [
      {
        request: {
          query: GET_STAKEHOLDER_PHONE,
        },
        result: {
          data: {
            me: {
              __typename: "Me",
              phone: null,
              userEmail: "test@fluidattacks.com",
            },
          },
        },
      },
      {
        request: {
          query: GET_STAKEHOLDER_PHONE,
        },
        result: {
          data: {
            me: {
              __typename: "Me",
              phone: {
                callingCountryCode: "57",
                countryCode: "CO",
                nationalNumber: "123456789",
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
          variables: {
            newPhone: {
              callingCountryCode: "57",
              nationalNumber: "123456789",
            },
          },
        },
        result: { data: { verifyStakeholder: { success: true } } },
      },
      {
        request: {
          query: UPDATE_STAKEHOLDER_PHONE_MUTATION,
          variables: {
            newPhone: { callingCountryCode: "57", nationalNumber: "123456789" },
            verificationCode: "1234",
          },
        },
        result: { data: { updateStakeholderPhone: { success: true } } },
      },
    ];

    render(
      <MockedProvider
        addTypename={false}
        mocks={mockQuery.concat(mocksMutation)}
      >
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <MobileModal onClose={handleOnClose} />
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );

    userEvent.type(screen.getByRole("textbox"), "123456789");
    userEvent.click(
      screen.getByRole("button", { name: "profile.mobileModal.add" })
    );
    await waitFor((): void => {
      expect(
        screen.getByRole("button", { name: "profile.mobileModal.verify" })
      ).toBeInTheDocument();
      expect(msgSuccess).toHaveBeenCalledTimes(1);
      expect(msgSuccess).toHaveBeenLastCalledWith(
        "profile.mobileModal.alerts.sendNewMobileVerificationSuccess",
        "groupAlerts.titleSuccess"
      );
    });

    userEvent.type(
      screen.getByRole("textbox", {
        name: "newVerificationCode",
      }),
      "1234"
    );
    userEvent.click(
      screen.getByRole("button", { name: "profile.mobileModal.verify" })
    );
    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledTimes(2);
      expect(msgSuccess).toHaveBeenLastCalledWith(
        "profile.mobileModal.alerts.additionSuccess",
        "groupAlerts.titleSuccess"
      );
    });

    expect(
      screen.getByRole("button", { name: "profile.mobileModal.close" })
    ).toBeInTheDocument();
    expect(handleOnClose).toHaveBeenCalledTimes(0);

    jest.clearAllMocks();
  });

  it("should edit mobile", async (): Promise<void> => {
    expect.hasAssertions();

    const handleOnClose: jest.Mock = jest.fn();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_update_stakeholder_phone_mutate" },
    ]);
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
                callingCountryCode: "57",
                countryCode: "CO",
                nationalNumber: "123456789",
              },
              userEmail: "test@fluidattacks.com",
            },
          },
        },
      },
      {
        request: {
          query: GET_STAKEHOLDER_PHONE,
        },
        result: {
          data: {
            me: {
              __typename: "Me",
              phone: {
                callingCountryCode: "57",
                countryCode: "CO",
                nationalNumber: "987654321",
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
      {
        request: {
          query: VERIFY_STAKEHOLDER_MUTATION,
          variables: {
            newPhone: {
              callingCountryCode: "57",
              nationalNumber: "987654321",
            },
            verificationCode: "1234",
          },
        },
        result: { data: { verifyStakeholder: { success: true } } },
      },
      {
        request: {
          query: UPDATE_STAKEHOLDER_PHONE_MUTATION,
          variables: {
            newPhone: { callingCountryCode: "57", nationalNumber: "987654321" },
            verificationCode: "1234",
          },
        },
        result: { data: { updateStakeholderPhone: { success: true } } },
      },
    ];

    render(
      <MockedProvider
        addTypename={false}
        mocks={mockQuery.concat(mocksMutation)}
      >
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <MobileModal onClose={handleOnClose} />
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );
    await waitFor((): void => {
      expect(screen.getByDisplayValue("+57 123 456 789")).toBeInTheDocument();
    });

    userEvent.click(
      screen.getByRole("button", { name: "profile.mobileModal.edit" })
    );
    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledTimes(1);
      expect(msgSuccess).toHaveBeenLastCalledWith(
        "profile.mobileModal.alerts.sendCurrentMobileVerificationSuccess",
        "groupAlerts.titleSuccess"
      );
    });

    userEvent.type(
      screen.getByRole("textbox", {
        name: "verificationCode",
      }),
      "1234"
    );
    userEvent.type(screen.getByDisplayValue("+57"), "987654321");
    userEvent.click(
      screen.getByRole("button", { name: "profile.mobileModal.edit" })
    );
    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledTimes(2);
      expect(msgSuccess).toHaveBeenLastCalledWith(
        "profile.mobileModal.alerts.sendNewMobileVerificationSuccess",
        "groupAlerts.titleSuccess"
      );
    });

    userEvent.type(
      screen.getByRole("textbox", {
        name: "newVerificationCode",
      }),
      "1234"
    );
    userEvent.click(
      screen.getByRole("button", { name: "profile.mobileModal.verify" })
    );
    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenLastCalledWith(
        "profile.mobileModal.alerts.editionSuccess",
        "groupAlerts.titleSuccess"
      );
    });

    expect(
      screen.getByRole("button", { name: "profile.mobileModal.close" })
    ).toBeInTheDocument();
    expect(handleOnClose).toHaveBeenCalledTimes(0);

    jest.clearAllMocks();
  });
});
