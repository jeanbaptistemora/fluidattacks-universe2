import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { act } from "react-dom/test-utils";
import { useTranslation } from "react-i18next";
import { MemoryRouter, Route } from "react-router-dom";
import waitForExpect from "wait-for-expect";

import { TasksContent } from "scenes/Dashboard/containers/Tasks";
import {
  GET_ME_VULNERABILITIES_ASSIGNED,
  GET_USER_ORGANIZATIONS_GROUPS,
} from "scenes/Dashboard/queries";
import type {
  IGetMeVulnerabilitiesAssigned,
  IGetUserOrganizationsGroups,
} from "scenes/Dashboard/types";
import { authzPermissionsContext } from "utils/authz/config";
import { msgError, msgSuccess } from "utils/notifications";

jest.mock("../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary<() => Dictionary> = jest.requireActual(
    "../../../../utils/notifications"
  );
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

describe("VulnerabilitiesView", (): void => {
  const mocksVulnerabilities: MockedResponse = {
    request: {
      query: GET_ME_VULNERABILITIES_ASSIGNED,
    },
    result: {
      data: {
        me: {
          vulnerabilitiesAssigned: [
            {
              __typename: "Vulnerability",
              currentState: "open",
              externalBugTrackingSystem: null,
              findingId: "422286126",
              groupName: "group1",
              id: "89521e9a-b1a3-4047-a16e-15d530dc1340",
              lastTreatmentDate: "2019-07-05 09:56:40",
              lastVerificationDate: null,
              remediated: false,
              reportDate: "2019-07-05 09:56:40",
              severity: "",
              specific: "specific-1",
              stream: "home > blog > articulo",
              tag: "tag-1, tag-2",
              treatment: "ACCEPTED",
              treatmentAcceptanceDate: "",
              treatmentAcceptanceStatus: "",
              treatmentAssigned: "assigned-user-1",
              treatmentDate: "2019-07-05 09:56:40",
              treatmentJustification: "test progress justification",
              verification: null,
              vulnerabilityType: "inputs",
              where: "https://example.com/inputs",
              zeroRisk: null,
            },
            {
              __typename: "Vulnerability",
              currentState: "open",
              externalBugTrackingSystem: null,
              findingId: "422286126",
              groupName: "group2",
              id: "6903f3e4-a8ee-4a5d-ac38-fb738ec7e540",
              lastTreatmentDate: "2019-07-05 09:56:40",
              lastVerificationDate: null,
              remediated: false,
              reportDate: "2020-07-05 09:56:40",
              severity: "",
              specific: "specific-3",
              stream: null,
              tag: "tag-3",
              treatment: "IN_PROGRESS",
              treatmentAcceptanceDate: "",
              treatmentAcceptanceStatus: "",
              treatmentAssigned: "assigned-user-1",
              treatmentDate: "2019-07-05 09:56:40",
              treatmentJustification: "test progress justification",
              verification: null,
              vulnerabilityType: "lines",
              where: "https://example.com/tests",
              zeroRisk: null,
            },
          ],
        },
      },
    },
  };

  const mocksUserGroups: MockedResponse = {
    request: {
      query: GET_USER_ORGANIZATIONS_GROUPS,
    },
    result: {
      data: {
        me: {
          organizations: [
            {
              groups: [
                {
                  name: "group1",
                  permissions: [
                    "api_mutations_request_vulnerabilities_verification_mutate",
                    "api_mutations_update_vulnerabilities_treatment_mutate",
                    "api_resolvers_group_stakeholders_resolve",
                  ],
                  serviceAttributes: ["is_continuous"],
                },
                {
                  name: "group2",
                  permissions: [
                    "api_mutations_request_vulnerabilities_verification_mutate",
                    "api_mutations_update_vulnerabilities_treatment_mutate",
                  ],
                  serviceAttributes: [],
                },
              ],
              name: "orgtest",
            },
          ],
        },
      },
    },
  };

  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof TasksContent).toStrictEqual("function");
  });

  it("should handle reattack button basic", async (): Promise<void> => {
    expect.hasAssertions();

    const { t } = useTranslation();

    const refreshClick: jest.Mock = jest.fn();
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_resolvers_vulnerability_hacker_resolve" },
    ]);

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/todos"]}>
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <Route path={"/todos"}>
            <TasksContent
              meVulnerabilitiesAssigned={
                (
                  mocksVulnerabilities.result as Dictionary<{
                    me: IGetMeVulnerabilitiesAssigned["me"];
                  }>
                ).data
              }
              refetchVulnerabilitiesAssigned={jest.fn()}
              setUserRole={refreshClick}
              userData={
                (
                  mocksUserGroups.result as Dictionary<{
                    me: IGetUserOrganizationsGroups["me"];
                  }>
                ).data
              }
            />
          </Route>
        </authzPermissionsContext.Provider>
      </MemoryRouter>
    );

    wrapper.update();

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper).toHaveLength(1);
      });
    });

    const refreshAssigned = wrapper
      .find("Button")
      .find("#refresh-assigned")
      .first();

    refreshAssigned.simulate("click");

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper).toHaveLength(1);
        expect(refreshClick).toHaveBeenCalledTimes(1);
      });
    });

    const tableVulnerabilities: ReactWrapper = wrapper
      .find({ id: "vulnerabilitiesTable" })
      .at(0);
    const selectionCell: ReactWrapper =
      tableVulnerabilities.find("SelectionCell");
    selectionCell.at(0).find("input").simulate("click");
    selectionCell.at(1).find("input").simulate("click");
    wrapper.update();

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        const tableUpdated: ReactWrapper = wrapper
          .find({ id: "vulnerabilitiesTable" })
          .at(0);
        const selectionUpdated: ReactWrapper =
          tableUpdated.find("SelectionCell");

        expect(selectionUpdated.at(0).find("input").prop("checked")).toBe(true);
        expect(selectionUpdated.at(1).find("input").prop("checked")).toBe(true);
      });
    });

    const buttons: ReactWrapper = wrapper.find("Button");
    const requestButton: ReactWrapper = buttons.filterWhere(
      (button: ReactWrapper): boolean =>
        button
          .text()
          .includes(t("searchFindings.tabDescription.requestVerify.tex"))
    );
    requestButton.simulate("click");

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper).toHaveLength(1);
        expect(msgSuccess).toHaveBeenCalledWith(
          t("searchFindings.tabVuln.info.text"),
          t("searchFindings.tabVuln.info.title")
        );
        expect(msgError).toHaveBeenCalledWith(
          t("searchFindings.tabVuln.errors.selectedVulnerabilities")
        );
      });
    });
  });

  it("should handle edit button basic", async (): Promise<void> => {
    expect.hasAssertions();

    const { t } = useTranslation();

    const refreshClick: jest.Mock = jest.fn();
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_resolvers_vulnerability_hacker_resolve" },
    ]);

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/todos"]}>
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <MockedProvider addTypename={false} mocks={[]}>
            <Route path={"/todos"}>
              <TasksContent
                meVulnerabilitiesAssigned={
                  (
                    mocksVulnerabilities.result as Dictionary<{
                      me: IGetMeVulnerabilitiesAssigned["me"];
                    }>
                  ).data
                }
                refetchVulnerabilitiesAssigned={jest.fn()}
                setUserRole={refreshClick}
                userData={
                  (
                    mocksUserGroups.result as Dictionary<{
                      me: IGetUserOrganizationsGroups["me"];
                    }>
                  ).data
                }
              />
            </Route>
          </MockedProvider>
        </authzPermissionsContext.Provider>
      </MemoryRouter>
    );

    wrapper.update();

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper).toHaveLength(1);
      });
    });

    const filterModal = (modal: ReactWrapper): boolean =>
      modal.text().includes(t("searchFindings.tabDescription.editVuln"));

    const tableVulnerabilities: ReactWrapper = wrapper
      .find({ id: "vulnerabilitiesTable" })
      .at(0);
    const selectionCell: ReactWrapper =
      tableVulnerabilities.find("SelectionCell");
    selectionCell.at(0).find("input").simulate("click");
    selectionCell.at(1).find("input").simulate("click");
    wrapper.update();

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        const tableUpdated: ReactWrapper = wrapper
          .find({ id: "vulnerabilitiesTable" })
          .at(0);
        const selectionUpdated: ReactWrapper =
          tableUpdated.find("SelectionCell");

        expect(selectionUpdated.at(0).find("input").prop("checked")).toBe(true);
        expect(selectionUpdated.at(1).find("input").prop("checked")).toBe(true);
      });
    });

    const buttons: ReactWrapper = wrapper.find("Button");
    const editButton: ReactWrapper = buttons.filterWhere(
      (button: ReactWrapper): boolean =>
        button.text().includes(t("searchFindings.tabVuln.buttons.edit"))
    );
    editButton.simulate("click");

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        const firstModal = wrapper.find("Modal").filterWhere(filterModal);

        expect(wrapper).toHaveLength(1);
        expect(firstModal).toHaveLength(1);
        expect(
          firstModal
            .first()
            .find({ name: "treatment" })
            .find("select")
            .prop("value")
        ).toStrictEqual("ACCEPTED");
      });
    });

    const firstCloseButton: ReactWrapper = wrapper
      .find("Modal")
      .filterWhere(filterModal)
      .first()
      .find("Button")
      .filterWhere((button: ReactWrapper): boolean => button.contains("Close"));

    firstCloseButton.simulate("click");

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        const secondModal = wrapper.find("Modal").filterWhere(filterModal);

        expect(wrapper).toHaveLength(1);
        expect(secondModal).toHaveLength(1);
        expect(
          secondModal
            .last()
            .find({ name: "treatment" })
            .find("select")
            .prop("value")
        ).toStrictEqual("IN_PROGRESS");
      });
    });

    const secondCloseButton: ReactWrapper = wrapper
      .find("Modal")
      .filterWhere(filterModal)
      .last()
      .find("Button")
      .filterWhere((button: ReactWrapper): boolean => button.contains("Close"));
    secondCloseButton.simulate("click");

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper).toHaveLength(1);
        expect(wrapper.find("Modal").filterWhere(filterModal)).toHaveLength(0);
      });
    });
  });
});
