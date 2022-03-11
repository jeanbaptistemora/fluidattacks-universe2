import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { useTranslation } from "react-i18next";

import { UPDATE_TOE_LINES_ATTACKED_LINES } from "./queries";

import { HandleEditionModal } from ".";
import type { IToeLinesData } from "../types";
import { authzPermissionsContext } from "utils/authz/config";
import { msgSuccess } from "utils/notifications";

jest.mock("../../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary<() => Dictionary> = jest.requireActual(
    "../../../../../utils/notifications"
  );
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

describe("handle toe lines edition modal", (): void => {
  it("should handle attacked lines edition", async (): Promise<void> => {
    expect.hasAssertions();

    const { t } = useTranslation();

    jest.clearAllMocks();

    const handleRefetchData: jest.Mock = jest.fn();
    const handleCloseModal: jest.Mock = jest.fn();
    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: UPDATE_TOE_LINES_ATTACKED_LINES,
          variables: {
            attackedLines: 5,
            comments: "This is a test of updating toe lines",
            filename: "test/test#.config",
            groupName: "groupname",
            rootId: "63298a73-9dff-46cf-b42d-9b2f01a56690",
          },
        },
        result: { data: { updateToeLinesAttackedLines: { success: true } } },
      },
    ];
    const mokedToeLines: IToeLinesData[] = [
      {
        attackedAt: new Date("2021-02-20T05:00:00+00:00"),
        attackedBy: "test2@test.com",
        attackedLines: 4,
        bePresent: true,
        bePresentUntil: undefined,
        comments: "comment 1",
        coverage: 0.1,
        daysToAttack: 4,
        extension: "config",
        filename: "test/test#.config",
        firstAttackAt: new Date("2020-02-19T15:41:04+00:00"),
        hasVulnerabilities: true,
        lastAuthor: "user@gmail.com",
        lastCommit: "983466z",
        loc: 8,
        modifiedDate: new Date("2020-11-15T15:41:04+00:00"),
        root: {
          id: "63298a73-9dff-46cf-b42d-9b2f01a56690",
          nickname: "product",
        },
        rootId: "63298a73-9dff-46cf-b42d-9b2f01a56690",
        rootNickname: "product",
        seenAt: new Date("2020-02-01T15:41:04+00:00"),
        sortsRiskLevel: 80,
      },
    ];
    render(
      <authzPermissionsContext.Provider value={new PureAbility([])}>
        <MockedProvider
          addTypename={false}
          mocks={[...mocksMutation, ...mocksMutation, ...mocksMutation]}
        >
          <HandleEditionModal
            groupName={"groupname"}
            handleCloseModal={handleCloseModal}
            refetchData={handleRefetchData}
            selectedToeLinesDatas={mokedToeLines}
            setSelectedToeLinesDatas={jest.fn()}
          />
        </MockedProvider>
      </authzPermissionsContext.Provider>
    );

    userEvent.clear(screen.getByRole("spinbutton"));
    userEvent.type(screen.getByRole("spinbutton"), "5");
    userEvent.type(
      screen.getByRole("textbox"),
      "This is a test of updating toe lines"
    );

    userEvent.click(
      screen.getByText(t("group.toe.lines.editModal.procced").toString())
    );

    await waitFor((): void => {
      expect(handleRefetchData).toHaveBeenCalledTimes(1);
    });

    expect(handleCloseModal).toHaveBeenCalledTimes(1);
    expect(msgSuccess).toHaveBeenCalledWith(
      "group.toe.lines.editModal.alerts.success",
      "groupAlerts.updatedTitle"
    );
  });
});
