/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { FC } from "react";
import React from "react";

import { getProgressBarColor } from "../utils";
import { Card } from "components/Card";
import { InfoDropdown } from "components/InfoDropdown";
import { Col } from "components/Layout/Col";
import { Row } from "components/Layout/Row";
import { ProgressBar } from "components/ProgressBar";
import { Text } from "components/Text";

interface IPercentageCardProps {
  info: string;
  percentage: number;
  title: string;
}

const PercentageCard: FC<IPercentageCardProps> = (
  props: IPercentageCardProps
): JSX.Element => {
  const { info, percentage, title } = props;

  return (
    <Card>
      <Row>
        <Text size={"small"} ta={"center"}>
          {title} <InfoDropdown>{info}</InfoDropdown>
        </Text>
      </Row>
      <Row>
        <Row justify={"center"}>
          <Col lg={50} md={50} sm={50}>
            <Text fw={9} size={"big"} ta={"end"} ws={"nowrap"}>
              {`${percentage}%`}
            </Text>
          </Col>
          <Col lg={50} md={50} sm={50}>
            <div className={"flex flex-column h-100 justify-center "}>
              <ProgressBar
                height={10}
                maxWidth={37}
                percentage={percentage}
                progressColor={getProgressBarColor(percentage)}
              />
            </div>
          </Col>
        </Row>
      </Row>
    </Card>
  );
};
export { PercentageCard };
