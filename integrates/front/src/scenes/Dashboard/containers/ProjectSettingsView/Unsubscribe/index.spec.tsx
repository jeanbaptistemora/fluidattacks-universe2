import type { MockedResponse } from "@apollo/react-testing";
import { MockedProvider, wait } from "@apollo/react-testing";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { MemoryRouter, Route } from "react-router";
import { Field } from "redux-form";

import type { IUnsubscribeModalProps } from "./UnsubscribeModal";
import { UnsubscribeModal } from "./UnsubscribeModal";
import { UNSUBSCRIBE_FROM_GROUP_MUTATION } from "./UnsubscribeModal/queries";

import { Unsubscribe } from ".";
import { Button } from "components/Button";
import store from "store";
import { msgSuccess } from "utils/notifications";

jest.mock(
  "../../../../../utils/notifications",
  (): Dictionary => {
    const mockedNotifications: Dictionary<
      () => Dictionary
    > = jest.requireActual("../../../../../utils/notifications");
    jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

    return mockedNotifications;
  }
);

describe("Unsubscribe from group", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Unsubscribe).toStrictEqual("function");
  });

  it("should unsubscribe from a group", async (): Promise<void> => {
    expect.hasAssertions();

    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: UNSUBSCRIBE_FROM_GROUP_MUTATION,
          variables: {
            groupName: "test",
          },
        },
        result: { data: { unsubscribeFromGroup: { success: true } } },
      },
    ];
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/test"]}>
        <MockedProvider addTypename={true} mocks={mocksMutation}>
          <Provider store={store}>
            <Route component={Unsubscribe} path={"/:projectName"} />
          </Provider>
        </MockedProvider>
      </MemoryRouter>
    );

    const unsubscribeButton: ReactWrapper = wrapper.find(Button);
    unsubscribeButton.simulate("click");

    const unsubscribeModal: ReactWrapper<IUnsubscribeModalProps> = wrapper.find(
      UnsubscribeModal
    );
    const confirmationField: ReactWrapper = unsubscribeModal
      .find(Field)
      .filter({ name: "confirmation" })
      .find("input");
    confirmationField.simulate("change", { target: { value: "test" } });

    const proccedButton: ReactWrapper = wrapper
      .find(Button)
      .filterWhere((element: ReactWrapper): boolean =>
        element.text().includes("confirmmodal.proceed")
      );
    proccedButton.simulate("click");

    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );

    expect(msgSuccess).toHaveBeenCalledWith(
      "searchFindings.servicesTable.unsubscribe.success",
      "searchFindings.servicesTable.unsubscribe.successTitle"
    );
  });
});
