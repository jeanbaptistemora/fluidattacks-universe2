import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { mount, ReactWrapper } from "enzyme";
import { GraphQLError } from "graphql";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import store from "store";
import waitForExpect from "wait-for-expect";

import { GET_VULNERABILITIES } from "scenes/Dashboard/components/Vulnerabilities/queries";
import { HandleAcceptationModal } from "scenes/Dashboard/containers/VulnerabilitiesView/HandleAcceptationModal/index";
import {
  HANDLE_VULNS_ACCEPTATION,
} from "scenes/Dashboard/containers/VulnerabilitiesView/HandleAcceptationModal/queries";
import { msgError, msgSuccess } from "utils/notifications";

jest.mock("../../../../../utils/notifications", () => {
  const mockedNotifications: Dictionary = jest.requireActual("../../../../../utils/notifications");
  mockedNotifications.msgError = jest.fn();
  mockedNotifications.msgSuccess = jest.fn();

  return mockedNotifications;
});

describe("handle vulns acceptation modal", () => {
  afterEach(() => {
    jest.clearAllMocks();
  });
  it("should handle vulns acceptation", async () => {
    const handleOnClose: jest.Mock = jest.fn();
    const handleRefetchData: jest.Mock = jest.fn();
    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: HANDLE_VULNS_ACCEPTATION,
          variables: {
            acceptedVulns: [],
            findingId: "1",
            justification: "This is a justification test",
            rejectedVulns: ["test"],
          },
        },
        result: { data: { handleVulnsAcceptation: { success: true } } },
      },
      {
        request: {
          query: GET_VULNERABILITIES,
          variables: {
            analystField: false,
            identifier: "1",
          },
        },
        result: {
          data: {
            finding: {
              id: "1",
              inputsVulns: [],
              linesVulns: [],
              portsVulns: [],
              releaseDate: "",
            },
          },
        },
      },
    ];
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksMutation} addTypename={false}>
          <HandleAcceptationModal
            findingId={"1"}
            vulns={[{acceptation: "APPROVED", id: "test", specific: "", where: ""}]}
            refetchData={handleRefetchData}
            handleCloseModal={handleOnClose}
          />
        </MockedProvider>
      </Provider>,
    );
    await act(async () => {
      await waitForExpect(() => {
        wrapper.update();
        expect(wrapper)
          .toHaveLength(1);
      });
    });
    const justification: ReactWrapper = wrapper.find("textarea");
    justification.simulate("change", { target: { value: "This is a justification test" } });
    const switchButton: ReactWrapper = wrapper.find("BootstrapTable")
      .find("e")
      .find("div")
      .first();
    switchButton.simulate("click");
    const form: ReactWrapper = wrapper.find("form");
    form.at(0)
      .simulate("submit");

    await act(async () => {
      await waitForExpect(() => {
        wrapper.update();
        expect(msgSuccess)
          .toHaveBeenCalled();
        expect(handleRefetchData)
        .toHaveBeenCalled();
        expect(handleOnClose)
          .toHaveBeenCalled();
      });
    });
  });

  it("should handle vulns acceptation errors", async () => {
    const handleRefetchData: jest.Mock = jest.fn();
    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: HANDLE_VULNS_ACCEPTATION,
          variables: {
            acceptedVulns: ["test_error"],
            findingId: "1",
            justification: "This is a justification test error",
            rejectedVulns: [],
          },
        },
        result: {
          errors: [
            new GraphQLError("Exception - It cant handle acceptation without being requested"),
            new GraphQLError("Exception - Vulnerability not found"),
            new GraphQLError("Unexpected error"),
          ],
        },
      },
    ];
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksMutation} addTypename={false}>
          <HandleAcceptationModal
            findingId={"1"}
            vulns={[{acceptation: "APPROVED", id: "test_error", specific: "", where: ""}]}
            refetchData={jest.fn()}
            handleCloseModal={jest.fn()}
          />
        </MockedProvider>
      </Provider>,
    );
    await act(async () => {
      await waitForExpect(() => {
        wrapper.update();
        expect(wrapper)
          .toHaveLength(1);
      });
    });
    const justification: ReactWrapper = wrapper.find("textarea");
    justification.simulate("change", { target: { value: "This is a justification test error" } });
    const form: ReactWrapper = wrapper.find("form");
    form.at(0)
      .simulate("submit");
    await act(async () => {
      await waitForExpect(() => {
        wrapper.update();
        expect(handleRefetchData)
          .not
          .toHaveBeenCalled();
        expect(msgError)
          .toBeCalledTimes(3);
      });
    });
  });
});
