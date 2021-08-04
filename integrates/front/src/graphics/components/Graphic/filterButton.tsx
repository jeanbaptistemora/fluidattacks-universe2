/* eslint-disable react/forbid-component-props
  --------
  We need className to override default styles
  */
import React from "react";

import { mergedDocuments } from "./ctx";
import { DropdownFilter } from "./filter";
import { DaysLabel, DocumentMerged } from "./helpers";

import styles from "graphics/components/Graphic/index.css";
import { GraphicButton } from "styles/styledComponents";

interface IFilterButton {
  subjectName: string;
  subject: string;
  documentName: string;
  currentDocumentName: string;
  timeFilter: boolean;
  documentNameFilter: boolean;
  changeToAlternative: () => void;
  changeTothirtyDays: () => void;
  changeToNinety: () => void;
  changeToAll: () => void;
  changeToDefault: () => void;
}

export const FilterButton: React.FC<IFilterButton> = ({
  subjectName,
  subject,
  documentName,
  currentDocumentName,
  timeFilter,
  documentNameFilter,
  changeToAlternative,
  changeTothirtyDays,
  changeToNinety,
  changeToAll,
  changeToDefault,
}: IFilterButton): JSX.Element => (
  <React.StrictMode>
    {documentNameFilter || timeFilter ? (
      <DropdownFilter>
        <React.Fragment>
          {documentNameFilter ? (
            <React.Fragment>
              <GraphicButton
                className={styles.buttonSize}
                onClick={changeToDefault}
              >
                <DocumentMerged
                  isEqual={documentName === currentDocumentName}
                  label={mergedDocuments[documentName].default.label}
                  tooltip={mergedDocuments[documentName].default.tooltip}
                />
              </GraphicButton>
              <GraphicButton
                className={styles.buttonSize}
                onClick={changeToAlternative}
              >
                <DocumentMerged
                  isEqual={
                    mergedDocuments[documentName].documentName ===
                    currentDocumentName
                  }
                  label={mergedDocuments[documentName].alt.label}
                  tooltip={mergedDocuments[documentName].alt.tooltip}
                />
              </GraphicButton>
            </React.Fragment>
          ) : undefined}
          {timeFilter ? (
            <React.Fragment>
              <GraphicButton
                className={styles.buttonSize}
                onClick={changeTothirtyDays}
              >
                <DaysLabel
                  days={"30"}
                  isEqual={subjectName === `${subject}_30`}
                />
              </GraphicButton>
              <GraphicButton
                className={styles.buttonSize}
                onClick={changeToNinety}
              >
                <DaysLabel
                  days={"90"}
                  isEqual={subjectName === `${subject}_90`}
                />
              </GraphicButton>
              <GraphicButton
                className={styles.buttonSize}
                onClick={changeToAll}
              >
                <DaysLabel days={"allTime"} isEqual={subjectName === subject} />
              </GraphicButton>
            </React.Fragment>
          ) : undefined}
        </React.Fragment>
      </DropdownFilter>
    ) : undefined}
  </React.StrictMode>
);
