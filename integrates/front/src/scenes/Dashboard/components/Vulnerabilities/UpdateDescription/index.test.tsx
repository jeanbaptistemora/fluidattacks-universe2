/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { GraphQLError } from "graphql";
import React from "react";

import {
  REQUEST_VULNS_ZERO_RISK,
  UPDATE_DESCRIPTION_MUTATION,
} from "./queries";
import type { IUpdateVulnDescriptionResultAttr } from "./types";

import { GET_GROUP_USERS } from "../queries";
import type { IVulnDataTypeAttr } from "scenes/Dashboard/components/Vulnerabilities/types";
import { UpdateDescription } from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription";
import {
  getLastTreatment,
  groupLastHistoricTreatment,
} from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/utils";
import type { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";
import { GET_FINDING_HEADER } from "scenes/Dashboard/containers/FindingContent/queries";
import {
  GET_FINDING_AND_GROUP_INFO,
  GET_FINDING_NZR_VULNS,
  GET_FINDING_ZR_VULNS,
} from "scenes/Dashboard/containers/VulnerabilitiesView/queries";
import { authzGroupContext, authzPermissionsContext } from "utils/authz/config";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

jest.mock("../../../../../utils/notifications", (): Record<string, unknown> => {
  const mockedNotifications: Record<string, () => Record<string, unknown>> =
    jest.requireActual("../../../../../utils/notifications");
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

describe("Update Description component", (): void => {
  const btnConfirm = "components.modal.confirm";

  const vulns: IVulnDataTypeAttr[] = [
    {
      assigned: "",
      currentState: "open",
      externalBugTrackingSystem: null,
      findingId: "1",
      groupName: "",
      historicTreatment: [
        {
          date: "",
          justification: "test justification",
          treatment: "NEW",
          user: "",
        },
      ],
      id: "ab25380d-dfe1-4cde-aefd-acca6990d6aa",
      severity: "2",
      specific: "",
      tag: "one",
      where: "",
    },
  ];
  const mocksVulns: MockedResponse[] = [
    {
      request: {
        query: GET_FINDING_AND_GROUP_INFO,
        variables: {
          findingId: "422286126",
        },
      },
      result: {
        data: {
          finding: {
            id: "422286126",
            remediated: false,
            state: "open",
            verified: false,
          },
        },
      },
    },
    {
      request: {
        query: GET_FINDING_ZR_VULNS,
        variables: {
          canRetrieveZeroRisk: false,
          findingId: "422286126",
          first: 100,
          state: "OPEN",
        },
      },
      result: {
        data: {
          finding: {
            zeroRiskConnection: undefined,
          },
        },
      },
    },
    {
      request: {
        query: GET_FINDING_NZR_VULNS,
        variables: {
          findingId: "422286126",
          first: 100,
          state: "OPEN",
        },
      },
      result: {
        data: {
          finding: {
            vulnerabilitiesConnection: {
              edges: [
                {
                  node: {
                    currentState: "open",
                    externalBugTrackingSystem: null,
                    findingId: "422286126",
                    id: "",
                    remediated: false,
                    reportDate: "",
                    severity: null,
                    specific: "",
                    tag: "",
                    verification: null,
                    vulnerabilityType: "",
                    where: "",
                    zeroRisk: null,
                  },
                },
              ],
              pageInfo: {
                endCursor: "test-cursor=",
                hasNextPage: false,
              },
            },
          },
        },
      },
    },
  ];
  const mocksFindingHeader: MockedResponse = {
    request: {
      query: GET_FINDING_HEADER,
      variables: {
        findingId: "422286126",
      },
    },
    result: {
      data: {
        finding: {
          closedVulns: 0,
          currentState: "APPROVED",
          id: "ab25380d-dfe1-4cde-aefd-acca6990d6aa",
          openVulns: 0,
          releaseDate: null,
          reportDate: null,
          severityScore: 1,
          state: "default",
          title: "",
          tracking: [],
        },
      },
    },
  };
  const mockedPermissions = new PureAbility<string>([
    { action: "api_mutations_remove_vulnerability_tags_mutate" },
    { action: "api_mutations_request_vulnerabilities_zero_risk_mutate" },
    { action: "api_mutations_update_vulnerability_treatment_mutate" },
    { action: "api_mutations_update_vulnerabilities_treatment_mutate" },
    { action: "api_resolvers_group_stakeholders_resolve" },
  ]);

  it("should group last treatment", (): void => {
    expect.hasAssertions();

    const treatment: IHistoricTreatment = {
      date: "",
      justification: "test justification",
      treatment: "IN PROGRESS",
      user: "",
    };

    const vulnerabilities: IVulnDataTypeAttr[] = [
      {
        assigned: "",
        currentState: "open",
        externalBugTrackingSystem: null,
        findingId: "1",
        groupName: "",
        historicTreatment: [treatment],
        id: "test_one",
        severity: null,
        specific: "",
        tag: "one",
        where: "",
      },
      {
        assigned: "",
        currentState: "open",
        externalBugTrackingSystem: null,
        findingId: "1",
        groupName: "",
        historicTreatment: [treatment],
        id: "test_two",
        severity: null,
        specific: "",
        tag: "one",
        where: "",
      },
    ];

    const lastTreatment: IHistoricTreatment =
      groupLastHistoricTreatment(vulnerabilities);

    expect(lastTreatment).toStrictEqual(getLastTreatment([treatment]));
  });

  it("list editable fields", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleOnClose: jest.Mock = jest.fn();
    const handleClearSelected: jest.Mock = jest.fn();
    const handleRefetchData: jest.Mock = jest.fn();
    render(
      <MockedProvider addTypename={false} mocks={[]}>
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <UpdateDescription
            findingId={"1"}
            groupName={""}
            handleClearSelected={handleClearSelected}
            handleCloseModal={handleOnClose}
            refetchData={handleRefetchData}
            vulnerabilities={vulns}
          />
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );

    await waitFor((): void => {
      expect(
        screen.queryAllByRole("combobox", { name: "treatment" })
      ).toHaveLength(1);
    });

    expect(screen.queryAllByRole("textbox")).toHaveLength(1);

    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "treatment" }),
      ["IN_PROGRESS"]
    );
    const numberOfEditableFields: number = 3;

    await waitFor((): void => {
      expect(screen.queryAllByRole("textbox")).toHaveLength(
        numberOfEditableFields
      );
    });

    expect(screen.getByRole("spinbutton", { name: "severity" })).toHaveValue(
      Number(vulns[0].severity)
    );
  });

  it("should handle request zero risk", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleOnClose: jest.Mock = jest.fn();
    const handleClearSelected: jest.Mock = jest.fn();
    const handleRefetchData: jest.Mock = jest.fn();

    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: REQUEST_VULNS_ZERO_RISK,
          variables: {
            findingId: "422286126",
            justification:
              "This is a commenting test of a request zero risk in vulns",
            vulnerabilities: ["ab25380d-dfe1-4cde-aefd-acca6990d6aa"],
          },
        },
        result: { data: { requestVulnerabilitiesZeroRisk: { success: true } } },
      },
      ...mocksVulns,
      mocksFindingHeader,
    ];
    render(
      <MockedProvider addTypename={false} mocks={mocksMutation}>
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <authzGroupContext.Provider
            value={new PureAbility([{ action: "can_report_vulnerabilities" }])}
          >
            <UpdateDescription
              findingId={"422286126"}
              groupName={"testgroupname"}
              handleClearSelected={handleClearSelected}
              handleCloseModal={handleOnClose}
              refetchData={handleRefetchData}
              vulnerabilities={vulns}
            />
          </authzGroupContext.Provider>
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );

    await waitFor((): void => {
      expect(
        screen.queryAllByRole("combobox", { name: "treatment" })
      ).toHaveLength(1);
    });

    expect(screen.getByText(btnConfirm)).toBeDisabled();

    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "treatment" }),
      ["REQUEST_ZERO_RISK"]
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "justification" }),
      "This is a commenting test of a request zero risk in vulns"
    );
    await waitFor((): void => {
      expect(screen.getByText(btnConfirm)).not.toBeDisabled();
    });

    await userEvent.click(screen.getByText(btnConfirm));

    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledWith(
        "Zero risk vulnerability has been requested",
        "Correct!"
      );
    });

    expect(handleClearSelected).toHaveBeenCalledWith();
    expect(handleOnClose).toHaveBeenCalledWith();
    expect(handleRefetchData).toHaveBeenCalledTimes(1);
  });

  it("should handle request zero risk error", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleOnClose: jest.Mock = jest.fn();
    const handleClearSelected: jest.Mock = jest.fn();
    const handleRefetchData: jest.Mock = jest.fn();

    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: REQUEST_VULNS_ZERO_RISK,
          variables: {
            findingId: "422286126",
            justification:
              "This is a commenting test of a request zero risk in vulns",
            vulnerabilities: ["ab25380d-dfe1-4cde-aefd-acca6990d6aa"],
          },
        },
        result: {
          errors: [
            new GraphQLError(
              "Exception - Zero risk vulnerability is already requested"
            ),
            new GraphQLError(
              "Exception - Justification must have a maximum of 5000 characters"
            ),
          ],
        },
      },
    ];
    render(
      <MockedProvider addTypename={false} mocks={[...mocksMutation]}>
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <authzGroupContext.Provider
            value={new PureAbility([{ action: "can_report_vulnerabilities" }])}
          >
            <UpdateDescription
              findingId={"422286126"}
              groupName={"testgroupname"}
              handleClearSelected={handleClearSelected}
              handleCloseModal={handleOnClose}
              refetchData={handleRefetchData}
              vulnerabilities={vulns}
            />
          </authzGroupContext.Provider>
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );

    await waitFor((): void => {
      expect(
        screen.queryAllByRole("combobox", { name: "treatment" })
      ).toHaveLength(1);
    });

    expect(screen.getByText(btnConfirm)).toBeDisabled();

    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "treatment" }),
      ["REQUEST_ZERO_RISK"]
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "justification" }),
      "This is a commenting test of a request zero risk in vulns"
    );
    await waitFor((): void => {
      expect(screen.getByText(btnConfirm)).not.toBeDisabled();
    });

    await userEvent.click(screen.getByText(btnConfirm));

    await waitFor((): void => {
      expect(msgError).toHaveBeenNthCalledWith(
        1,
        translate.t("groupAlerts.zeroRiskAlreadyRequested")
      );
    });

    expect(handleClearSelected).not.toHaveBeenCalled();
    expect(handleOnClose).not.toHaveBeenCalled();
    expect(handleRefetchData).not.toHaveBeenCalled();
    expect(msgError).toHaveBeenNthCalledWith(
      2,
      translate.t("validations.invalidFieldLength")
    );
  });

  it("should render update treatment", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleClearSelected: jest.Mock = jest.fn();
    const handleOnClose: jest.Mock = jest.fn();
    const handleRefetchData: jest.Mock = jest.fn();
    const updateTreatment: IUpdateVulnDescriptionResultAttr = {
      updateVulnerabilitiesTreatment: { success: true },
      updateVulnerabilityTreatment: { success: true },
    };
    const mutationVariables: Record<string, boolean | number | string> = {
      acceptanceDate: "",
      assigned: "manager_test@test.test",
      externalBugTrackingSystem: "http://test.t",
      findingId: "422286126",
      isVulnInfoChanged: true,
      isVulnTreatmentChanged: true,
      justification: "test justification to treatment",
      severity: 2,
      tag: "one",
      treatment: "IN_PROGRESS",
    };
    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: UPDATE_DESCRIPTION_MUTATION,
          variables: { ...mutationVariables, vulnerabilityId: "test1" },
        },
        result: { data: updateTreatment },
      },
      {
        request: {
          query: UPDATE_DESCRIPTION_MUTATION,
          variables: { ...mutationVariables, vulnerabilityId: "test2" },
        },
        result: { data: updateTreatment },
      },
      {
        request: {
          query: GET_GROUP_USERS,
          variables: {
            groupName: "testgroupname",
          },
        },
        result: {
          data: {
            group: {
              name: "testgroupname",
              stakeholders: [
                {
                  email: "manager_test@test.test",
                  invitationState: "REGISTERED",
                },
              ],
            },
          },
        },
      },
    ];
    const vulnsToUpdate: IVulnDataTypeAttr[] = [
      {
        assigned: "",
        currentState: "open",
        externalBugTrackingSystem: null,
        findingId: "422286126",
        groupName: "testgroupname",
        historicTreatment: [],
        id: "test1",
        severity: null,
        specific: "",
        tag: "one",
        where: "",
      },
      {
        assigned: "",
        currentState: "open",
        externalBugTrackingSystem: null,
        findingId: "422286126",
        groupName: "testgroupname",
        historicTreatment: [],
        id: "test2",
        severity: null,
        specific: "",
        tag: "one",
        where: "",
      },
    ];
    render(
      <MockedProvider
        addTypename={false}
        mocks={[...mocksMutation, ...mocksVulns]}
      >
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <authzGroupContext.Provider
            value={new PureAbility([{ action: "can_report_vulnerabilities" }])}
          >
            <UpdateDescription
              findingId={"422286126"}
              groupName={"testgroupname"}
              handleClearSelected={handleClearSelected}
              handleCloseModal={handleOnClose}
              refetchData={handleRefetchData}
              vulnerabilities={vulnsToUpdate}
            />
          </authzGroupContext.Provider>
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );
    await waitFor((): void => {
      expect(
        screen.queryAllByRole("combobox", { name: "treatment" })
      ).toHaveLength(1);
    });

    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "treatment" }),
      ["IN_PROGRESS"]
    );
    await waitFor((): void => {
      expect(
        screen.queryByRole("combobox", { name: "assigned" })
      ).toBeInTheDocument();
    });

    await userEvent.type(
      screen.getByRole("textbox", { name: "justification" }),
      "test justification to treatment"
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "externalBugTrackingSystem" }),
      "http://test.t"
    );
    await userEvent.type(
      screen.getByRole("spinbutton", { name: "severity" }),
      "2"
    );
    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "assigned" }),
      ["manager_test@test.test"]
    );

    await waitFor((): void => {
      expect(screen.getByText(btnConfirm)).not.toBeDisabled();
    });

    await userEvent.click(screen.getByText(btnConfirm));
    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledTimes(1);
    });

    expect(handleOnClose).toHaveBeenCalledTimes(1);
  });

  it("should render error update treatment", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleClearSelected: jest.Mock = jest.fn();
    const handleOnClose: jest.Mock = jest.fn();
    const handleRefetchData: jest.Mock = jest.fn();

    const mocksError: MockedResponse = {
      request: {
        query: UPDATE_DESCRIPTION_MUTATION,
        variables: {
          acceptanceDate: "",
          externalBugTrackingSystem: "",
          findingId: "422286126",
          isVulnInfoChanged: false,
          isVulnTreatmentChanged: true,
          justification: "test justification to treatment",
          severity: -1,
          tag: "one",
          treatment: "ACCEPTED_UNDEFINED",
          vulnerabilityId: "test",
        },
      },
      result: {
        errors: [
          new GraphQLError(
            "Vulnerability has been accepted the maximum number of times allowed by the defined policy"
          ),
        ],
      },
    };
    const vulnsToUpdate: IVulnDataTypeAttr[] = [
      {
        assigned: "",
        currentState: "open",
        externalBugTrackingSystem: null,
        findingId: "422286126",
        groupName: "testgroupname",
        historicTreatment: [],
        id: "test",
        severity: null,
        specific: "",
        tag: "one",
        where: "",
      },
    ];
    render(
      <MockedProvider addTypename={false} mocks={[mocksError, ...mocksVulns]}>
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <authzGroupContext.Provider
            value={new PureAbility([{ action: "can_report_vulnerabilities" }])}
          >
            <UpdateDescription
              findingId={"422286126"}
              groupName={"testgroupname"}
              handleClearSelected={handleClearSelected}
              handleCloseModal={handleOnClose}
              refetchData={handleRefetchData}
              vulnerabilities={vulnsToUpdate}
            />
          </authzGroupContext.Provider>
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );

    await waitFor((): void => {
      expect(
        screen.queryAllByRole("combobox", { name: "treatment" })
      ).toHaveLength(1);
    });

    expect(
      screen.queryByText("searchFindings.tabDescription.approvalTitle")
    ).not.toBeInTheDocument();

    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "treatment" }),
      ["ACCEPTED_UNDEFINED"]
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "justification" }),
      "test justification to treatment"
    );

    await waitFor((): void => {
      expect(screen.getByText(btnConfirm)).not.toBeDisabled();
    });

    await userEvent.click(screen.getByText(btnConfirm));

    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.tabDescription.approvalTitle")
      ).toBeInTheDocument();
    });
    await userEvent.click(
      within(
        screen.getByText("searchFindings.tabDescription.approvalMessage")
      ).getByRole("button", { name: btnConfirm })
    );
    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith(
        translate.t("searchFindings.tabVuln.alerts.maximumNumberOfAcceptances")
      );
    });

    expect(handleOnClose).not.toHaveBeenCalled();
    expect(handleRefetchData).not.toHaveBeenCalled();
  });
});
