import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import { reset } from "mixpanel-browser";
import React from "react";
import { act } from "react-dom/test-utils";
import { useTranslation } from "react-i18next";
import { MemoryRouter } from "react-router-dom";
import waitForExpect from "wait-for-expect";

import { DropdownButton, NavbarButton } from "../styles";
import { Modal } from "components/Modal";
import { UserProfile } from "scenes/Dashboard/components/Navbar/UserProfile/index";
import { REMOVE_STAKEHOLDER_MUTATION } from "scenes/Dashboard/components/Navbar/UserProfile/queries";

jest.mock("mixpanel-browser", (): Dictionary => {
  const mockedMixPanel: Dictionary<() => Dictionary> =
    jest.requireActual("mixpanel-browser");
  jest.spyOn(mockedMixPanel, "reset").mockImplementation();

  return mockedMixPanel;
});

describe("User Profile", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof UserProfile).toStrictEqual("function");
  });

  it("should render an delete account modal", async (): Promise<void> => {
    expect.hasAssertions();

    const { t } = useTranslation();
    const mockQueryFalse: MockedResponse[] = [
      {
        request: {
          query: REMOVE_STAKEHOLDER_MUTATION,
        },
        result: {
          data: {
            removeStakeholder: {
              success: true,
            },
          },
        },
      },
    ];

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/okada"]}>
        <MockedProvider addTypename={false} mocks={mockQueryFalse}>
          <UserProfile userRole={"customer"} />
        </MockedProvider>
      </MemoryRouter>
    );

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper).toHaveLength(1);
        expect(wrapper.find(DropdownButton)).toHaveLength(0);
      });
    });

    const navbarButton: ReactWrapper = wrapper.find(NavbarButton).first();
    const NUMBER_OF_DROPDOWN_BUTTONS: number = 5;
    navbarButton.simulate("click");

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper).toHaveLength(1);
        expect(wrapper.find(DropdownButton)).toHaveLength(
          NUMBER_OF_DROPDOWN_BUTTONS
        );
        expect(wrapper.find(Modal).first().prop("open")).toBe(false);
      });
    });

    const deleteAccountDropdown: ReactWrapper = wrapper
      .find("button")
      .filterWhere((element: ReactWrapper): boolean =>
        element.contains(t("navbar.deleteAccount.text").toString())
      )
      .first();

    deleteAccountDropdown.simulate("click");

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper).toHaveLength(1);
        expect(
          wrapper
            .find("Modal")
            .filterWhere((element: ReactWrapper): boolean =>
              element.contains(t("navbar.deleteAccount.text").toString())
            )
            .first()
            .prop("open")
        ).toBe(true);
      });
    });

    const proceedButton: ReactWrapper = wrapper
      .find("button")
      .filterWhere((element: ReactWrapper): boolean =>
        element.contains("Proceed")
      )
      .first();

    proceedButton.simulate("click");

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper).toHaveLength(1);
        expect(reset).toHaveBeenCalledTimes(1);
      });
    });

    jest.clearAllMocks();
  });
});
