import React from "react";
import { useTranslation } from "react-i18next";

import type { IClosingDateFieldProps } from "./types";

import { InfoField, Label, LabelField, Row } from "../../styles";
import { Value } from "../../value";

const ClosingDateField: React.FC<IClosingDateFieldProps> = ({
  vulnerability,
  vulnerabilityAdditionalInfo,
}: IClosingDateFieldProps): JSX.Element => {
  const { t } = useTranslation();

  return (
    <React.StrictMode>
      <Row>
        <LabelField>
          <Label>{t("searchFindings.tabVuln.vulnTable.closingDate")}</Label>
        </LabelField>
        <InfoField>
          <Value
            value={
              vulnerability.currentState === "closed"
                ? vulnerabilityAdditionalInfo.lastStateDate.split(" ")[0]
                : ""
            }
          />
        </InfoField>
      </Row>
    </React.StrictMode>
  );
};

export { ClosingDateField };
