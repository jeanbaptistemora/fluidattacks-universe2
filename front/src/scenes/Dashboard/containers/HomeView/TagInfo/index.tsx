import { useQuery } from "@apollo/react-hooks";
import _ from "lodash";
import React from "react";
import { ButtonToolbar, Col, Row } from "react-bootstrap";
import { Button } from "../../../../../components/Button";
import { Modal } from "../../../../../components/Modal";
import { IStatusGraph, statusGraph } from "../../../../../utils/formatHelpers";
import translate from "../../../../../utils/translations/translate";
import { IndicatorGraph } from "../../../components/IndicatorGraph";
import { default as style } from "./index.css";
import { TAG_QUERY } from "./queries";

interface ITagsProps {
  isOpen: boolean;
  tag: string;
  onClose(): void;
}
interface ITag {
  tag: {
    name: string;
    projects: IStatusGraph[];
  };
}
const tagsInfo: React.FC<ITagsProps> = (props: ITagsProps): JSX.Element => {
  const { tag, onClose, isOpen } = props;
  const { data } = useQuery<ITag>(TAG_QUERY, { variables: {tag }});

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
      <Modal
        open={isOpen}
        onClose={onClose}
        headerTitle={tag}
        footer={<div />}
      >
        <Row>
          <Col mdOffset={2} md={8} sm={12} xs={12}>
            <Col md={12} sm={12} xs={12} className={style.box_size}>
              <IndicatorGraph
                data={statusGraph(formatStatusGraphData(data.tag.projects))}
                name={translate.t("search_findings.tab_indicators.status_graph")}
              />
            </Col>
          </Col>
        </Row>
        <ButtonToolbar className="pull-right">
          <Button bsStyle="success" onClick={onClose}>
            {translate.t("project.findings.report.modal_close")}
          </Button>
        </ButtonToolbar>
      </Modal>
    </React.Fragment>
  );
};

export { tagsInfo as TagsInfo };
