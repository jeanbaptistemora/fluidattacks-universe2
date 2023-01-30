import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";

import { DisplayImage } from "./DisplayImage";
import { EvidenceForm } from "./EvidenceForm";
import { DescriptionContainer, ImageContainer } from "./styles";

import { Col33, EvidenceDescription, Row } from "styles/styledComponents";
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
      <Col33>
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
      </Col33>
    </React.StrictMode>
  );
};

export { EvidenceImage };
export type { IEvidenceImageProps };
