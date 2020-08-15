import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { mount, ReactWrapper } from "enzyme";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import waitForExpect from "wait-for-expect";
import store from "../../../../store";
import { AddOrganizationModal } from "./index";
import { CREATE_NEW_ORGANIZATION, GET_AVAILABLE_ORGANIZATION_NAME } from "./queries";
import { IAddOrganizationModalProps } from "./types";

const mockCloseModal: jest.Mock = jest.fn();
const mockHistoryPush: jest.Mock = jest.fn();
jest.mock("react-router-dom", (): Dictionary => {
  const mockedRouter: Dictionary<() => Dictionary> = jest.requireActual("react-router-dom");

  return {
    ...mockedRouter,
    useHistory: (): Dictionary => ({
      ...mockedRouter.useHistory(),
      push: mockHistoryPush,
    }),
  };
});

describe("Add organization modal", () => {
  const mockProps: IAddOrganizationModalProps = {
    onClose: mockCloseModal,
    open: true,
  };

  it("should return a function", () => {
    expect(typeof AddOrganizationModal)
      .toEqual("function");
  });

  it("should render component", async () => {
    const mocks: ReadonlyArray<MockedResponse> = [
      {
        request: {
          query: GET_AVAILABLE_ORGANIZATION_NAME,
        },
        result: {
          data: {
            internalNames: {
              name: "ESDEATH",
            },
          },
        },
      },
    ];
    const wrapper: ReactWrapper = mount(
      <Provider store={store} >
        <MockedProvider mocks={mocks} addTypename={false}>
          <AddOrganizationModal {...mockProps} />
        </MockedProvider>
      </Provider>,
    );

    await act(async () => {
      await waitForExpect(() => {
        wrapper.update();

        expect(wrapper)
          .toHaveLength(1);
        expect(
          wrapper
            .find({ name: "name" })
            .find("input")
            .prop("value"))
          .toBe("ESDEATH");
      });
    });

    expect(
      wrapper
        .find({ name: "name" })
        .find("input")
        .prop("disabled"))
        .toBe(true);

    const cancelButton: ReactWrapper = wrapper
      .find("button")
      .filterWhere((element: ReactWrapper) => element.contains("Cancel"))
      .first();

    cancelButton.simulate("click");

    expect(mockCloseModal)
      .toHaveBeenCalled();
  });

  it("should create an organization", async () => {
    const mocks: ReadonlyArray<MockedResponse> = [
      {
        request: {
          query: GET_AVAILABLE_ORGANIZATION_NAME,
        },
        result: {
          data: {
            internalNames: {
              name: "ESDEATH",
            },
          },
        },
      },
      {
        request: {
          query: CREATE_NEW_ORGANIZATION,
          variables: {
            name: "ESDEATH",
          },
        },
        result: {
          data: {
            createOrganization: {
              organization: {
                id: "ORG#eb50af04-4d50-4e40-bab1-a3fe9f672f9d",
                name: "esdeath",
              },
              success: true,
            },
          },
        },
      },
    ];
    const wrapper: ReactWrapper = mount(
      <Provider store={store} >
        <MockedProvider mocks={mocks} addTypename={false}>
          <AddOrganizationModal {...mockProps} />
        </MockedProvider>
      </Provider>,
    );

    await act(async () => {
      await waitForExpect(() => {
        wrapper.update();

        expect(wrapper)
          .toHaveLength(1);
        expect(
          wrapper
            .find({ name: "name" })
            .find("input")
            .prop("value"))
          .toBe("ESDEATH");
      });
    });

    wrapper
      .find("genericForm")
      .simulate("submit");

    await act(async () => {
      await waitForExpect(() => {
        wrapper.update();

        expect(mockCloseModal)
          .toHaveBeenCalled();
        expect(mockHistoryPush)
          .toHaveBeenCalledWith("/orgs/esdeath/");
      });
    });
  });
});
