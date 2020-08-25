import { APITokenModal } from ".";
import { GraphQLError } from "graphql";
import { Provider } from "react-redux";
import React from "react";
import { act } from "react-dom/test-utils";
import moment from "moment";
import store from "../../../../store";
import waitForExpect from "wait-for-expect";
import { GET_ACCESS_TOKEN, UPDATE_ACCESS_TOKEN_MUTATION } from "./queries";
import { IGetAccessTokenDictAttr, IUpdateAccessTokenAttr } from "./types";
import { MockedProvider, MockedResponse, wait } from "@apollo/react-testing";
import { ReactWrapper, mount } from "enzyme";

describe("Update access token modal", (): void => {
  const handleOnClose: jest.Mock = jest.fn();

  const msToSec: number = 1000;
  const yyyymmdd: number = 10;

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof APITokenModal).toStrictEqual("function");
  });

  it("should render an add access token modal", async (): Promise<void> => {
    expect.hasAssertions();

    const noAccessToken: IGetAccessTokenDictAttr = {
      hasAccessToken: false,
      issuedAt: "",
    };
    const mockQueryFalse: MockedResponse[] = [
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
        <MockedProvider addTypename={false} mocks={mockQueryFalse}>
          <APITokenModal onClose={handleOnClose} open={true} />
        </MockedProvider>
      </Provider>
    );

    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );

    const componentTitle: ReactWrapper = wrapper.find("h4");

    const dateField: ReactWrapper = wrapper
      .find({ type: "date" })
      .find("input");

    const submitButton: ReactWrapper = wrapper
      .find("button")
      .filterWhere(
        (element: ReactWrapper): boolean =>
          element.contains("Proceed") && element.prop("disabled") === false
      )
      .first();

    const closeButton: ReactWrapper = wrapper
      .find("button")
      .filterWhere((element: ReactWrapper): boolean =>
        element.contains("Close")
      )
      .first();
    closeButton.simulate("click");

    expect(wrapper).toHaveLength(1);
    expect(componentTitle.text()).toBe("Update access token");
    expect(dateField).toHaveLength(1);
    expect(submitButton).toHaveLength(1);
    expect(handleOnClose).toHaveBeenCalledWith(expect.anything());
  });

  it("should render a token creation date", async (): Promise<void> => {
    expect.hasAssertions();

    const accessToken: IGetAccessTokenDictAttr = {
      hasAccessToken: true,
      issuedAt: Date.now().toString(),
    };
    const mockQueryTrue: MockedResponse[] = [
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
        <MockedProvider addTypename={false} mocks={mockQueryTrue}>
          <APITokenModal onClose={handleOnClose} open={true} />
        </MockedProvider>
      </Provider>
    );

    expect(wrapper).toHaveLength(1);

    await act(
      async (): Promise<void> => {
        await waitForExpect((): void => {
          wrapper.update();

          const tokenCreationLabel: ReactWrapper = wrapper.find("label");

          const submitButton: ReactWrapper = wrapper
            .find("button")
            .filterWhere(
              (element: ReactWrapper): boolean =>
                element.contains("Proceed") && element.prop("disabled") === true
            )
            .first();

          const revokeButton: ReactWrapper = wrapper
            .find("button")
            .filterWhere((element: ReactWrapper): boolean =>
              element.contains("Revoke current token")
            )
            .first();

          expect(wrapper).toHaveLength(1);
          expect(tokenCreationLabel.text()).toMatch(/Token created at:/u);
          expect(submitButton).toHaveLength(1);
          expect(revokeButton).toHaveLength(1);
        });
      }
    );
  });

  it("should render a new access token", async (): Promise<void> => {
    expect.hasAssertions();

    const expirationTime: string = moment()
      .add(1, "month")
      .toISOString()
      .substring(0, yyyymmdd);
    const updatedAccessToken: IUpdateAccessTokenAttr = {
      updateAccessToken: {
        sessionJwt: "dummyJwt",
        success: true,
      },
    };
    const noAccessToken: IGetAccessTokenDictAttr = {
      hasAccessToken: false,
      issuedAt: "",
    };
    const accessToken: IGetAccessTokenDictAttr = {
      hasAccessToken: true,
      issuedAt: Date.now().toString(),
    };
    const mockMutation: MockedResponse[] = [
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
      {
        request: {
          query: UPDATE_ACCESS_TOKEN_MUTATION,
          variables: {
            expirationTime: Math.floor(
              new Date(expirationTime).getTime() / msToSec
            ),
          },
        },
        result: {
          data: {
            ...updatedAccessToken,
          },
        },
      },
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
        <MockedProvider addTypename={false} mocks={mockMutation}>
          <APITokenModal onClose={handleOnClose} open={true} />
        </MockedProvider>
      </Provider>
    );

    const dateField: ReactWrapper = wrapper
      .find({ type: "date" })
      .find("input");
    dateField.simulate("change", { target: { value: expirationTime } });

    const form: ReactWrapper = wrapper.find("genericForm");
    form.simulate("submit");

    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );

    const newTokenLabel: ReactWrapper = wrapper
      .find("label")
      .filterWhere((element: ReactWrapper): boolean =>
        element.contains("Personal Access Token")
      );

    const copyTokenButton: ReactWrapper = wrapper
      .find("button")
      .filterWhere((element: ReactWrapper): boolean => element.contains("Copy"))
      .first();
    copyTokenButton.simulate("click");

    expect(wrapper).toHaveLength(1);
    expect(newTokenLabel).toHaveLength(1);
    expect(copyTokenButton).toHaveLength(1);
  });

  it("should reset the GenericForm component", async (): Promise<void> => {
    expect.hasAssertions();

    const expirationTime: string = moment()
      .add(1, "month")
      .toISOString()
      .substring(0, yyyymmdd);
    const mockMutationError: readonly MockedResponse[] = [
      {
        request: {
          query: UPDATE_ACCESS_TOKEN_MUTATION,
          variables: {
            expirationTime: Math.floor(
              new Date(expirationTime).getTime() / msToSec
            ),
          },
        },
        result: {
          errors: [new GraphQLError("Access denied")],
        },
      },
    ];

    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider addTypename={false} mocks={mockMutationError}>
          <APITokenModal onClose={handleOnClose} open={true} />
        </MockedProvider>
      </Provider>
    );

    const dateField: ReactWrapper = wrapper
      .find({ type: "date" })
      .find("input");
    dateField.simulate("change", { target: { value: expirationTime } });

    const form: ReactWrapper = wrapper.find("genericForm");
    form.simulate("submit");

    expect(wrapper).toHaveLength(1);
    expect(dateField.prop("value")).toBe(expirationTime);

    await act(
      async (): Promise<void> => {
        await waitForExpect((): void => {
          wrapper.update();

          const dateFieldOnReset: ReactWrapper = wrapper
            .find({ type: "date" })
            .find("input");

          expect(wrapper).toHaveLength(1);
          expect(dateFieldOnReset.prop("value")).toBe("");
        });
      }
    );
  });
});
