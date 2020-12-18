import { GET_VULNERABILITIES } from "scenes/Dashboard/components/Vulnerabilities/queries";
import { GraphQLError } from "graphql";
import { HANDLE_VULNS_ACCEPTATION } from "scenes/Dashboard/containers/VulnerabilitiesView/HandleAcceptationModal/queries";
import { HandleAcceptationModal } from "scenes/Dashboard/containers/VulnerabilitiesView/HandleAcceptationModal/index";
import { MockedProvider } from "@apollo/react-testing";
import type { MockedResponse } from "@apollo/react-testing";
import { Provider } from "react-redux";
import React from "react";
import type { ReactWrapper } from "enzyme";
import { act } from "react-dom/test-utils";
import { mount } from "enzyme";
import store from "store";
import waitForExpect from "wait-for-expect";
import { msgError, msgSuccess } from "utils/notifications";

jest.mock(
  "../../../../../utils/notifications",
  (): Dictionary => {
    const mockedNotifications: Dictionary<() => Dictionary> = jest.requireActual(
      "../../../../../utils/notifications"
    );
    jest.spyOn(mockedNotifications, "msgError").mockImplementation();
    jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

    return mockedNotifications;
  }
);

describe("handle vulns acceptation modal", (): void => {
  it("should handle vulns acceptation", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

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
        <MockedProvider addTypename={false} mocks={mocksMutation}>
          <HandleAcceptationModal
            findingId={"1"}
            handleCloseModal={handleOnClose}
            refetchData={handleRefetchData}
            vulns={[
              { acceptation: "APPROVED", id: "test", specific: "", where: "" },
            ]}
          />
        </MockedProvider>
      </Provider>
    );
    await act(
      async (): Promise<void> => {
        await waitForExpect((): void => {
          wrapper.update();

          expect(wrapper).toHaveLength(1);
        });
      }
    );
    const justification: ReactWrapper = wrapper.find("textarea");
    justification.simulate("change", {
      target: { value: "This is a justification test" },
    });
    const switchButton: ReactWrapper = wrapper
      .find("BootstrapTable")
      .find("e")
      .find("div")
      .first();
    switchButton.simulate("click");
    const form: ReactWrapper = wrapper.find("form");
    form.at(0).simulate("submit");

    await act(
      async (): Promise<void> => {
        await waitForExpect((): void => {
          wrapper.update();

          expect(msgSuccess).toHaveBeenCalledWith(
            "Indefinite acceptation has been handled",
            "Correct!"
          );
          expect(handleRefetchData).toHaveBeenCalledWith();
          expect(handleOnClose).toHaveBeenCalledWith();
        });
      }
    );
  });

  it("should handle vulns acceptation errors", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

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
            new GraphQLError(
              "Exception - It cant handle acceptation without being requested"
            ),
            new GraphQLError("Exception - Vulnerability not found"),
            new GraphQLError("Unexpected error"),
          ],
        },
      },
    ];
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider addTypename={false} mocks={mocksMutation}>
          <HandleAcceptationModal
            findingId={"1"}
            handleCloseModal={jest.fn()}
            refetchData={jest.fn()}
            vulns={[
              {
                acceptation: "APPROVED",
                id: "test_error",
                specific: "",
                where: "",
              },
            ]}
          />
        </MockedProvider>
      </Provider>
    );
    await act(
      async (): Promise<void> => {
        await waitForExpect((): void => {
          wrapper.update();

          expect(wrapper).toHaveLength(1);
        });
      }
    );
    const justification: ReactWrapper = wrapper.find("textarea");
    justification.simulate("change", {
      target: { value: "This is a justification test error" },
    });
    const form: ReactWrapper = wrapper.find("form");
    form.at(0).simulate("submit");
    await act(
      async (): Promise<void> => {
        await waitForExpect((): void => {
          wrapper.update();
          const expectedErrorMsgs: number = 3;

          expect(handleRefetchData).not.toHaveBeenCalled();
          expect(msgError).toHaveBeenCalledTimes(expectedErrorMsgs);
        });
      }
    );
  });
});
