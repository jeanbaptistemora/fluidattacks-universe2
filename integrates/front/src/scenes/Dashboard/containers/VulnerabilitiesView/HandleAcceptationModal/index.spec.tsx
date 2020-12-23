import { GET_FINDING_VULN_INFO } from "scenes/Dashboard/containers/VulnerabilitiesView/queries";
import { GraphQLError } from "graphql";
import { HANDLE_VULNS_ACCEPTATION } from "scenes/Dashboard/containers/VulnerabilitiesView/HandleAcceptationModal/queries";
import { HandleAcceptationModal } from "scenes/Dashboard/containers/VulnerabilitiesView/HandleAcceptationModal/index";
import type { IVulnerabilities } from "../types";
import { MockedProvider } from "@apollo/react-testing";
import type { MockedResponse } from "@apollo/react-testing";
import { Provider } from "react-redux";
import { PureAbility } from "@casl/ability";
import React from "react";
import type { ReactWrapper } from "enzyme";
import { act } from "react-dom/test-utils";
import { authzPermissionsContext } from "utils/authz/config";
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
    const mockedPermissions: PureAbility<string> = new PureAbility([
      {
        action: "backend_api_mutations_handle_vulns_acceptation_mutate",
      },
    ]);
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
          query: GET_FINDING_VULN_INFO,
          variables: {
            findingId: "1",
            groupName: "",
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
    const mokedVulns: IVulnerabilities[] = [
      {
        historicTreatment: [
          {
            acceptanceDate: "",
            acceptanceStatus: "SUBMITTED",
            date: "2019-07-05 09:56:40",
            justification: "test justification",
            treatment: "ACCEPTED_UNDEFINED",
            treatmentManager: "treatment-manager-1",
            user: "user@test.com",
          },
        ],
        id: "test",
        specific: "",
        where: "",
        zeroRisk: "Requested",
      },
    ];
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider addTypename={false} mocks={mocksMutation}>
          <HandleAcceptationModal
            findingId={"1"}
            groupName={""}
            handleCloseModal={handleOnClose}
            refetchData={handleRefetchData}
            vulns={mokedVulns}
          />
        </MockedProvider>
      </Provider>,
      {
        wrappingComponent: authzPermissionsContext.Provider,
        wrappingComponentProps: { value: mockedPermissions },
      }
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
    const mockedPermissions: PureAbility<string> = new PureAbility([
      {
        action: "backend_api_mutations_handle_vulns_acceptation_mutate",
      },
    ]);
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
    const mokedVulns: IVulnerabilities[] = [
      {
        historicTreatment: [
          {
            acceptanceDate: "",
            acceptanceStatus: "SUBMITTED",
            date: "2019-07-05 09:56:40",
            justification: "test justification",
            treatment: "ACCEPTED_UNDEFINED",
            treatmentManager: "treatment-manager-1",
            user: "user@test.com",
          },
        ],
        id: "test_error",
        specific: "",
        where: "",
        zeroRisk: "Requested",
      },
    ];
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider addTypename={false} mocks={mocksMutation}>
          <HandleAcceptationModal
            findingId={"1"}
            groupName={""}
            handleCloseModal={jest.fn()}
            refetchData={jest.fn()}
            vulns={mokedVulns}
          />
        </MockedProvider>
      </Provider>,
      {
        wrappingComponent: authzPermissionsContext.Provider,
        wrappingComponentProps: { value: mockedPermissions },
      }
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
