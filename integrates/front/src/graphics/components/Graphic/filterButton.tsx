/* eslint-disable react/forbid-component-props, react/no-multi-comp
--------
  We need className to override default styles
  Needed to declare various small helpers components
*/
import React, { useCallback, useMemo } from "react";
import { useTranslation } from "react-i18next";

import type { IDocumentValues } from "./ctx";
import { mergedDocuments } from "./ctx";
import { DropdownFilter } from "./filter";
import { DaysLabel, DocumentMerged } from "./helpers";

import { Tooltip } from "components/Tooltip";
import styles from "graphics/components/Graphic/index.css";
import { GraphicButton } from "styles/styledComponents";

interface ITimeFilterButton {
  shouldDisplayAll: boolean | undefined;
  subjectName: string;
  subject: string;
  timeFilter: boolean;
  changeToThirtyDays: () => void;
  changeToOneHundredEighty: (() => void) | undefined;
  changeToSixtyDays: (() => void) | undefined;
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
  const onClick = useCallback((): void => {
    changeToAlternative(index);
  }, [changeToAlternative, index]);

  return (
    <Tooltip
      id={alternative.tooltip.split(" ").join("_")}
      tip={alternative.tooltip}
    >
      <GraphicButton className={styles.buttonSize} onClick={onClick}>
        <DocumentMerged
          isEqual={alternative.documentName === currentDocumentName}
          label={alternative.label}
        />
      </GraphicButton>
    </Tooltip>
  );
};

const TimeFilterButton: React.FC<ITimeFilterButton> = ({
  shouldDisplayAll = true,
  subjectName,
  subject,
  timeFilter,
  changeToThirtyDays,
  changeToSixtyDays = undefined,
  changeToNinety,
  changeToOneHundredEighty = undefined,
  changeToAll,
}: ITimeFilterButton): JSX.Element => {
  const { t } = useTranslation();
  if (!timeFilter) {
    return <React.StrictMode />;
  }

  return (
    <React.StrictMode>
      <Tooltip
        id={"analytics.limitData.thirtyDays.tooltip.id"}
        tip={t("analytics.limitData.thirtyDays.tooltip")}
      >
        <GraphicButton
          className={styles.buttonSize}
          onClick={changeToThirtyDays}
        >
          <DaysLabel
            days={"30"}
            isEqual={
              shouldDisplayAll
                ? subjectName === `${subject}_30`
                : subjectName === subject
            }
          />
        </GraphicButton>
      </Tooltip>
      {changeToSixtyDays !== undefined && (
        <Tooltip
          id={"analytics.limitData.sixtyDays.tooltip.id"}
          tip={t("analytics.limitData.sixtyDays.tooltip")}
        >
          <GraphicButton
            className={styles.buttonSize}
            onClick={changeToSixtyDays}
          >
            <DaysLabel days={"60"} isEqual={subjectName === `${subject}_60`} />
          </GraphicButton>
        </Tooltip>
      )}
      <Tooltip
        id={"analytics.limitData.ninetyDays.tooltip.id"}
        tip={t("analytics.limitData.ninetyDays.tooltip")}
      >
        <GraphicButton className={styles.buttonSize} onClick={changeToNinety}>
          <DaysLabel days={"90"} isEqual={subjectName === `${subject}_90`} />
        </GraphicButton>
      </Tooltip>
      {changeToOneHundredEighty !== undefined && (
        <Tooltip
          id={"analytics.limitData.oneHundredEighty.tooltip.id"}
          tip={t("analytics.limitData.oneHundredEighty.tooltip")}
        >
          <GraphicButton
            className={styles.buttonSize}
            onClick={changeToOneHundredEighty}
          >
            <DaysLabel
              days={"180"}
              isEqual={subjectName === `${subject}_180`}
            />
          </GraphicButton>
        </Tooltip>
      )}
      {shouldDisplayAll && (
        <Tooltip
          id={"analytics.limitData.all.tooltip.id"}
          tip={t("analytics.limitData.all.tooltip")}
        >
          <GraphicButton className={styles.buttonSize} onClick={changeToAll}>
            <DaysLabel days={"allTime"} isEqual={subjectName === subject} />
          </GraphicButton>
        </Tooltip>
      )}
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
    (): string =>
      documentNameFilter ? mergedDocuments[documentName].default.tooltip : "",
    [documentName, documentNameFilter]
  );

  if (!documentNameFilter) {
    return <React.StrictMode />;
  }

  return (
    <React.StrictMode>
      <Tooltip id={tooltip.split(" ").join("_")} tip={tooltip}>
        <GraphicButton className={styles.buttonSize} onClick={changeToDefault}>
          <DocumentMerged
            isEqual={documentName === currentDocumentName}
            label={mergedDocuments[documentName].default.label}
          />
        </GraphicButton>
      </Tooltip>
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
  shouldDisplayAll = true,
  subjectName,
  subject,
  documentName,
  currentDocumentName,
  timeFilter,
  documentNameFilter,
  changeToAlternative,
  changeToThirtyDays,
  changeToSixtyDays = undefined,
  changeToNinety,
  changeToOneHundredEighty = undefined,
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
            changeToOneHundredEighty={changeToOneHundredEighty}
            changeToSixtyDays={changeToSixtyDays}
            changeToThirtyDays={changeToThirtyDays}
            shouldDisplayAll={shouldDisplayAll}
            subject={subject}
            subjectName={subjectName}
            timeFilter={timeFilter}
          />
        </React.Fragment>
      </DropdownFilter>
    ) : undefined}
  </React.StrictMode>
);
