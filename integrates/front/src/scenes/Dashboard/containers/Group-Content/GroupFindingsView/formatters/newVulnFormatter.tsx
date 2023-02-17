import React from "react";

import { LittleFlag } from "./styles";

import { Container } from "components/Container";
import { Text } from "components/Text";
import type { IFindingAttr } from "scenes/Dashboard/containers/Group-Content/GroupFindingsView/types";

export function newVulnFormatter(finding: IFindingAttr): JSX.Element {
  if (finding.lastVulnerability <= 7 && finding.openVulnerabilities > 0) {
    return (
      <Container display={"inline-block"}>
        <Container align={"center"} display={"flex"}>
          <Text disp={"inline-block"} mr={1}>
            {finding.title}
          </Text>
          <LittleFlag>{"New"}</LittleFlag>
        </Container>
      </Container>
    );
  }

  return <Text disp={"inline-block"}>{finding.title}</Text>;
}
