import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";

import { ADD_TOE_INPUT, GET_ROOTS } from "./queries";

import { HandleAdditionModal } from ".";
import { authzPermissionsContext } from "utils/authz/config";
import { msgSuccess } from "utils/notifications";

jest.mock("../../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary<() => Dictionary> = jest.requireActual(
    "../../../../../utils/notifications"
  );
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

describe("handle toe inputs addition modal", (): void => {
  it("should handle input addition", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleRefetchData: jest.Mock = jest.fn();
    const handleCloseModal: jest.Mock = jest.fn();
    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: ADD_TOE_INPUT,
          variables: {
            component: "https://test.test.com/test/path",
            entryPoint: "-",
            groupName: "groupname",
            rootId: "4039d098-ffc5-4984-8ed3-eb17bca98e19",
          },
        },
        result: { data: { addToeInput: { success: true } } },
      },
    ];
    const queryMock: MockedResponse = {
      request: {
        query: GET_ROOTS,
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
                nickname: "product",
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
            refetchData={handleRefetchData}
          />
        </MockedProvider>
      </authzPermissionsContext.Provider>
    );

    await screen.findByPlaceholderText("group.toe.inputs.addModal.fields.path");
    userEvent.type(
      screen.getByPlaceholderText("group.toe.inputs.addModal.fields.path"),
      "test/path"
    );
    userEvent.type(screen.getAllByRole("textbox")[2], "-");
    userEvent.click(screen.getByText("group.toe.inputs.addModal.procced"));

    await waitFor((): void => {
      expect(handleCloseModal).toHaveBeenCalledTimes(1);
    });

    expect(handleRefetchData).toHaveBeenCalledTimes(1);
    expect(msgSuccess).toHaveBeenCalledWith(
      "group.toe.inputs.addModal.alerts.success",
      "groupAlerts.titleSuccess"
    );
  });
});
