import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import moment from "moment";
import React from "react";
import { act } from "react-dom/test-utils";
import { useTranslation } from "react-i18next";
import { MemoryRouter } from "react-router-dom";
import waitForExpect from "wait-for-expect";

import { ClosingDateField } from "./components/ClosingDateField";
import type { IClosingDateFieldProps } from "./components/ClosingDateField/types";
import { Label } from "./styles";
import { Value } from "./value";

import type { IVulnRowAttr } from "../types";
import { AdditionalInfo } from "scenes/Dashboard/components/Vulnerabilities/AdditionalInfo";
import { GET_VULN_ADDITIONAL_INFO } from "scenes/Dashboard/components/Vulnerabilities/AdditionalInfo/queries";
import { formatVulnerabilities } from "scenes/Dashboard/components/Vulnerabilities/utils";

describe("AdditionalInfo", (): void => {
  const numberOfDays: number = 5;
  const mockVuln: IVulnRowAttr = {
    assigned: "assigned-user-4",
    currentState: "closed",
    currentStateCapitalized: "Closed",
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
    lastVerificationDate: moment()
      .subtract(numberOfDays, "days")
      .format("YYYY-MM-DD hh:mm:ss"),
    remediated: false,
    reportDate: "",
    severity: "1",
    specific: "specific-3",
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
          commitHash: null,
          cycles: "1",
          efficacy: "0",
          lastReattackRequester: "",
          lastRequestedReattackDate: null,
          lastStateDate: "2020-09-05 03:23:23",
          lastTreatmentDate: "2019-07-05 09:56:40",
          reportDate: "",
          severity: "1",
          stream: null,
          treatment: "IN_PROGRESS",
          treatmentAcceptanceDate: "",
          treatmentAssigned: "assigned-user-4",
          treatmentChanges: "1",
          treatmentJustification: "test progress justification",
          vulnerabilityType: "lines",
        },
      },
    },
  };

  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof AdditionalInfo).toStrictEqual("function");
  });

  it("should render in vulnerabilities", async (): Promise<void> => {
    expect.hasAssertions();

    const { t } = useTranslation();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/vulns/438679960/locations"]}>
        <MockedProvider
          addTypename={false}
          mocks={[mockQueryVulnAdditionalInfo]}
        >
          <AdditionalInfo
            canRetrieveHacker={false}
            onClose={jest.fn()}
            vulnerability={formatVulnerabilities([mockVuln])[0]}
          />
        </MockedProvider>
      </MemoryRouter>
    );

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();
      });
    });

    expect(wrapper).toHaveLength(1);

    expect(wrapper.find(Label).first().find("span").text()).toContain(
      t("searchFindings.tabVuln.vulnTable.vulnerabilityType.lines")
    );

    const closingDateField: ReactWrapper<IClosingDateFieldProps> =
      wrapper.find(ClosingDateField);
    const closingDateFieldLabel = closingDateField.find(Label);
    const closingDateFieldValue = closingDateField.find(Value);

    expect(closingDateFieldLabel.text()).toStrictEqual(
      t("searchFindings.tabVuln.vulnTable.closingDate")
    );
    expect(closingDateFieldValue.text()).toStrictEqual("2020-09-05");
  });
});
