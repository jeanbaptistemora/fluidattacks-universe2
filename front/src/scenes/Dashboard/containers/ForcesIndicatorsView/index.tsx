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
            const executions: [IForcesExecution] = data.forcesExecutions.executions;
            const executionsInAnyMode: number = executions.length;
            const executionsInStrictMode: number =
              executions.filter((execution: IForcesExecution): boolean => execution.strictness === "strict").length;

            const securityCommitmentNumber: number =
              _.round(executionsInAnyMode > 0 ? executionsInStrictMode / executionsInAnyMode * 100 : 100, 0);
            const securityCommitment: string = `${securityCommitmentNumber}%`;

            return (
              <React.StrictMode>
                <br />
                <br />
                <hr />
                <Row>
                  <Col md={12} sm={12} xs={12}>
                    <h1 className={style.title}>{translate.t("search_findings.tab_indicators.forces.title")}</h1>
                    <Col md={4} sm={12} xs={12}>
                      {data.project.hasForces ? (
                        <IndicatorBox
                          icon="verified"
                          name={translate.t("search_findings.tab_indicators.forces.indicators.has_forces.title")}
                          quantity={
                            translate.t("search_findings.tab_indicators.forces.indicators.has_forces.protected")}
                          onClick={goToProjectForces}
                          title=""
                          total=""
                          description={
                            translate.t("search_findings.tab_indicators.forces.indicators.has_forces.protected_desc")}
                          small={true}
                        />
                      ) : (
                        <IndicatorBox
                          icon="fail"
                          name={translate.t("search_findings.tab_indicators.forces.indicators.has_forces.title")}
                          quantity={
                            translate.t("search_findings.tab_indicators.forces.indicators.has_forces.unprotected")}
                          title=""
                          total=""
                          description={
                            translate.t("search_findings.tab_indicators.forces.indicators.has_forces.unprotected_desc")}
                          small={true}
                        />
                      )}
                    </Col>
                    <Col md={4} sm={12} xs={12}>
                      {data.project.hasForces ? (
                        <IndicatorBox
                          icon="authors"
                          name={translate.t("search_findings.tab_indicators.forces.indicators.strictness.title")}
                          quantity={securityCommitment}
                          onClick={goToProjectForces}
                          title=""
                          total={translate.t("search_findings.tab_indicators.forces.indicators.strictness.total")}
                          description={
                            translate.t("search_findings.tab_indicators.forces.indicators.strictness.strict_desc")}
                          small={true}
                        />
                      ) : (
                        <React.Fragment />
                      )}
                    </Col>
                  </Col>
                </Row>

              </React.StrictMode>
            );
          } else { return <React.Fragment />; }
        }}
    </Query>
  );
};

export { forcesIndicatorsView as ForcesIndicatorsView };
