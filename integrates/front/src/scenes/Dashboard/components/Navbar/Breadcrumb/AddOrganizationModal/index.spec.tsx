import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { act } from "react-dom/test-utils";
import waitForExpect from "wait-for-expect";

import { AddOrganizationModal } from "scenes/Dashboard/components/Navbar/Breadcrumb/AddOrganizationModal";
import {
  CREATE_NEW_ORGANIZATION,
  GET_AVAILABLE_ORGANIZATION_NAME,
} from "scenes/Dashboard/components/Navbar/Breadcrumb/AddOrganizationModal/queries";

const handleCloseModal: jest.Mock = jest.fn();
const mockHistoryPush: jest.Mock = jest.fn();
jest.mock("react-router-dom", (): Dictionary => {
  const mockedRouter: Dictionary<() => Dictionary> =
    jest.requireActual("react-router-dom");

  return {
    ...mockedRouter,
    useHistory: (): Dictionary => ({
      ...mockedRouter.useHistory(),
      push: mockHistoryPush,
    }),
  };
});

describe("Add organization modal", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof AddOrganizationModal).toStrictEqual("function");
  });

  it("should render component", async (): Promise<void> => {
    expect.hasAssertions();

    const mocks: MockedResponse[] = [
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
      <MockedProvider addTypename={false} mocks={mocks}>
        <AddOrganizationModal onClose={handleCloseModal} open={true} />
      </MockedProvider>
    );

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper).toHaveLength(1);
        expect(wrapper.find("Formik").find("input").prop("value")).toBe(
          "ESDEATH"
        );
      });
    });

    expect(wrapper.find({ name: "name" }).find("input").prop("disabled")).toBe(
      true
    );

    const cancelButton: ReactWrapper = wrapper
      .find("button")
      .filterWhere((element: ReactWrapper): boolean =>
        element.contains("Cancel")
      )
      .first();

    cancelButton.simulate("click");

    expect(handleCloseModal).toHaveBeenCalledWith(expect.anything());
  });

  it("should create an organization", async (): Promise<void> => {
    expect.hasAssertions();

    const mocks: MockedResponse[] = [
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
      <MockedProvider addTypename={false} mocks={mocks}>
        <AddOrganizationModal onClose={handleCloseModal} open={true} />
      </MockedProvider>
    );

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper).toHaveLength(1);
        expect(wrapper.find({ name: "name" }).find("input").prop("value")).toBe(
          "ESDEATH"
        );
      });
    });

    wrapper.find("Formik").simulate("submit");

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(handleCloseModal).toHaveBeenCalledWith(expect.anything());
        expect(mockHistoryPush).toHaveBeenCalledWith("/orgs/esdeath/");
      });
    });
  });
});
