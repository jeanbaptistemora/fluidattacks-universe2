import { MockedProvider, MockedResponse, wait } from "@apollo/react-testing";
import { mount, ReactWrapper } from "enzyme";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import store from "../../../../store";
import { updateAccessTokenModal as UpdateAccessTokenModal } from "./index";
import { GET_ACCESS_TOKEN } from "./queries";
import { IGetAccessTokenDictAttr } from "./types";

describe("Update access token modal", () => {
  const handleOnClose: jest.Mock = jest.fn();

  const accessToken: IGetAccessTokenDictAttr = {
    hasAccessToken: true,
    issuedAt: Date.now()
      .toString(),
  };

  const noAccessToken: IGetAccessTokenDictAttr = {
    hasAccessToken: false,
    issuedAt: "",
  };

  const mockQueryTrue: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: GET_ACCESS_TOKEN,
      },
      result: {
        data: {
          me: {
            accessToken: JSON.stringify(accessToken),
          },
        },
      },
    },
  ];

  const mockQueryFalse: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: GET_ACCESS_TOKEN,
      },
      result: {
        data: {
          me: {
            accessToken: JSON.stringify(noAccessToken),
          },
        },
      },
    },
  ];

  it("should return a function", () => {
    expect(typeof UpdateAccessTokenModal)
      .toEqual("function");
  });

  it("should render an add access token modal", async (): Promise<void> => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mockQueryFalse} addTypename={false}>
          <UpdateAccessTokenModal onClose={handleOnClose} open={true} />
        </MockedProvider>
      </Provider>,
    );

    await act(async () => {
      await wait(0);
      wrapper.update();
    });

    const componentTitle: ReactWrapper = wrapper.find("h4");

    const dateField: ReactWrapper = wrapper.find({ type: "date" })
      .find("input");

    const submitButton: ReactWrapper = wrapper
      .find("button")
      .filterWhere((element: ReactWrapper) => element.contains("Proceed") && element.prop("disabled") === false)
      .first();

    const closeButton: ReactWrapper = wrapper
      .find("button")
      .filterWhere((element: ReactWrapper) => element.contains("Close"))
      .first();
    closeButton.simulate("click");

    expect(wrapper)
      .toHaveLength(1);
    expect(componentTitle.text())
      .toBe("Update access token");
    expect(dateField)
      .toHaveLength(1);
    expect(submitButton)
      .toHaveLength(1);
    expect(handleOnClose)
      .toHaveBeenCalled();
  });

  it("should render a token creation date", async (): Promise<void> => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mockQueryTrue} addTypename={false}>
          <UpdateAccessTokenModal onClose={handleOnClose} open={true} />
        </MockedProvider>
      </Provider>,
    );

    await act(async () => {
      await wait(0);
      wrapper.update();
    });

    const tokenCreationLabel: ReactWrapper = wrapper.find("label");

    const submitButton: ReactWrapper = wrapper
      .find("button")
      .filterWhere((element: ReactWrapper) => element.contains("Proceed") && element.prop("disabled") === true)
      .first();

    const revokeButton: ReactWrapper = wrapper
      .find("button")
      .filterWhere((element: ReactWrapper) => element.contains("Revoke current token"))
      .first();

    expect(wrapper)
      .toHaveLength(1);
    expect(tokenCreationLabel.text())
      .toMatch(/Token created at:/);
    expect(submitButton)
      .toHaveLength(1);
    expect(revokeButton)
      .toHaveLength(1);
  }, 15000);
});
