/* eslint-disable react/forbid-component-props, react/no-multi-comp
--------
  We need className to override default styles
  Needed to declare various small helpers components
*/
import React from "react";

import { mergedDocuments } from "./ctx";
import { DropdownFilter } from "./filter";
import { DaysLabel, DocumentMerged } from "./helpers";

import styles from "graphics/components/Graphic/index.css";
import { GraphicButton } from "styles/styledComponents";

interface ITimeFilterButton {
  subjectName: string;
  subject: string;
  timeFilter: boolean;
  changeToThirtyDays: () => void;
  changeToNinety: () => void;
  changeToAll: () => void;
}

interface ITypeFilterButton {
  documentName: string;
  currentDocumentName: string;
  documentNameFilter: boolean;
  changeToAlternative: () => void;
  changeToDefault: () => void;
}

const TimeFilterButton: React.FC<ITimeFilterButton> = ({
  subjectName,
  subject,
  timeFilter,
  changeToThirtyDays,
  changeToNinety,
  changeToAll,
}: ITimeFilterButton): JSX.Element => {
  if (!timeFilter) {
    return <React.StrictMode />;
  }

  return (
    <React.StrictMode>
      <GraphicButton className={styles.buttonSize} onClick={changeToThirtyDays}>
        <DaysLabel days={"30"} isEqual={subjectName === `${subject}_30`} />
      </GraphicButton>
      <GraphicButton className={styles.buttonSize} onClick={changeToNinety}>
        <DaysLabel days={"90"} isEqual={subjectName === `${subject}_90`} />
      </GraphicButton>
      <GraphicButton className={styles.buttonSize} onClick={changeToAll}>
        <DaysLabel days={"allTime"} isEqual={subjectName === subject} />
      </GraphicButton>
    </React.StrictMode>
  );
};

const TypeFilterButton: React.FC<ITypeFilterButton> = ({
  documentName,
  currentDocumentName,
  documentNameFilter,
  changeToAlternative,
  changeToDefault,
}: ITypeFilterButton): JSX.Element => {
  if (!documentNameFilter) {
    return <React.StrictMode />;
  }

  return (
    <React.StrictMode>
      <GraphicButton className={styles.buttonSize} onClick={changeToDefault}>
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
            mergedDocuments[documentName].documentName === currentDocumentName
          }
          label={mergedDocuments[documentName].alt.label}
          tooltip={mergedDocuments[documentName].alt.tooltip}
        />
      </GraphicButton>
    </React.StrictMode>
  );
};

export const FilterButton: React.FC<ITimeFilterButton & ITypeFilterButton> = ({
  subjectName,
  subject,
  documentName,
  currentDocumentName,
  timeFilter,
  documentNameFilter,
  changeToAlternative,
  changeToThirtyDays,
  changeToNinety,
  changeToAll,
  changeToDefault,
}: ITimeFilterButton & ITypeFilterButton): JSX.Element => (
  <React.StrictMode>
    {documentNameFilter || timeFilter ? (
      <DropdownFilter>
        <React.Fragment>
          <TypeFilterButton
            changeToAlternative={changeToAlternative}
            changeToDefault={changeToDefault}
            currentDocumentName={currentDocumentName}
            documentName={documentName}
            documentNameFilter={documentNameFilter}
          />
          <TimeFilterButton
            changeToAll={changeToAll}
            changeToNinety={changeToNinety}
            changeToThirtyDays={changeToThirtyDays}
            subject={subject}
            subjectName={subjectName}
            timeFilter={timeFilter}
          />
        </React.Fragment>
      </DropdownFilter>
    ) : undefined}
  </React.StrictMode>
);
