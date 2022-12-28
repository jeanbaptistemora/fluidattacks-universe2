import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";

import { ADD_TOE_LINES, GET_GIT_ROOTS } from "./queries";

import { HandleAdditionModal } from ".";
import { authzPermissionsContext } from "utils/authz/config";
import { msgSuccess } from "utils/notifications";

jest.mock(
  "../../../../../../../utils/notifications",
  (): Record<string, unknown> => {
    const mockedNotifications: Record<string, () => Record<string, unknown>> =
      jest.requireActual("../../../../../../../utils/notifications");
    jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

    return mockedNotifications;
  }
);

describe("handle toe lines addition modal", (): void => {
  it("should handle lines addition", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleRefetchData: jest.Mock = jest.fn();
    const handleCloseModal: jest.Mock = jest.fn();
    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: ADD_TOE_LINES,
          variables: {
            filename: "test/filename.py",
            groupName: "groupname",
            lastAuthor: "test@test.com",
            lastCommit: "2fab76140221397cabbc0eae536b41ff38e7540a",
            loc: 10,
            modifiedDate: "2022-05-23T07:18:00.000Z",
            rootId: "4039d098-ffc5-4984-8ed3-eb17bca98e19",
          },
        },
        result: { data: { addToeLines: { success: true } } },
      },
    ];
    const queryMock: MockedResponse = {
      request: {
        query: GET_GIT_ROOTS,
        variables: { groupName: "groupname" },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            name: "test",
            roots: [
              {
                __typename: "GitRoot",
                environmentUrls: ["https://test.test.com"],
                id: "4039d098-ffc5-4984-8ed3-eb17bca98e19",
                nickname: "universe",
                state: "ACTIVE",
              },
            ],
          },
        },
      },
    };

    render(
      <authzPermissionsContext.Provider value={new PureAbility([])}>
        <MockedProvider
          addTypename={false}
          mocks={[...mocksMutation, queryMock]}
        >
          <HandleAdditionModal
            groupName={"groupname"}
            handleCloseModal={handleCloseModal}
            isAdding={true}
            refetchData={handleRefetchData}
          />
        </MockedProvider>
      </authzPermissionsContext.Provider>
    );

    await screen.findByText("group.toe.lines.addModal.title");

    fireEvent.change(screen.getByPlaceholderText("mm/dd/yyyy hh:mm (a|p)m"), {
      target: { value: "" },
    });

    // 05/23/2022 07:18 AM
    await userEvent.type(
      screen.getByPlaceholderText("mm/dd/yyyy hh:mm (a|p)m"),
      "052320220718A"
    );

    await userEvent.type(
      screen.getByRole("textbox", { name: "filename" }),
      "test/filename.py"
    );
    await userEvent.type(screen.getByRole("spinbutton", { name: "loc" }), "10");
    await userEvent.type(
      screen.getByRole("textbox", { name: "lastAuthor" }),
      "test@test.com"
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "lastCommit" }),
      "2fab76140221397cabbc0eae536b41ff38e7540a"
    );

    await userEvent.click(screen.getByText("components.modal.confirm"));

    await waitFor((): void => {
      expect(handleCloseModal).toHaveBeenCalledTimes(1);
      expect(handleRefetchData).toHaveBeenCalledTimes(1);
      expect(msgSuccess).toHaveBeenCalledWith(
        "group.toe.lines.addModal.alerts.success",
        "groupAlerts.titleSuccess"
      );
    });
  });
});
