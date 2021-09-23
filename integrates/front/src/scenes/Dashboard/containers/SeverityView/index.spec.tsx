import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import { GraphQLError } from "graphql";
import React from "react";
import { act } from "react-dom/test-utils";
import { useTranslation } from "react-i18next";
import { MemoryRouter, Route } from "react-router-dom";
import wait from "waait";

import type { ISeverityTile } from "./SeverityContent/tile";
import { SeverityTile } from "./SeverityContent/tile";
import type { ISeverityAttr } from "./types";

import { SeverityView } from "scenes/Dashboard/containers/SeverityView";
import { GET_SEVERITY } from "scenes/Dashboard/containers/SeverityView/queries";
import { authzPermissionsContext } from "utils/authz/config";

describe("SeverityView", (): void => {
  const mocks: readonly MockedResponse[] = [
    {
      request: {
        query: GET_SEVERITY,
        variables: {
          identifier: "438679960",
        },
      },
      result: {
        data: {
          finding: {
            cvssVersion: "3.1",
            id: "468603225",
            severity: {
              attackComplexity: 0.77,
              attackVector: 0.85,
              availabilityImpact: 0.56,
              availabilityRequirement: 1.5,
              confidentialityImpact: 0.56,
              confidentialityRequirement: 1.5,
              exploitability: 1,
              integrityImpact: 0.56,
              integrityRequirement: 1.5,
              modifiedAttackComplexity: 0.44,
              modifiedAttackVector: 0.62,
              modifiedAvailabilityImpact: 0,
              modifiedConfidentialityImpact: 0.22,
              modifiedIntegrityImpact: 0.22,
              modifiedPrivilegesRequired: 0.85,
              modifiedSeverityScope: 0,
              modifiedUserInteraction: 0.85,
              privilegesRequired: 0.85,
              remediationLevel: 1,
              reportConfidence: 1,
              severityScope: 1,
              userInteraction: 0.85,
            },
            severityScore: 2.9,
          },
        },
      },
    },
  ];

  const mockError: readonly MockedResponse[] = [
    {
      request: {
        query: GET_SEVERITY,
        variables: {
          identifier: "438679960",
        },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
    },
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof SeverityView).toStrictEqual("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    const { t } = useTranslation();
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_update_severity_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/vulns/438679960/severity"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={SeverityView}
              path={"/:groupName/vulns/:findingId/severity"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    expect(wrapper).toHaveLength(1);

    const numberOfTiles: number = 11;
    const severityTiles: ReactWrapper<ISeverityTile> =
      wrapper.find(SeverityTile);
    const reportConfidence: ReactWrapper<ISeverityTile> = severityTiles.last();

    type resultType = Dictionary<{ finding: ISeverityAttr["finding"] }>;

    expect(severityTiles).toHaveLength(numberOfTiles);
    expect(reportConfidence.find("small").last().text()).toStrictEqual(
      String(
        (mocks[0].result as resultType).data.finding.severity.reportConfidence
      )
    );
    expect(reportConfidence.find("b").first().text()).toStrictEqual(
      t("searchFindings.tabSeverity.reportConfidence")
    );

    const editButton: ReactWrapper = wrapper
      .find("button")
      .findWhere((element: ReactWrapper): boolean => element.contains("Edit"))
      .at(0);

    expect(editButton).toHaveLength(1);

    editButton.simulate("click");

    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    expect(wrapper.text()).toContain(
      "High: Exploit is not required or it can be automated"
    );
  });

  it("should render an error in component", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/vulns/438679960/severity"]}>
        <MockedProvider addTypename={false} mocks={mockError}>
          <Route
            component={SeverityView}
            path={"/:groupName/vulns/:findingId/severity"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    expect(wrapper).toHaveLength(1);
  });

  it("should render as editable", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_update_severity_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/vulns/438679960/severity"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={SeverityView}
              path={"/:groupName/vulns/:findingId/severity"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });
    const editButton: ReactWrapper = wrapper
      .find("button")
      .findWhere((element: ReactWrapper): boolean => element.contains("Edit"))
      .at(0);

    expect(editButton).toHaveLength(1);

    editButton.simulate("click");
    act((): void => {
      wrapper.update();
    });

    expect(wrapper.text()).toContain("Update");
  });

  it("should render as readonly", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/vulns/438679960/severity"]}>
        <MockedProvider addTypename={false} mocks={mockError}>
          <Route
            component={SeverityView}
            path={"/:groupName/vulns/:findingId/severity"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });
    const editButton: ReactWrapper = wrapper
      .find("button")
      .findWhere((element: ReactWrapper): boolean => element.contains("Edit"))
      .at(0);

    expect(editButton).toHaveLength(0);
  });
});
