import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { shallow, ShallowWrapper } from "enzyme";
import { GraphQLError } from "graphql";
import React from "react";
import { Provider } from "react-redux";
import { Action, createStore, Store } from "redux";
import { IAddAccessTokenModalProps, updateAccessTokenModal as UpdateAccessTokenModal } from "./index";
import { GET_ACCESS_TOKEN } from "./queries";
import { IGetAccessTokenDictAttr } from "./types";

const functionMock: (() => void) = (): void => undefined;

describe("Update access token modal", () => {

  const mockProps: IAddAccessTokenModalProps = {
    onClose: functionMock,
    open: true,
  };

  const store: Store<{}, Action<{}>> = createStore(() => ({}));

  const accessToken: IGetAccessTokenDictAttr = {
    hasAccessToken: true,
    issuedAt: Date.now(),
  };

  const mocks: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: GET_ACCESS_TOKEN,
      },
      result: {
        data: {
            me: {
            __typename: "Me",
            accessToken: JSON.stringify(accessToken),
          },
        },
      },
  }];

  const mockError: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: GET_ACCESS_TOKEN,
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
  }];

  it("should return a function", () => {
    expect(typeof (UpdateAccessTokenModal))
      .toEqual("function");
  });

  it("should render an error in component", (): void => {
    const wrapper: ShallowWrapper = shallow(
      <Provider store={store}>
        <MockedProvider mocks={mockError} addTypename={true}>
          <UpdateAccessTokenModal {...mockProps} />
        </MockedProvider>
      </Provider>,
    );

    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render an add component", (): void => {
    const wrapper: ShallowWrapper = shallow(
      <Provider store={store}>
        <MockedProvider mocks={mocks} addTypename={true}>
          <UpdateAccessTokenModal {...mockProps} />
        </MockedProvider>
      </Provider>,
    );

    expect(wrapper)
      .toHaveLength(1);
  });
});
