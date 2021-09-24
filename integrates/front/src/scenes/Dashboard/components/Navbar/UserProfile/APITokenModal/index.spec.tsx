import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import moment from "moment";
import React from "react";
import { act } from "react-dom/test-utils";
import wait from "waait";
import waitForExpect from "wait-for-expect";

import { APITokenModal } from "scenes/Dashboard/components/Navbar/UserProfile/APITokenModal";
import {
  GET_ACCESS_TOKEN,
  UPDATE_ACCESS_TOKEN_MUTATION,
} from "scenes/Dashboard/components/Navbar/UserProfile/APITokenModal/queries";
import type {
  IGetAccessTokenDictAttr,
  IUpdateAccessTokenAttr,
} from "scenes/Dashboard/components/Navbar/UserProfile/APITokenModal/types";

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
              userEmail: "test@fluidattacks.com",
            },
          },
        },
      },
    ];

    const wrapper: ReactWrapper = mount(
      <MockedProvider addTypename={false} mocks={mockQueryFalse}>
        <APITokenModal onClose={handleOnClose} open={true} />
      </MockedProvider>
    );

    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

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
              userEmail: "test@fluidattacks.com",
            },
          },
        },
      },
    ];

    const wrapper: ReactWrapper = mount(
      <MockedProvider addTypename={false} mocks={mockQueryTrue}>
        <APITokenModal onClose={handleOnClose} open={true} />
      </MockedProvider>
    );

    expect(wrapper).toHaveLength(1);

    await act(async (): Promise<void> => {
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
    });
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
              userEmail: "test@fluidattacks.com",
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
              userEmail: "test@fluidattacks.com",
            },
          },
        },
      },
    ];

    const wrapper: ReactWrapper = mount(
      <MockedProvider addTypename={false} mocks={mockMutation}>
        <APITokenModal onClose={handleOnClose} open={true} />
      </MockedProvider>
    );

    const dateField: ReactWrapper = wrapper
      .find({ name: "expirationTime" })
      .find("input");
    dateField.simulate("change", {
      target: { name: "expirationTime", value: expirationTime },
    });

    const form: ReactWrapper = wrapper.find("Formik");
    form.simulate("submit");

    await act(async (): Promise<void> => {
      const delay = 200;
      await wait(delay);
      wrapper.update();
    });

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
});
