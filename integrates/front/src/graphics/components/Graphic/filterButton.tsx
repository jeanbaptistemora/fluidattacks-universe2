/* eslint-disable react/forbid-component-props, react/no-multi-comp
--------
  We need className to override default styles
  Needed to declare various small helpers components
*/
import React, { useMemo } from "react";
import { useTranslation } from "react-i18next";

import type { IDocumentValues } from "./ctx";
import { mergedDocuments } from "./ctx";
import { DropdownFilter } from "./filter";
import { DaysLabel, DocumentMerged } from "./helpers";

import { TooltipWrapper } from "components/TooltipWrapper";
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
  changeToAlternative: (index: number) => void;
  changeToDefault: () => void;
}

interface IGButton {
  alternative: IDocumentValues;
  changeToAlternative: (index: number) => void;
  currentDocumentName: string;
  index: number;
}

const GButton: React.FC<IGButton> = ({
  alternative,
  changeToAlternative,
  currentDocumentName,
  index,
}: IGButton): JSX.Element => {
  function onClick(): void {
    changeToAlternative(index);
  }

  return (
    <TooltipWrapper
      id={alternative.tooltip.split(" ").join("_")}
      message={alternative.tooltip}
    >
      <GraphicButton className={styles.buttonSize} onClick={onClick}>
        <DocumentMerged
          isEqual={alternative.documentName === currentDocumentName}
          label={alternative.label}
        />
      </GraphicButton>
    </TooltipWrapper>
  );
};

const TimeFilterButton: React.FC<ITimeFilterButton> = ({
  subjectName,
  subject,
  timeFilter,
  changeToThirtyDays,
  changeToNinety,
  changeToAll,
}: ITimeFilterButton): JSX.Element => {
  const { t } = useTranslation();
  if (!timeFilter) {
    return <React.StrictMode />;
  }

  return (
    <React.StrictMode>
      <TooltipWrapper
        id={"analytics.limitData.thirtyDays.tooltip.id"}
        message={t("analytics.limitData.thirtyDays.tooltip")}
      >
        <GraphicButton
          className={styles.buttonSize}
          onClick={changeToThirtyDays}
        >
          <DaysLabel days={"30"} isEqual={subjectName === `${subject}_30`} />
        </GraphicButton>
      </TooltipWrapper>
      <TooltipWrapper
        id={"analytics.limitData.ninetyDays.tooltip.id"}
        message={t("analytics.limitData.ninetyDays.tooltip")}
      >
        <GraphicButton className={styles.buttonSize} onClick={changeToNinety}>
          <DaysLabel days={"90"} isEqual={subjectName === `${subject}_90`} />
        </GraphicButton>
      </TooltipWrapper>
      <TooltipWrapper
        id={"analytics.limitData.all.tooltip.id"}
        message={t("analytics.limitData.all.tooltip")}
      >
        <GraphicButton className={styles.buttonSize} onClick={changeToAll}>
          <DaysLabel days={"allTime"} isEqual={subjectName === subject} />
        </GraphicButton>
      </TooltipWrapper>
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
  const tooltip: string = useMemo(
    (): string => mergedDocuments[documentName].default.tooltip,
    [documentName]
  );

  if (!documentNameFilter) {
    return <React.StrictMode />;
  }

  return (
    <React.StrictMode>
      <TooltipWrapper id={tooltip.split(" ").join("_")} message={tooltip}>
        <GraphicButton className={styles.buttonSize} onClick={changeToDefault}>
          <DocumentMerged
            isEqual={documentName === currentDocumentName}
            label={mergedDocuments[documentName].default.label}
          />
        </GraphicButton>
      </TooltipWrapper>
      {mergedDocuments[documentName].alt.map(
        (alternative: IDocumentValues, index: number): JSX.Element => (
          <GButton
            alternative={alternative}
            changeToAlternative={changeToAlternative}
            currentDocumentName={currentDocumentName}
            index={index}
            key={alternative.documentName}
          />
        )
      )}
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
