import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import { Field } from "formik";
import React from "react";
import { act } from "react-dom/test-utils";
import waitForExpect from "wait-for-expect";

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

    jest.clearAllMocks();

    const handleRefetchData: jest.Mock = jest.fn();
    const handleCloseModal: jest.Mock = jest.fn();
    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: UPDATE_TOE_LINES_ATTACKED_LINES,
          variables: {
            attackedAt: "2021-02-20T06:52:00+00:00",
            attackedLines: 5,
            comments: "This is a test of updating toe lines",
            filenames: ["test/test#.config"],
            groupName: "groupname",
            rootId: "63298a73-9dff-46cf-b42d-9b2f01a56690",
          },
        },
        result: { data: { updateToeLinesAttackedLines: { success: true } } },
      },
    ];
    const mokedVulns: IToeLinesData[] = [
      {
        attackedAt: "2021-02-20T05:00:00+00:00",
        attackedBy: "test2@test.com",
        attackedLines: 4,
        bePresent: true,
        bePresentUntil: "",
        comments: "comment 1",
        commitAuthor: "customer@gmail.com",
        coverage: 0.1,
        daysToAttack: 4,
        filename: "test/test#.config",
        firstAttackAt: "2020-02-19T15:41:04+00:00",
        loc: 8,
        modifiedCommit: "983466z",
        modifiedDate: "2020-11-15T15:41:04+00:00",
        root: {
          id: "63298a73-9dff-46cf-b42d-9b2f01a56690",
          nickname: "product",
        },
        rootId: "63298a73-9dff-46cf-b42d-9b2f01a56690",
        rootNickname: "product",
        seenAt: "2020-02-01T15:41:04+00:00",
        sortsRiskLevel: "80%",
      },
    ];
    const wrapper: ReactWrapper = mount(
      <MockedProvider
        addTypename={false}
        mocks={[...mocksMutation, ...mocksMutation, ...mocksMutation]}
      >
        <HandleEditionModal
          groupName={"groupname"}
          handleCloseModal={handleCloseModal}
          refetchData={handleRefetchData}
          selectedToeLinesDatas={mokedVulns}
        />
      </MockedProvider>,
      {
        wrappingComponent: authzPermissionsContext.Provider,
      }
    );

    const attackedAtFieldInput: ReactWrapper = wrapper
      .find(Field)
      .filter({ name: "attackedAt" })
      .find("input");
    attackedAtFieldInput.simulate("change", {
      target: {
        name: "attackedAt",
        value: "02/20/2021 6:52 AM",
      },
    });
    const attackedLinesFieldInput: ReactWrapper = wrapper
      .find(Field)
      .filter({ name: "attackedLines" })
      .find("input");
    attackedLinesFieldInput.simulate("change", {
      target: {
        name: "attackedLines",
        value: 5,
      },
    });
    const commentsFieldTextArea: ReactWrapper = wrapper
      .find(Field)
      .filter({ name: "comments" })
      .find("textarea");
    commentsFieldTextArea.simulate("change", {
      target: {
        name: "comments",
        value: "This is a test of updating toe lines",
      },
    });

    const form: ReactWrapper = wrapper.find("Formik");
    form.at(0).simulate("submit");

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(handleCloseModal).toHaveBeenCalledTimes(1);
        expect(handleRefetchData).toHaveBeenCalledTimes(1);
        expect(msgSuccess).toHaveBeenCalledWith(
          "group.toe.lines.editModal.alerts.success",
          "groupAlerts.updatedTitle"
        );
      });
    });
  });
});
