import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { act } from "react-dom/test-utils";
import wait from "waait";
import waitForExpect from "wait-for-expect";

import { GlobalConfigModal } from "scenes/Dashboard/components/Navbar/UserProfile/GlobalConfigModal";
import {
  SUBSCRIBE_TO_ENTITY_REPORT,
  SUBSCRIPTIONS_TO_ENTITY_REPORT,
} from "scenes/Dashboard/components/Navbar/UserProfile/GlobalConfigModal/queries";

describe("Global configuration modal", (): void => {
  const handleOnClose: jest.Mock = jest.fn();

  const mockQueryFalse: MockedResponse = {
    request: {
      query: SUBSCRIPTIONS_TO_ENTITY_REPORT,
    },
    result: {
      data: {
        me: {
          subscriptionsToEntityReport: [],
          userEmail: "test@fluidattacks.com",
        },
      },
    },
  };
  const mockQueryTrue: MockedResponse = {
    request: {
      query: SUBSCRIPTIONS_TO_ENTITY_REPORT,
    },
    result: {
      data: {
        me: {
          subscriptionsToEntityReport: [
            { entity: "DIGEST", frequency: "DAILY", subject: "ALL_GROUPS" },
            { entity: "COMMENTS", frequency: "DAILY", subject: "ALL_GROUPS" },
          ],
          userEmail: "test@fluidattacks.com",
        },
      },
    },
  };

  const mockMutationDigest: MockedResponse = {
    request: {
      query: SUBSCRIBE_TO_ENTITY_REPORT,
      variables: {
        frequency: "DAILY",
        reportEntity: "DIGEST",
        reportSubject: "ALL_GROUPS",
      },
    },
    result: {
      data: {
        subscribeToEntityReport: {
          success: true,
        },
      },
    },
  };

  const mockMutationComments: MockedResponse = {
    request: {
      query: SUBSCRIBE_TO_ENTITY_REPORT,
      variables: {
        frequency: "DAILY",
        reportEntity: "COMMENTS",
        reportSubject: "ALL_GROUPS",
      },
    },
    result: {
      data: {
        subscribeToEntityReport: {
          success: true,
        },
      },
    },
  };

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GlobalConfigModal).toStrictEqual("function");
  });

  it("should render modal components", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MockedProvider addTypename={false} mocks={[mockQueryFalse]}>
        <GlobalConfigModal onClose={handleOnClose} open={true} />
      </MockedProvider>
    );

    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    const componentTitle: ReactWrapper = wrapper.find("h4");
    const confirmButton: ReactWrapper = wrapper.find("#config-confirm").first();
    const closeButton: ReactWrapper = wrapper.find("#config-close").first();

    closeButton.simulate("click");

    expect(wrapper).toHaveLength(1);
    expect(componentTitle.text()).toBe("Configuration");
    expect(confirmButton).toHaveLength(1);
    expect(confirmButton.prop("disabled")).toBe(true);
    expect(closeButton).toHaveLength(1);
    expect(handleOnClose).toHaveBeenCalledWith(expect.anything());
  });

  it("should render digest subscription option", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MockedProvider
        addTypename={false}
        mocks={[mockQueryTrue, mockMutationDigest]}
      >
        <GlobalConfigModal onClose={handleOnClose} open={true} />
      </MockedProvider>
    );

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        const configLabel: ReactWrapper = wrapper
          .find({
            id: "config-digest-label",
          })
          .first();

        expect(wrapper).toHaveLength(1);
        expect(configLabel).toHaveLength(1);
        expect(
          wrapper
            .find({
              name: "config-digest-switch",
            })
            .prop("checked")
        ).toBe(true);
        expect(wrapper.find("#config-confirm").first().prop("disabled")).toBe(
          true
        );
      });
    });

    wrapper
      .find({
        name: "config-digest-switch",
      })
      .simulate("click");
    wrapper.find("#config-confirm").first().simulate("click");
    wrapper.find("form").simulate("submit");

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper.find("#config-confirm").first().prop("disabled")).toBe(
          true
        );
      });
    });
  });

  it("should render comments subscription option", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MockedProvider
        addTypename={false}
        mocks={[mockQueryTrue, mockMutationComments]}
      >
        <GlobalConfigModal onClose={handleOnClose} open={true} />
      </MockedProvider>
    );

    await act(async (): Promise<void> => {
      const delay = 50;
      await wait(delay);
      wrapper.update();
    });

    const configLabel: ReactWrapper = wrapper
      .find({
        id: "config-comments-label",
      })
      .first();
    const configSwitch: ReactWrapper = wrapper.find({
      name: "config-comments-switch",
    });
    const confirmButton: ReactWrapper = wrapper.find("#config-confirm").first();

    expect(wrapper).toHaveLength(1);
    expect(configLabel).toHaveLength(1);
    expect(configSwitch.prop("checked")).toBe(true);
    expect(confirmButton.prop("disabled")).toBe(true);

    configSwitch.simulate("click");
    confirmButton.simulate("click");
    wrapper.find("form").simulate("submit");

    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    expect(confirmButton.prop("disabled")).toBe(true);
  });
});
