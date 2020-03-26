import { useQuery } from "@apollo/react-hooks";
import _ from "lodash";
import React from "react";
import { Col, Row } from "react-bootstrap";
import { RouteComponentProps } from "react-router-dom";
import { IStatusGraph, statusGraph } from "../../../../../utils/formatHelpers";
import translate from "../../../../../utils/translations/translate";
import { IndicatorGraph } from "../../../components/IndicatorGraph";
import { default as style } from "./index.css";
import { TAG_QUERY } from "./queries";

type TagsProps = RouteComponentProps<{ tagName: string }>;
interface ITag {
  tag: {
    name: string;
    projects: IStatusGraph[];
  };
}
const tagsInfo: React.FC<TagsProps> = (props: TagsProps): JSX.Element => {
  const { tagName } = props.match.params;
  const { data } = useQuery<ITag>(TAG_QUERY, { variables: { tag: tagName }});

  const  formatStatusGraphData: ((projects: IStatusGraph[]) => IStatusGraph) = (
    projects: IStatusGraph[],
  ): IStatusGraph => {
    const closedVulnerabilities: number = projects.reduce(
      (acc: number, project: IStatusGraph) => (acc + project.closedVulnerabilities), 0);
    const openVulnerabilities: number = projects.reduce(
      (acc: number, project: IStatusGraph) => (acc + project.openVulnerabilities), 0);

    return { closedVulnerabilities, openVulnerabilities };
  };

  if (_.isUndefined(data) || _.isEmpty(data)) { return <React.Fragment />; }

  return (
    <React.Fragment>
      <Row>
        <Col mdOffset={4} md={8} sm={12} xs={12}>
          <Col md={12} sm={12} xs={12} className={style.box_size}>
            <IndicatorGraph
              data={statusGraph(formatStatusGraphData(data.tag.projects))}
              name={translate.t("search_findings.tab_indicators.status_graph")}
            />
          </Col>
        </Col>
      </Row>
    </React.Fragment>
  );
};

export { tagsInfo as TagsInfo };
