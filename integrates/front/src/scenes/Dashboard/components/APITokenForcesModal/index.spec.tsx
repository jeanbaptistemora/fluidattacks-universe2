import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { act } from "react-dom/test-utils";
import wait from "waait";
import waitForExpect from "wait-for-expect";

import { APITokenForcesModal } from "scenes/Dashboard/components/APITokenForcesModal";
import {
  GET_FORCES_TOKEN,
  UPDATE_FORCES_TOKEN_MUTATION,
} from "scenes/Dashboard/components/APITokenForcesModal/queries";

describe("Update access token modal", (): void => {
  const handleOnClose: jest.Mock = jest.fn();

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof APITokenForcesModal).toStrictEqual("function");
  });

  it("should render an token modal with token and reset", async (): Promise<void> => {
    expect.hasAssertions();

    const beforeValue: string = "before value";
    const afterValue: string = "after value";
    const mockQueryFull: MockedResponse[] = [
      {
        request: {
          query: GET_FORCES_TOKEN,
          variables: {
            groupName: "unittesting",
          },
        },
        result: {
          data: {
            group: {
              forcesToken: beforeValue,
              name: "unittesting",
            },
          },
        },
      },
      {
        request: {
          query: UPDATE_FORCES_TOKEN_MUTATION,
          variables: {
            groupName: "unittesting",
          },
        },
        result: {
          data: {
            updateForcesAccessToken: {
              sessionJwt: afterValue,
              success: true,
            },
          },
        },
      },
      {
        request: {
          query: GET_FORCES_TOKEN,
          variables: {
            groupName: "unittesting",
          },
        },
        result: {
          data: {
            group: {
              forcesToken: afterValue,
              name: "unittesting",
            },
          },
        },
      },
    ];
    const wrapper: ReactWrapper = mount(
      <MockedProvider addTypename={false} mocks={mockQueryFull}>
        <APITokenForcesModal
          groupName={"unittesting"}
          onClose={handleOnClose}
          open={true}
        />
      </MockedProvider>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    const revealButton: ReactWrapper = wrapper
      .find("button")
      .filterWhere((element: ReactWrapper): boolean =>
        element.contains("Reveal Token")
      )
      .first();

    revealButton.simulate("click");

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(revealButton.prop("disabled")).toBe(false);

        const tokenTextAreaBefore: ReactWrapper = wrapper
          .find("textarea")
          .first();

        expect(tokenTextAreaBefore.text()).toBe(beforeValue);

        const resetButton: ReactWrapper = wrapper
          .find("button")
          .filterWhere((element: ReactWrapper): boolean =>
            element.contains("Reset")
          )
          .first();

        expect(resetButton.prop("disabled")).toBe(false);
      });
    });

    const form: ReactWrapper = wrapper.find("Formik");
    form.simulate("submit");

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();
        const tokenTextAreaAfter: ReactWrapper = wrapper
          .find("textarea")
          .first();

        expect(tokenTextAreaAfter.text()).toBe(afterValue);
      });
    });
  });

  it("should render an token modal with token", async (): Promise<void> => {
    expect.hasAssertions();

    const tokenValue: string = "some value";
    const mockQueryFull: MockedResponse[] = [
      {
        request: {
          query: GET_FORCES_TOKEN,
          variables: {
            groupName: "unnittesting",
          },
        },
        result: {
          data: {
            group: {
              forcesToken: tokenValue,
              name: "unnittesting",
            },
          },
        },
      },
    ];
    const wrapper: ReactWrapper = mount(
      <MockedProvider addTypename={false} mocks={mockQueryFull}>
        <APITokenForcesModal
          groupName={"unnittesting"}
          onClose={handleOnClose}
          open={true}
        />
      </MockedProvider>
    );

    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    const revealButton: ReactWrapper = wrapper
      .find("button")
      .filterWhere((element: ReactWrapper): boolean =>
        element.contains("Reveal Token")
      )
      .first();

    revealButton.simulate("click");
    await act(async (): Promise<void> => {
      const delay = 50;
      await wait(delay);
      wrapper.update();
    });

    expect(revealButton.prop("disabled")).toBe(false);

    const copyButton: ReactWrapper = wrapper
      .find("button")
      .filterWhere((element: ReactWrapper): boolean => element.contains("Copy"))
      .first();

    expect(copyButton.prop("disabled")).toBe(false);

    const resetButton: ReactWrapper = wrapper
      .find("button")
      .filterWhere((element: ReactWrapper): boolean =>
        element.contains("Reset")
      )
      .first();

    expect(resetButton.prop("disabled")).toBe(false);

    const tokenTextArea: ReactWrapper = wrapper.find("textarea").first();

    expect(tokenTextArea.text()).toBe(tokenValue);
  });

  it("should render an token modal without token", async (): Promise<void> => {
    expect.hasAssertions();

    const mockQueryNull: MockedResponse[] = [
      {
        request: {
          query: GET_FORCES_TOKEN,
          variables: {
            groupName: "unnittesting",
          },
        },
        result: {
          data: {
            group: {
              forcesToken: null,
              name: "unnittesting",
            },
          },
        },
      },
    ];

    const wrapper: ReactWrapper = mount(
      <MockedProvider addTypename={false} mocks={mockQueryNull}>
        <APITokenForcesModal
          groupName={"unnittesting"}
          onClose={handleOnClose}
          open={true}
        />
      </MockedProvider>
    );

    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    const componentTitle: ReactWrapper = wrapper.find("h4");

    const revealButton: ReactWrapper = wrapper
      .find("button")
      .filterWhere((element: ReactWrapper): boolean =>
        element.contains("Reveal Token")
      )
      .first();

    const closeButton: ReactWrapper = wrapper
      .find("button")
      .filterWhere((element: ReactWrapper): boolean =>
        element.contains("Close")
      )
      .first();

    revealButton.simulate("click");

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();
        const generateButton: ReactWrapper = wrapper
          .find("button")
          .filterWhere((element: ReactWrapper): boolean =>
            element.contains("Generate")
          )
          .first();
        const copyButton: ReactWrapper = wrapper
          .find("button")
          .filterWhere((element: ReactWrapper): boolean =>
            element.contains("Copy")
          )
          .first();
        const revealButtonAfter: ReactWrapper = wrapper
          .find("button")
          .filterWhere((element: ReactWrapper): boolean =>
            element.contains("Reveal Token")
          )
          .first();

        // When the token is revealed and does not exist, it cannot be copied
        expect(copyButton.prop("disabled")).toBe(true);
        expect(generateButton.prop("disabled")).toBe(false);
        expect(revealButtonAfter.prop("disabled")).toBe(true);
      });
    });

    closeButton.simulate("click");

    expect(wrapper).toHaveLength(1);
    expect(componentTitle.text()).toBe("Manage DevSecOps token");
    expect(revealButton).toHaveLength(1);
    expect(handleOnClose).toHaveBeenCalledWith(expect.anything());
  });
});
