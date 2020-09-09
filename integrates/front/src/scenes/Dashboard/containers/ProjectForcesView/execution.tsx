/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for the sake of readability
 */

// Third parties imports
import { useQuery } from "@apollo/react-hooks";
import React, { ReactElement } from "react";
import { Col, Row } from "react-bootstrap";
// tslint:disable-next-line no-submodule-imports
import SyntaxHighlighter from "react-syntax-highlighter/dist/esm/light";
// tslint:disable-next-line no-submodule-imports
import { default as monokaiSublime } from "react-syntax-highlighter/dist/esm/styles/hljs/monokai-sublime";
import { statusFormatter } from "../../../../components/DataTableNext/formatters";

// Local imports
import { DataTableNext } from "../../../../components/DataTableNext/index";
import { IHeaderConfig } from "../../../../components/DataTableNext/types";
import { translate } from "../../../../utils/translations/translate";
import {
  IExecution,
  IExploitResult,
  IFoundVulnerabilities,
  IFoundVulnerabilitiesNew,
  IVulnerabilities,
  IVulnerabilitiesNew,
} from "./index";
import styles from "./index.css";
import { GET_FORCES_EXECUTION } from "./queries";

const modalExecution: React.FC<IExecution> = (
  props: Readonly<IExecution>,
): JSX.Element => {
  const isOld: boolean = props.log !== undefined;

  const { loading, data } = useQuery(GET_FORCES_EXECUTION, {
    skip: isOld,
    variables: {
      executionId: props.execution_id,
      projectName: props.projectName,
    },
  });
  if (loading && !isOld) {

    return <p>Loading ...</p>;
  }

  const execution: IExecution = isOld ? props : { ...props, ...data.forcesExecution };

  const formatText: ((text: string) => ReactElement<Text>) = (text: string): ReactElement<Text> =>
    <p className={styles.wrapped}>{text}</p>;

  const stateResolve: (status: string) => string = (status: string): string => {
    switch (status) {
      case "OPEN":
        return translate.t("group.forces.status.vulnerable");
      case "CLOSED":
        return translate.t("group.forces.status.secure");
      case "ACCEPTED":
        return translate.t("group.forces.status.accepted");
      default:
        return "";
    }
  };

  const getVulnerabilitySummaries: (
    foundVulnerabilities: IFoundVulnerabilities | IFoundVulnerabilitiesNew,
  ) => string = (
    foundVulnerabilities: IFoundVulnerabilities | IFoundVulnerabilitiesNew,
    ): string => {
      if ("exploitable" in foundVulnerabilities) {
        const exploitableTrans: string = translate.t(
          "group.forces.found_vulnerabilities.exploitable");
        const acceptedTrans: string = translate.t(
          "group.forces.found_vulnerabilities.accepted");
        const notExploitableTrans: string = translate.t(
          "group.forces.found_vulnerabilities.not_exploitable");
        const totalTrans: string = translate.t(
          "group.forces.found_vulnerabilities.total");

        const exploitableStr: string = `${foundVulnerabilities.exploitable} ${exploitableTrans}`;
        const acceptedStr: string = `${foundVulnerabilities.accepted} ${acceptedTrans}`;
        const notExploitableStr: string = `${foundVulnerabilities.notExploitable} ${notExploitableTrans}`;
        const totalStr: string = `${foundVulnerabilities.total} ${totalTrans}`;

        return `${exploitableStr}, ${acceptedStr}, ${notExploitableStr}, ${totalStr}`;
      } else {
        const openTrans: string = translate.t(
          "group.forces.found_vulnerabilities_new.open");
        const acceptedTrans: string = translate.t(
          "group.forces.found_vulnerabilities_new.accepted");
        const closedTrans: string = translate.t(
          "group.forces.found_vulnerabilities_new.closed");
        const totalTrans: string = translate.t(
          "group.forces.found_vulnerabilities_new.total");

        const openStr: string = `${foundVulnerabilities.open} ${openTrans}`;
        const acceptedStr: string = `${foundVulnerabilities.accepted} ${acceptedTrans}`;
        const closedStr: string = `${foundVulnerabilities.closed} ${closedTrans}`;
        const totalStr: string = `${foundVulnerabilities.total} ${totalTrans}`;

        return `${openStr}, ${acceptedStr}, ${closedStr}, ${totalStr}`;
      }
    };

  const getDatasetFromVulnerabilities: (
    vulnerabilities: IVulnerabilities | IVulnerabilitiesNew,
  ) => Dictionary[] = (
    vulnerabilities: IVulnerabilities | IVulnerabilitiesNew,
    ): Dictionary[] => {
      const vulns: IExploitResult[] =
        "exploits" in vulnerabilities
          ? vulnerabilities.exploits.concat(
            vulnerabilities.acceptedExploits.concat(
              vulnerabilities.integratesExploits,
            ),
          )
          : vulnerabilities.open.concat(
            vulnerabilities.closed.concat(vulnerabilities.accepted),
          );

      return vulns.map((elem: IExploitResult) => ({
        ...elem,
        state: statusFormatter(stateResolve(elem.state)),
      }));
    };

  const headersCompromisedToeTable: (
    vulnerabilities: IVulnerabilities | IVulnerabilitiesNew,
  ) => IHeaderConfig[] = (
    vulnerabilities: IVulnerabilities | IVulnerabilitiesNew,
    ) => [
        ...("open" in vulnerabilities
          ? [
            {
              dataField: "exploitability",
              formatter: formatText,
              header: translate.t("group.forces.compromised_toe.exploitability"),
              width: "15%",
              wrapped: true,
            },
            {
              dataField: "state",
              formatter: formatText,
              header: translate.t("group.forces.compromised_toe.status"),
              width: "10%",
              wrapped: true,
            },
          ]
          : []),
        {
          dataField: "kind",
          formatter: formatText,
          header: translate.t("group.forces.compromised_toe.type"),
          width: "10%",
          wrapped: true,
        },
        {
          dataField: "who",
          formatter: formatText,
          header: translate.t("group.forces.compromised_toe.what"),
          wrapped: true,
        },
        {
          dataField: "where",
          formatter: formatText,
          header: translate.t("group.forces.compromised_toe.where"),
          wrapped: true,
        },
      ];

  return (
    <div>
      <Row>
        <Col md={4}><p><b>{translate.t("group.forces.date")}</b></p></Col>
        <Col md={8}><p>{execution.date}</p></Col>
      </Row>
      <Row>
        <Col md={4}><p><b>{translate.t("group.forces.status.title")}</b></p></Col>
        <Col md={8}><p>{execution.status}</p></Col>
      </Row>
      <Row>
        <Col md={4}><p><b>{translate.t("group.forces.strictness.title")}</b></p></Col>
        <Col md={8}><p>{execution.strictness}</p></Col>
      </Row>
      <Row>
        <Col md={4}><p><b>{translate.t("group.forces.kind.title")}</b></p></Col>
        <Col md={8}><p>{execution.kind}</p></Col>
      </Row>
      <Row>
        <Col md={4}><p><b>{translate.t("group.forces.git_repo")}</b></p></Col>
        <Col md={8}><p>{execution.gitRepo}</p></Col>
      </Row>
      <Row>
        <Col md={4}><p><b>{translate.t("group.forces.identifier")}</b></p></Col>
        <Col md={8}><p>{execution.execution_id}</p></Col>
      </Row>
      <Row>
        <Col md={4}><p><b>{translate.t("group.forces.found_vulnerabilities.title")}</b></p></Col>
        <Col md={8}>
          <p className={styles.wrapped}>
            {getVulnerabilitySummaries(execution.foundVulnerabilities)}
          </p>
        </Col>
      </Row>
      <br />
      <DataTableNext
        bordered={true}
        dataset={getDatasetFromVulnerabilities(execution.vulnerabilities)}
        exportCsv={false}
        search={false}
        headers={headersCompromisedToeTable(execution.vulnerabilities)}
        id="tblCompromisedToe"
        pageSize={100}
      />
      <hr />

      <SyntaxHighlighter style={monokaiSublime} language="yaml" wrapLines={true}>
        {execution.log}
      </SyntaxHighlighter>

    </div>
  );
};

export { modalExecution as Execution };
