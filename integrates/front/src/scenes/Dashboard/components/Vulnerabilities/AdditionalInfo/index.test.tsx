import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import dayjs from "dayjs";
import React from "react";
import { MemoryRouter } from "react-router-dom";

import type { IVulnRowAttr } from "../types";
import { AdditionalInfo } from "scenes/Dashboard/components/Vulnerabilities/AdditionalInfo";
import {
  GET_VULN_ADDITIONAL_INFO,
  UPDATE_VULNERABILITY_DESCRIPTION,
} from "scenes/Dashboard/components/Vulnerabilities/AdditionalInfo/queries";
import { formatVulnerabilities } from "scenes/Dashboard/components/Vulnerabilities/utils";
import { authzPermissionsContext } from "utils/authz/config";
import { msgSuccess } from "utils/notifications";

jest.mock("../../../../../utils/notifications", (): Record<string, unknown> => {
  const mockedNotifications: Record<string, () => Record<string, unknown>> =
    jest.requireActual("../../../../../utils/notifications");
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

describe("AdditionalInfo", (): void => {
  const numberOfDays: number = 5;
  const mockVuln: IVulnRowAttr = {
    assigned: "assigned-user-4",
    externalBugTrackingSystem: null,
    findingId: "438679960",
    groupName: "test",
    historicTreatment: [
      {
        acceptanceDate: "",
        acceptanceStatus: "",
        assigned: "assigned-user-4",
        date: "2019-07-05 09:56:40",
        justification: "test progress justification",
        treatment: "IN PROGRESS",
        user: "usertreatment@test.test",
      },
    ],
    id: "af7a48b8-d8fc-41da-9282-d424fff563f0",
    lastTreatmentDate: "2019-07-05 09:56:40",
    lastVerificationDate: dayjs()
      .subtract(numberOfDays, "days")
      .format("YYYY-MM-DD hh:mm:ss"),
    organizationName: undefined,
    remediated: false,
    reportDate: "",
    rootNickname: "https:",
    severity: "1",
    snippet: null,
    source: "asm",
    specific: "specific-3",
    state: "SAFE",
    stream: null,
    tag: "tag-7, tag-8",
    treatment: "IN PROGRESS",
    treatmentAcceptanceDate: "",
    treatmentAcceptanceStatus: "",
    treatmentAssigned: "assigned-user-4",
    treatmentDate: "2019-07-05 09:56:40",
    treatmentJustification: "test progress justification",
    treatmentUser: "usertreatment@test.test",
    verification: "Verified",
    vulnerabilityType: "lines",
    where: "https://example.com/lines",
    zeroRisk: null,
  };

  const mockQueryVulnAdditionalInfo: MockedResponse = {
    request: {
      query: GET_VULN_ADDITIONAL_INFO,
      variables: {
        canRetrieveHacker: false,
        vulnId: "af7a48b8-d8fc-41da-9282-d424fff563f0",
      },
    },
    result: {
      data: {
        vulnerability: {
          __typename: "Vulnerability",
          closingDate: "2020-09-05 03:23:23",
          commitHash: null,
          cycles: "1",
          efficacy: "0",
          lastReattackRequester: "",
          lastRequestedReattackDate: null,
          lastStateDate: "2020-09-05 03:23:23",
          lastTreatmentDate: "2019-07-05 09:56:40",
          reportDate: "",
          rootNickname: "",
          severity: "1",
          source: "escape",
          specific: "specific-3",
          stream: null,
          treatment: "IN_PROGRESS",
          treatmentAcceptanceDate: "",
          treatmentAssigned: "assigned-user-4",
          treatmentChanges: "1",
          treatmentJustification: "test progress justification",
          vulnerabilityType: "lines",
          where: "https://example.com/lines",
        },
      },
    },
  };

  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof AdditionalInfo).toBe("function");
  });

  it("should render in vulnerabilities", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/TEST/vulns/438679960/locations"]}>
        <MockedProvider
          addTypename={false}
          mocks={[mockQueryVulnAdditionalInfo]}
        >
          <AdditionalInfo
            canRetrieveHacker={false}
            canSeeSource={true}
            refetchData={jest.fn()}
            vulnerability={formatVulnerabilities([mockVuln])[0]}
          />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(
        screen.getByText(
          "searchFindings.tabVuln.vulnTable.vulnerabilityType.lines"
        )
      ).toBeInTheDocument();
    });

    expect(
      screen.getByText("searchFindings.tabVuln.vulnTable.closingDate")
    ).toBeInTheDocument();

    expect(screen.getByText("2020-09-05")).toBeInTheDocument();
  });

  it("should update vulnerability details", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedMutations: MockedResponse[] = [
      {
        request: {
          query: UPDATE_VULNERABILITY_DESCRIPTION,
          variables: {
            commit: "ea871eee64cfd5ce293411efaf4d3b446d04eb4a",
            source: "DETERMINISTIC",
            vulnerabilityId: "af7a48b8-d8fc-41da-9282-d424fff563f0",
          },
        },
        result: {
          data: {
            updateVulnerabilityDescription: {
              success: true,
            },
          },
        },
      },
    ];
    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_update_vulnerability_description_mutate" },
    ]);

    render(
      <MemoryRouter initialEntries={["/TEST/vulns/438679960/locations"]}>
        <MockedProvider
          addTypename={false}
          mocks={[mockQueryVulnAdditionalInfo, ...mockedMutations]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <AdditionalInfo
              canRetrieveHacker={false}
              canSeeSource={true}
              refetchData={jest.fn()}
              vulnerability={formatVulnerabilities([mockVuln])[0]}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(
        screen.getByText(
          "searchFindings.tabVuln.vulnTable.vulnerabilityType.lines"
        )
      ).toBeInTheDocument();
    });
    await userEvent.click(
      screen.getByText(
        "searchFindings.tabVuln.additionalInfo.buttons.edit.text"
      )
    );
    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: /source/iu }),
      ["DETERMINISTIC"]
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: /commithash/iu }),
      "ea871eee64cfd5ce293411efaf4d3b446d04eb4a"
    );
    await userEvent.click(
      screen.getByRole("button", {
        name: "searchFindings.tabVuln.additionalInfo.buttons.save.text",
      })
    );

    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledWith(
        "searchFindings.tabVuln.additionalInfo.alerts.updatedDetails",
        "groupAlerts.updatedTitle"
      );
    });
  });
});
