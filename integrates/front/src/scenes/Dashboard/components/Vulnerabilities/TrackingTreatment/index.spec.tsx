import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { act } from "react-dom/test-utils";
import { useTranslation } from "react-i18next";
import { MemoryRouter } from "react-router-dom";
import waitForExpect from "wait-for-expect";

import { TreatmentTracking } from "scenes/Dashboard/components/Vulnerabilities/TrackingTreatment/index";
import { GET_VULN_TREATMENT } from "scenes/Dashboard/components/Vulnerabilities/TrackingTreatment/queries";
import type { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";
import { formatDropdownField } from "utils/formatHelpers";

describe("TrackingTreatment", (): void => {
  const vulnId: string = "af7a48b8-d8fc-41da-9282-d424fff563f0";
  const newNumberOfFields: number = 1;
  const normalNumberOfFields: number = 3;
  const permanentlyNumberOfFields: number = 5;
  const historicTreatment: IHistoricTreatment[] = [
    {
      date: "2019-01-17 10:06:04",
      treatment: "NEW",
      user: "",
    },
    {
      acceptanceStatus: "SUBMITTED",
      assigned: "usermanager1@test.test",
      date: "2020-02-17 18:36:24",
      justification: "Some of the resources",
      treatment: "ACCEPTED_UNDEFINED",
      user: "usertreatment1@test.test",
    },
    {
      acceptanceStatus: "APPROVED",
      assigned: "usermanager2@test.test",
      date: "2020-02-18 18:36:24",
      justification: "The headers must be",
      treatment: "ACCEPTED_UNDEFINED",
      user: "usertreatment2@test.test",
    },
    {
      acceptanceDate: "2020-10-09 15:29:48",
      assigned: "usermanager3@test.test",
      date: "2020-10-02 15:29:48",
      justification: "The headers must be",
      treatment: "ACCEPTED",
      user: "usertreatment3@test.test",
    },
    {
      assigned: "usermanager4@test.test",
      date: "2020-10-08 15:29:48",
      justification: "The headers must be",
      treatment: "IN PROGRESS",
      user: "usertreatment4@test.test",
    },
  ];

  const mockQueryVulnTreatment1: MockedResponse = {
    request: {
      query: GET_VULN_TREATMENT,
      variables: {
        vulnId,
      },
    },
    result: {
      data: {
        vulnerability: {
          __typename: "Vulnerability",
          historicTreatment: [...historicTreatment],
        },
      },
    },
  };

  const rejectedObservation: string = "The treatment was rejected";
  const mockQueryVulnTreatment2: MockedResponse = {
    request: {
      query: GET_VULN_TREATMENT,
      variables: {
        vulnId,
      },
    },
    result: {
      data: {
        vulnerability: {
          __typename: "Vulnerability",
          historicTreatment: [
            ...historicTreatment.slice(0, 2),
            {
              acceptanceStatus: "REJECTED",
              assigned: "usermanager2@test.test",
              date: "2020-02-18 18:36:24",
              justification: rejectedObservation,
              treatment: "ACCEPTED_UNDEFINED",
              user: "usertreatment2@test.test",
            },
            {
              date: "2020-02-18 18:36:25",
              treatment: "NEW",
              user: "",
            },
          ],
        },
      },
    },
  };

  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof TreatmentTracking).toStrictEqual("function");
  });

  it("should render in treatment tracking 1", async (): Promise<void> => {
    expect.hasAssertions();

    const { t } = useTranslation();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/vulns/438679960/locations"]}>
        <MockedProvider addTypename={false} mocks={[mockQueryVulnTreatment1]}>
          <TreatmentTracking vulnId={vulnId} />
        </MockedProvider>
      </MemoryRouter>
    );

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();
      });
    });

    expect(wrapper).toHaveLength(1);

    expect(wrapper.find("li").first().find("p")).toHaveLength(
      normalNumberOfFields
    );
    expect(wrapper.find("li").at(1).find("p")).toHaveLength(
      normalNumberOfFields
    );
    expect(wrapper.find("li").at(2).find("p")).toHaveLength(
      permanentlyNumberOfFields
    );
    expect(wrapper.find("li").last().find("p")).toHaveLength(newNumberOfFields);
    expect(wrapper.find("li").first().find("p").first().text()).toBe(
      t("searchFindings.tabDescription.treatment.inProgress")
    );
  });

  it("should render in treatment tracking 2", async (): Promise<void> => {
    expect.hasAssertions();

    const { t } = useTranslation();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/vulns/438679960/locations"]}>
        <MockedProvider addTypename={false} mocks={[mockQueryVulnTreatment2]}>
          <TreatmentTracking vulnId={vulnId} />
        </MockedProvider>
      </MemoryRouter>
    );

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();
      });
    });

    expect(wrapper).toHaveLength(1);

    expect(wrapper.find("li").first().find("p")).toHaveLength(
      newNumberOfFields
    );
    expect(wrapper.find("li").at(1).find("p")).toHaveLength(
      normalNumberOfFields
    );
    expect(wrapper.find("li").at(1).find("p").first().text()).toBe(
      t(formatDropdownField(historicTreatment[2].treatment)) +
        t("searchFindings.tabDescription.treatment.pendingApproval")
    );
    expect(wrapper.find("li").at(1).find("p").last().text()).toBe(
      `${t(
        "searchFindings.tabTracking.justification"
      )}\u00a0${rejectedObservation}`
    );
  });
});
