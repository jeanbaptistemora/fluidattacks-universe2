import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";

import { Col, Row } from "components/Layout";
import { DisplayImage } from "scenes/Dashboard/components/EvidenceImage/DisplayImage";
import { EvidenceForm } from "scenes/Dashboard/components/EvidenceImage/EvidenceForm";
import {
  DescriptionContainer,
  ImageContainer,
} from "scenes/Dashboard/components/EvidenceImage/styles";
import { EvidenceDescription } from "styles/styledComponents";
import { getFileNameExtension } from "utils/validations";

interface IEvidenceImageProps {
  acceptedMimes?: string;
  content: string;
  date?: string;
  description: string;
  isDescriptionEditable: boolean;
  isEditing: boolean;
  isRemovable?: boolean;
  name: string;
  validate?: (value: unknown) => string | undefined;
  onClick: () => void;
  onDelete?: () => void;
}

const EvidenceImage: React.FC<Readonly<IEvidenceImageProps>> = (
  props
): JSX.Element => {
  const { content, isEditing, description, date, name, onClick } = props;
  const { t } = useTranslation();

  return (
    <React.StrictMode>
      <Col lg={33} md={50} sm={100}>
        <div>
          <ImageContainer>
            <DisplayImage
              content={content}
              extension={getFileNameExtension(content)}
              name={name}
              onClick={onClick}
            />
          </ImageContainer>
          <DescriptionContainer>
            <Row>
              <label>
                <b>{t("searchFindings.tabEvidence.detail")}</b>
              </label>
            </Row>
            <Row>
              {isEditing ? (
                // eslint-disable-next-line react/jsx-props-no-spreading
                <EvidenceForm {...props} />
              ) : (
                <React.Fragment>
                  <EvidenceDescription>{description}</EvidenceDescription>
                  {_.isEmpty(date) ? undefined : (
                    <EvidenceDescription>
                      {t("searchFindings.tabEvidence.date")}&nbsp;
                      {date?.split(" ")[0]}
                    </EvidenceDescription>
                  )}
                </React.Fragment>
              )}
            </Row>
          </DescriptionContainer>
        </div>
      </Col>
    </React.StrictMode>
  );
};

export { EvidenceImage };
export type { IEvidenceImageProps };
