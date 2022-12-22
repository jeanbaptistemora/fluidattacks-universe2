import React from "react";

import {
  BoldColor,
  ComparativeTable,
  Container,
  HeadCol,
  TableCol,
  TableContainer,
  TableDescription,
  TableRow,
} from "./styledComponents";

import { translate } from "../../../utils/translations/translate";
import { Paragraph, Title } from "../../Texts";

const Comparative: React.FC = (): JSX.Element => {
  return (
    <Container>
      <Title fColor={"#2e2e38"} fSize={"36"} marginBottom={"4"}>
        {translate.t("plansPage.comparative.title")}
      </Title>
      <TableContainer>
        <ComparativeTable>
          <thead>
            <TableRow>
              <HeadCol />
              <HeadCol>
                <Title fColor={"#f4f4f6"} fSize={"20"}>
                  {"Fluid Attacks"}
                </Title>
              </HeadCol>
              <HeadCol>
                <Title fColor={"#f4f4f6"} fSize={"20"}>
                  {"Competition"}
                </Title>
              </HeadCol>
            </TableRow>
          </thead>
          <tbody>
            <TableRow>
              <TableCol>
                <Title fColor={"#2e2e38"} fSize={"20"}>
                  {"Accuracy"}
                </Title>
              </TableCol>
              <TableCol>
                <Paragraph fColor={"#5c5c70"} fSize={"16"}>
                  {
                    "Our combination of technology and human expertise substantially "
                  }
                  <BoldColor fColor={"#5c5c70"}>
                    {"reduces false positives and false negatives."}
                  </BoldColor>
                </Paragraph>
              </TableCol>
              <TableCol>
                <Paragraph fColor={"#5c5c70"} fSize={"16"}>
                  {
                    "Most solutions rely on automated tools with a false positive rate near 35% and a false negative rate up to "
                  }
                  <BoldColor fColor={"#b80000"}>{"80%*"}</BoldColor>
                </Paragraph>
              </TableCol>
            </TableRow>

            <TableRow>
              <TableCol>
                <Title fColor={"#2e2e38"} fSize={"20"}>
                  {"Accuracy (OWASP Benchmark)"}
                </Title>
              </TableCol>
              <TableCol>
                <Paragraph fColor={"#5c5c70"} fSize={"16"}>
                  {"Our SAST solution achieved a "}
                  <BoldColor fColor={"#5c5c70"}>
                    {"True Positive Rate (TPR) of 100% "}
                  </BoldColor>
                  {"and a "}
                  <BoldColor fColor={"#5c5c70"}>
                    {"False Positive Rate (FPR) of 0% "}
                  </BoldColor>
                  {"against the OWASP Benchmark (read here)."}
                </Paragraph>
              </TableCol>
              <TableCol>
                <Paragraph fColor={"#5c5c70"} fSize={"16"}>
                  {"Other solutions show lower TPR and higher FPR."}
                </Paragraph>
              </TableCol>
            </TableRow>

            <TableRow>
              <TableCol>
                <Title fColor={"#2e2e38"} fSize={"20"}>
                  {"All-in-one"}
                </Title>
              </TableCol>
              <TableCol>
                <Paragraph fColor={"#5c5c70"} fSize={"16"}>
                  {"We provide "}
                  <BoldColor fColor={"#5c5c70"}>
                    {"comprehensive testing in a single solution"}
                  </BoldColor>
                  {", including SAST, DAST, SCA, manual pentesting, "}
                  <BoldColor fColor={"#b80000"}>
                    {"reverse engineering*"}
                  </BoldColor>
                  {", and real attack simulations."}
                </Paragraph>
              </TableCol>
              <TableCol>
                <Paragraph fColor={"#5c5c70"} fSize={"16"}>
                  {"Limited to a few techniques and sold separately."}
                </Paragraph>
              </TableCol>
            </TableRow>
          </tbody>
        </ComparativeTable>
      </TableContainer>
      <TableDescription>
        <Paragraph fColor={"#5c5c70"} fSize={"16"}>
          {translate.t("plansPage.comparative.tableDescription1")}
        </Paragraph>
        <Paragraph fColor={"#5c5c70"} fSize={"16"}>
          {translate.t("plansPage.comparative.tableDescription2")}
        </Paragraph>
      </TableDescription>
    </Container>
  );
};

export { Comparative };
