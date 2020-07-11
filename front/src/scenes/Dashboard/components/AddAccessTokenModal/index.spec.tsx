import { MockedProvider, MockedResponse, wait } from "@apollo/react-testing";
import { mount, ReactWrapper } from "enzyme";
import { GraphQLError } from "graphql";
import moment from "moment";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import waitForExpect from "wait-for-expect";
import store from "../../../../store";
import { updateAccessTokenModal as UpdateAccessTokenModal } from "./index";
import { GET_ACCESS_TOKEN, UPDATE_ACCESS_TOKEN_MUTATION } from "./queries";
import { IGetAccessTokenDictAttr, IUpdateAccessTokenAttr } from "./types";

describe("Update access token modal", () => {
  const handleOnClose: jest.Mock = jest.fn();
  const expirationTime: string = moment()
    .add(30, "days")
    .toISOString()
    .substring(0, 10);

  it("should return a function", () => {
    expect(typeof UpdateAccessTokenModal)
      .toEqual("function");
  });

  it("should render an add access token modal", async (): Promise<void> => {
    const noAccessToken: IGetAccessTokenDictAttr = {
      hasAccessToken: false,
      issuedAt: "",
    };

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
    const accessToken: IGetAccessTokenDictAttr = {
      hasAccessToken: true,
      issuedAt: Date.now()
        .toString(),
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

    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mockQueryTrue} addTypename={false}>
          <UpdateAccessTokenModal onClose={handleOnClose} open={true} />
        </MockedProvider>
      </Provider>,
    );

    expect(wrapper)
      .toHaveLength(1);

    await act(async () => {
      await waitForExpect(() => {
        wrapper.update();

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
      });
    });
  });

  it("should render a new access token", async (): Promise<void> => {
    const updatedAccessToken: IUpdateAccessTokenAttr = {
      updateAccessToken: {
        sessionJwt: "dummyJwt",
        success: true,
      },
    };

    const mockMutation: MockedResponse[] = [
      {
        request: {
          query: UPDATE_ACCESS_TOKEN_MUTATION,
          variables: {
            expirationTime: Math.floor(new Date(expirationTime).getTime() / 1000),
          },
        },
        result: {
          data: {
            ...updatedAccessToken,
          },
        },
      },
    ];

    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mockMutation} addTypename={false}>
          <UpdateAccessTokenModal onClose={handleOnClose} open={true} />
        </MockedProvider>
      </Provider>,
    );

    const dateField: ReactWrapper = wrapper
      .find({ type: "date" })
      .find("input");
    dateField.simulate("change", { target: { value: expirationTime } });

    const form: ReactWrapper = wrapper.find("genericForm");
    form.simulate("submit");

    await act(async () => {
      await wait(0);
      wrapper.update();
    });

    const newTokenLabel: ReactWrapper = wrapper
      .find("label")
      .filterWhere((element: ReactWrapper) => element.contains("Personal Access Token"));

    const copyTokenButton: ReactWrapper = wrapper
      .find("button")
      .filterWhere((element: ReactWrapper) => element.contains("Copy"))
      .first();
    copyTokenButton.simulate("click");

    expect(wrapper)
      .toHaveLength(1);
    expect(newTokenLabel)
      .toHaveLength(1);
    expect(copyTokenButton)
      .toHaveLength(1);
  });

  it("should reset the GenericForm component", async (): Promise<void> => {
    const mockMutationError: ReadonlyArray<MockedResponse> = [
      {
        request: {
          query: UPDATE_ACCESS_TOKEN_MUTATION,
          variables: {
            expirationTime: Math.floor(new Date(expirationTime).getTime() / 1000),
          },
        },
        result: {
          errors: [new GraphQLError("Access denied")],
        },
      },
    ];

    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mockMutationError} addTypename={false}>
          <UpdateAccessTokenModal onClose={handleOnClose} open={true} />
        </MockedProvider>
      </Provider>,
    );

    const dateField: ReactWrapper = wrapper
      .find({ type: "date" })
      .find("input");
    dateField.simulate("change", { target: { value: expirationTime } });

    const form: ReactWrapper = wrapper.find("genericForm");
    form.simulate("submit");

    expect(wrapper)
      .toHaveLength(1);
    expect(dateField.prop("value"))
      .toBe(expirationTime);

    await act(async () => {
      await waitForExpect(() => {
        wrapper.update();

        const dateFieldOnReset: ReactWrapper = wrapper
          .find({ type: "date" })
          .find("input");

        expect(wrapper)
          .toHaveLength(1);
        expect(dateFieldOnReset.prop("value"))
          .toBe("");
      });
    });
  });
});
