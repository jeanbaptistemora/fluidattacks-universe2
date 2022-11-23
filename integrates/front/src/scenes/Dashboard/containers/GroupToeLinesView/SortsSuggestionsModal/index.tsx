import _ from "lodash";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";

import { Field, Label, Value } from "../styles";
import type { ISortsSuggestionAttr } from "../types";
import { Col, Row } from "components/Layout";
import { Modal } from "components/Modal";

interface ISortsSuggestionsModal {
  closeSortsSuggestionsModal: () => void;
  isSortsSuggestionsOpen: boolean;
  selectedSortsSuggestions: ISortsSuggestionAttr[] | undefined;
}

const SortsSuggestionsModal: React.FC<ISortsSuggestionsModal> = ({
  closeSortsSuggestionsModal,
  isSortsSuggestionsOpen,
  selectedSortsSuggestions,
}: ISortsSuggestionsModal): JSX.Element => {
  const { t } = useTranslation();

  const onClose: () => void = useCallback((): void => {
    closeSortsSuggestionsModal();
  }, [closeSortsSuggestionsModal]);

  if (
    _.isUndefined(selectedSortsSuggestions) ||
    _.isEmpty(selectedSortsSuggestions)
  ) {
    return <div />;
  }

  const sortsSuggestionsItems: JSX.Element[] = selectedSortsSuggestions.map(
    (item: ISortsSuggestionAttr): JSX.Element => {
      return (
        <Row key={item.findingTitle}>
          <Col lg={80} md={80} sm={80}>
            <Field>
              <Label>{item.findingTitle}</Label>
            </Field>
          </Col>
          <Col lg={20} md={20} sm={20}>
            <Value>{`${item.probability} %`}</Value>
          </Col>
        </Row>
      );
    }
  );

  return (
    <React.StrictMode>
      <Modal
        onClose={onClose}
        open={isSortsSuggestionsOpen}
        title={<h4>{t("group.toe.lines.sortsSuggestions")}</h4>}
      >
        {sortsSuggestionsItems}
      </Modal>
    </React.StrictMode>
  );
};

export { SortsSuggestionsModal };
