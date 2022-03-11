import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { useTranslation } from "react-i18next";

import { UPDATE_TOE_INPUT } from "./queries";

import { HandleEditionModal } from ".";
import type { IToeInputData } from "../types";
import { authzPermissionsContext } from "utils/authz/config";
import { msgSuccess } from "utils/notifications";

jest.mock("../../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary<() => Dictionary> = jest.requireActual(
    "../../../../../utils/notifications"
  );
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

describe("handle toe input edition modal", (): void => {
  it("should handle input edition", async (): Promise<void> => {
    expect.hasAssertions();

    const { t } = useTranslation();

    jest.clearAllMocks();

    const handleRefetchData: jest.Mock = jest.fn();
    const handleCloseModal: jest.Mock = jest.fn();
    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: UPDATE_TOE_INPUT,
          variables: {
            bePresent: true,
            component: "https://test.test.com/test/path",
            entryPoint: "-",
            groupName: "groupname",
            hasRecentAttack: true,
            rootId: "1a32cab8-7b4c-4761-a0a5-85cb8b64ce68",
          },
        },
        result: { data: { updateToeInput: { success: true } } },
      },
    ];
    const mokedToeInputs: IToeInputData[] = [
      {
        attackedAt: new Date("2021-02-20T05:00:00+00:00"),
        attackedBy: "test2@test.com",
        bePresent: true,
        bePresentUntil: undefined,
        component: "https://test.test.com/test/path",
        entryPoint: "-",
        firstAttackAt: new Date("2020-02-19T15:41:04+00:00"),
        hasVulnerabilities: true,
        markedSeenFirstTimeBy: "test1@test.com",
        root: {
          id: "1a32cab8-7b4c-4761-a0a5-85cb8b64ce68",
          nickname: "nickname",
        },
        rootId: "1a32cab8-7b4c-4761-a0a5-85cb8b64ce68",
        rootNickname: "nickname",
        seenAt: new Date("2020-02-01T15:41:04+00:00"),
        seenFirstTimeBy: "test1@test.com",
      },
    ];

    render(
      <authzPermissionsContext.Provider value={new PureAbility([])}>
        <MockedProvider addTypename={false} mocks={[...mocksMutation]}>
          <HandleEditionModal
            groupName={"groupname"}
            handleCloseModal={handleCloseModal}
            refetchData={handleRefetchData}
            selectedToeInputDatas={mokedToeInputs}
            setSelectedToeInputDatas={jest.fn()}
          />
        </MockedProvider>
      </authzPermissionsContext.Provider>
    );

    userEvent.click(
      screen.getByText(t("group.toe.inputs.editModal.procced").toString())
    );

    await waitFor((): void => {
      expect(handleCloseModal).toHaveBeenCalledTimes(1);
    });

    expect(handleRefetchData).toHaveBeenCalledTimes(1);
    expect(msgSuccess).toHaveBeenCalledWith(
      "group.toe.inputs.editModal.alerts.success",
      "groupAlerts.updatedTitle"
    );
  });
});
