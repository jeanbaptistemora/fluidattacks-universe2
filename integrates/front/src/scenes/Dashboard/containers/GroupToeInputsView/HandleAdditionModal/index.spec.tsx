import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import { Field } from "formik";
import React from "react";
import { act } from "react-dom/test-utils";
import wait from "waait";
import waitForExpect from "wait-for-expect";

import { ADD_TOE_INPUT, GET_ROOTS } from "./queries";

import { HandleAdditionModal } from ".";
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

    const wrapper: ReactWrapper = mount(
      <MockedProvider addTypename={false} mocks={[...mocksMutation, queryMock]}>
        <HandleAdditionModal
          groupName={"groupname"}
          handleCloseModal={handleCloseModal}
          refetchData={handleRefetchData}
        />
      </MockedProvider>,
      {
        wrappingComponent: authzPermissionsContext.Provider,
      }
    );

    await act(async (): Promise<void> => {
      await wait(0);

      wrapper.update();
    });

    const componentFieldInput: ReactWrapper = wrapper
      .find(Field)
      .filter({ name: "path" })
      .find("input");
    componentFieldInput.simulate("change", {
      target: {
        name: "path",
        value: "test/path",
      },
    });
    const entryPointFieldInput: ReactWrapper = wrapper
      .find(Field)
      .filter({ name: "entryPoint" })
      .find("input");
    entryPointFieldInput.simulate("change", {
      target: {
        name: "entryPoint",
        value: "-",
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
          "group.toe.inputs.addModal.alerts.success",
          "groupAlerts.titleSuccess"
        );
      });
    });
  });
});
