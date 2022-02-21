import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { act } from "react-dom/test-utils";
import waitForExpect from "wait-for-expect";

import { UPDATE_TOE_INPUT } from "./queries";

import { HandleEditionModal } from ".";
import type { IToeInputData } from "../types";
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

describe("handle toe input edition modal", (): void => {
  it("should handle input edition", async (): Promise<void> => {
    expect.hasAssertions();

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
        markedRootNickname: "nickname",
        markedSeenFirstTimeBy: "test1@test.com",
        seenAt: new Date("2020-02-01T15:41:04+00:00"),
        seenFirstTimeBy: "test1@test.com",
        unreliableRootNickname: "nickname",
      },
    ];

    const wrapper: ReactWrapper = mount(
      <MockedProvider addTypename={false} mocks={[...mocksMutation]}>
        <HandleEditionModal
          groupName={"groupname"}
          handleCloseModal={handleCloseModal}
          refetchData={handleRefetchData}
          selectedToeInputDatas={mokedToeInputs}
          setSelectedToeInputDatas={jest.fn()}
        />
      </MockedProvider>,
      {
        wrappingComponent: authzPermissionsContext.Provider,
      }
    );

    const form: ReactWrapper = wrapper.find("Formik");
    form.at(0).simulate("submit");

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(handleCloseModal).toHaveBeenCalledTimes(1);
        expect(handleRefetchData).toHaveBeenCalledTimes(1);
        expect(msgSuccess).toHaveBeenCalledWith(
          "group.toe.inputs.editModal.alerts.success",
          "groupAlerts.updatedTitle"
        );
      });
    });
  });
});
