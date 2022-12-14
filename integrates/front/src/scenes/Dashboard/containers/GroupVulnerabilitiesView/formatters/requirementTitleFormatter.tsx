import _ from "lodash";
import React, { useCallback, useState } from "react";
import type { ReactElement } from "react";
import { useTranslation } from "react-i18next";

import type { IReqFormatProps } from "./types";

import { Container } from "components/Container";
import { ExternalLink } from "components/ExternalLink";
import { Col, Row } from "components/Layout";

const CRITERIA_TEXT_SLICE: number = 5;

const RequirementsTitleFormat: React.FC<IReqFormatProps> = ({
  reqsList,
}: IReqFormatProps): JSX.Element => {
  const [collapsed, setCollapsed] = useState(true);
  const { t } = useTranslation();

  const handleClick = useCallback(
    (event: React.MouseEvent<HTMLElement>): void => {
      event.stopPropagation();
      setCollapsed(!collapsed);
    },
    [collapsed]
  );

  if (_.isNil(reqsList) || _.isEmpty(reqsList)) return <div />;

  return (
    <React.StrictMode>
      <Container minWidth={"300px"} scroll={"none"}>
        <Col>
          {collapsed ? (
            <Row>
              <div>{reqsList[0].slice(CRITERIA_TEXT_SLICE)}</div>
            </Row>
          ) : (
            reqsList.map((req: string): ReactElement => {
              return (
                <div key={req}>
                  <Row>
                    <div>{req.slice(CRITERIA_TEXT_SLICE)}</div>
                  </Row>
                </div>
              );
            })
          )}
          <br />
          {reqsList.length > 1 ? (
            <ExternalLink onClick={handleClick}>
              {collapsed
                ? t("group.findings.description.showMore")
                : t("group.findings.description.showLess")}
            </ExternalLink>
          ) : undefined}
        </Col>
      </Container>
    </React.StrictMode>
  );
};

const requirementsTitleFormatter = ({
  reqsList,
}: IReqFormatProps): JSX.Element => {
  return <RequirementsTitleFormat reqsList={reqsList} />;
};

export { RequirementsTitleFormat, requirementsTitleFormatter };
