import { useQuery } from "@apollo/react-hooks";
import _ from "lodash";
import React from "react";
import { Col, Row } from "react-bootstrap";
import { RouteComponentProps } from "react-router-dom";
import { IStatusGraph, ITreatmentGraph, statusGraph, treatmentGraph } from "../../../../../utils/formatHelpers";
import translate from "../../../../../utils/translations/translate";
import { IndicatorGraph } from "../../../components/IndicatorGraph";
import { default as style } from "./index.css";
import { TAG_QUERY } from "./queries";

type TagsProps = RouteComponentProps<{ tagName: string }>;
interface ITag {
  tag: {
    name: string;
    projects: ITreatmentGraph[];
  };
}
const tagsInfo: React.FC<TagsProps> = (props: TagsProps): JSX.Element => {
  const { tagName } = props.match.params;
  const { data } = useQuery<ITag>(TAG_QUERY, { variables: { tag: tagName }});

  const formatStatusGraphData: ((projects: ITreatmentGraph[]) => IStatusGraph) = (
    projects: ITreatmentGraph[],
  ): IStatusGraph => {
    const closedVulnerabilities: number = projects.reduce(
      (acc: number, project: ITreatmentGraph) => (acc + project.closedVulnerabilities), 0);
    const openVulnerabilities: number = projects.reduce(
      (acc: number, project: ITreatmentGraph) => (acc + project.openVulnerabilities), 0);

    return { closedVulnerabilities, openVulnerabilities };
  };

  const formatTreatmentGraphData: ((projects: ITreatmentGraph[]) => ITreatmentGraph) = (
    projects: ITreatmentGraph[],
  ): ITreatmentGraph => {
    const totalTreatment: Dictionary<number> = projects.reduce(
      (acc: Dictionary<number>, project: ITreatmentGraph) => {
        const projectTreatment: Dictionary<number> = JSON.parse(project.totalTreatment);

        return ({
          accepted: acc.accepted + projectTreatment.accepted,
          inProgress: acc.inProgress + projectTreatment.inProgress,
          undefined: acc.undefined + projectTreatment.undefined,
        });
      },
      { accepted: 0, inProgress: 0, undefined: 0 });

    return { totalTreatment: JSON.stringify(totalTreatment), ...formatStatusGraphData(projects) };
  };

  if (_.isUndefined(data) || _.isEmpty(data)) { return <React.Fragment />; }

  return (
    <React.Fragment>
      <Row>
        <Col md={6} sm={12} xs={12}>
          <Col md={12} sm={12} xs={12} className={style.box_size}>
            <IndicatorGraph
              data={statusGraph(formatStatusGraphData(data.tag.projects))}
              name={translate.t("search_findings.tab_indicators.status_graph")}
            />
          </Col>
        </Col>
        <Col md={6} sm={12} xs={12}>
          <Col md={12} sm={12} xs={12} className={style.box_size}>
            <IndicatorGraph
              data={treatmentGraph(formatTreatmentGraphData(data.tag.projects))}
              name={translate.t("search_findings.tab_indicators.treatment_graph")}
            />
          </Col>
        </Col>
      </Row>
    </React.Fragment>
  );
};

export { tagsInfo as TagsInfo };
