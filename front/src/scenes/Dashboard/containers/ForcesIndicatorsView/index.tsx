/* tslint:disable:jsx-no-multiline-js
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code in graphql queries
 */
import { QueryResult } from "@apollo/react-common";
import { Query } from "@apollo/react-components";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { Col, Row } from "react-bootstrap";
import { handleGraphQLErrors } from "../../../../utils/formatHelpers";
import translate from "../../../../utils/translations/translate";
import { IndicatorBox } from "../../components/IndicatorBox/index";
import { default as style } from "./index.css";
import { GET_INDICATORS } from "./queries";
import { IForcesExecution, IForcesIndicatorsProps, IForcesIndicatorsViewBaseProps } from "./types";

const forcesIndicatorsView: React.FC<IForcesIndicatorsViewBaseProps> =
(props: IForcesIndicatorsViewBaseProps): JSX.Element => {
  const projectName: string = props.projectName;

  const goToProjectForces: (() => void) = (): void => {
    location.hash = `#!/project/${projectName}/forces`;
  };

  const handleQryResult: ((qrResult: IForcesIndicatorsProps) => void) = (qrResult: IForcesIndicatorsProps): void => {
    mixpanel.track(
      "ForcesIndicator",
      {
        Organization: (window as typeof window & { userOrganization: string }).userOrganization,
        User: (window as typeof window & { userName: string }).userName,
      });
  };

  return (
    <Query query={GET_INDICATORS} variables={{ projectName }} onCompleted={handleQryResult}>
      {
        ({ error, data }: QueryResult<IForcesIndicatorsProps>): JSX.Element => {
          if (_.isUndefined(data) || _.isEmpty(data)) {

            return <React.Fragment />;
          }
          if (!_.isUndefined(error)) {
            handleGraphQLErrors("An error occurred getting forces indicators", error);

            return <React.Fragment />;
          }
          if (!_.isUndefined(data)) {
            const executions: IForcesExecution[] = data.forcesExecutions.executions;
            const executionsInStrictMode: IForcesExecution[] =
              executions.filter((execution: IForcesExecution): boolean => execution.strictness === "strict");
            const executionsInAnyModeWithAcceptedVulns: IForcesExecution[] =
              executions.filter((execution: IForcesExecution): boolean => (
                execution.vulnerabilities.numOfVulnerabilitiesInAcceptedExploits > 0));
            const executionsInAnyModeWithVulns: IForcesExecution[] =
              executions.filter((execution: IForcesExecution): boolean => (
                execution.vulnerabilities.numOfVulnerabilitiesInExploits > 0
                  || execution.vulnerabilities.numOfVulnerabilitiesInMockedExploits > 0));
            const executionsInStrictModeWithVulns: IForcesExecution[] =
              executionsInStrictMode.filter((execution: IForcesExecution): boolean => (
                execution.vulnerabilities.numOfVulnerabilitiesInExploits > 0
                  || execution.vulnerabilities.numOfVulnerabilitiesInMockedExploits > 0));

            const executionsInAnyModeNumber: number = executions.length;
            const executionsInAnyModeWithVulnsNumber: number = executionsInAnyModeWithVulns.length;
            const executionsInAnyModeWithAcceptedVulnsNumber: number = executionsInAnyModeWithAcceptedVulns.length;
            const executionsInStrictModeNumber: number = executionsInStrictMode.length;
            const executionsInStrictModeWithVulnsNumber: number = executionsInStrictModeWithVulns.length;

            const securityCommitmentNumber: number = _.round(
              executionsInAnyModeNumber > 0 ? executionsInStrictModeNumber / executionsInAnyModeNumber * 100 : 100);
            const securityCommitment: string = `${securityCommitmentNumber}%`;

            return (
              <React.StrictMode>
                <br />
                <br />
                <hr />
                <Row>
                  <Col md={12} sm={12} xs={12}>
                    <h1 className={style.title}>{translate.t("search_findings.tab_indicators.forces.title")}</h1>
                    <h4 className={style.subTitle}>{translate.t("search_findings.tab_indicators.forces.sub_title")}</h4>
                  </Col>
                </Row>
                {data.project.hasForces ? (
                  <React.Fragment>
                    <Row>
                      <Col md={12} sm={12} xs={12}>
                        <Col md={4} sm={12} xs={12}>
                          <IndicatorBox
                            description={
                              translate.t("search_findings.tab_indicators.forces.indicators.has_forces.protected_desc")}
                            icon="verified"
                            name={translate.t("search_findings.tab_indicators.forces.indicators.has_forces.title")}
                            onClick={goToProjectForces}
                            quantity={
                              translate.t("search_findings.tab_indicators.forces.indicators.has_forces.protected")}
                            small={true}
                            title=""
                            total=""
                          />
                        </Col>
                        <Col md={4} sm={12} xs={12}>
                          <IndicatorBox
                            description={
                              translate.t("search_findings.tab_indicators.forces.indicators.strictness.strict_desc")}
                            icon="authors"
                            name={translate.t("search_findings.tab_indicators.forces.indicators.strictness.title")}
                            onClick={goToProjectForces}
                            quantity={securityCommitment}
                            small={true}
                            title=""
                          />
                        </Col>
                        <Col md={4} sm={12} xs={12}>
                          <IndicatorBox
                            icon="privilegesHigh"
                            name={translate.t(
                              "search_findings.tab_indicators.forces.indicators.service_use.title")}
                            onClick={goToProjectForces}
                            quantity={executionsInAnyModeNumber}
                            title=""
                            total={translate.t(
                              "search_findings.tab_indicators.forces.indicators.service_use.total")}
                          />
                        </Col>
                      </Col>
                    </Row>
                    <Row>
                      <Col md={12} sm={12} xs={12}>
                        <Col md={4} sm={12} xs={12}>
                          <IndicatorBox
                            description={translate.t(
                              "search_findings.tab_indicators.forces.indicators.builds.allowed.desc")}
                            icon="complexityHigh"
                            name={translate.t(
                              "search_findings.tab_indicators.forces.indicators.builds.allowed.title")}
                            onClick={goToProjectForces}
                            quantity={executionsInAnyModeWithVulnsNumber}
                            small={true}
                            title=""
                            total={`/ ${executionsInAnyModeNumber} ${translate.t(
                              "search_findings.tab_indicators.forces.indicators.builds.allowed.total")}`}
                          />
                        </Col>
                        <Col md={4} sm={12} xs={12}>
                          <IndicatorBox
                            description={translate.t(
                              "search_findings.tab_indicators.forces.indicators.builds.stopped.desc")}
                            icon="confidentialityHigh"
                            name={translate.t(
                              "search_findings.tab_indicators.forces.indicators.builds.stopped.title")}
                            onClick={goToProjectForces}
                            quantity={executionsInStrictModeWithVulnsNumber}
                            small={true}
                            title=""
                            total={`/ ${executionsInAnyModeWithVulnsNumber}`}
                          />
                        </Col>
                        <Col md={4} sm={12} xs={12}>
                          <IndicatorBox
                            description={translate.t(
                              "search_findings.tab_indicators.forces.indicators.builds.accepted_risk.desc")}
                            icon="confidentialityNone"
                            name={translate.t(
                              "search_findings.tab_indicators.forces.indicators.builds.accepted_risk.title")}
                            onClick={goToProjectForces}
                            quantity={executionsInAnyModeWithAcceptedVulnsNumber}
                            small={true}
                            title=""
                            total={`/ ${executionsInAnyModeNumber}`}
                          />
                        </Col>
                      </Col>
                    </Row>
                  </React.Fragment>
                ) : (
                  <Row>
                    <Col md={12} sm={12} xs={12}>
                      <Col md={4} sm={12} xs={12}>
                        <IndicatorBox
                          icon="fail"
                          name={translate.t(
                            "search_findings.tab_indicators.forces.indicators.has_forces.title")}
                          quantity={translate.t(
                            "search_findings.tab_indicators.forces.indicators.has_forces.unprotected")}
                          title=""
                          total=""
                          description={translate.t(
                            "search_findings.tab_indicators.forces.indicators.has_forces.unprotected_desc")}
                          small={true}
                        />
                      </Col>
                    </Col>
                  </Row>
                )}
              </React.StrictMode>
            );
          } else { return <React.Fragment />; }
        }}
    </Query>
  );
};

export { forcesIndicatorsView as ForcesIndicatorsView };
