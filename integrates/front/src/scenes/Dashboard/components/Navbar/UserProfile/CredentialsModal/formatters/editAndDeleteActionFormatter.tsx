import { faPen, faTrashAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import { ConfirmDialog } from "components/ConfirmDialog";
import type { IHeaderConfig } from "components/Table/types";
import { translate } from "utils/translations/translate";

const ActionButton: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs(
  (): Partial<React.ButtonHTMLAttributes<HTMLButtonElement>> => ({
    className: "b--sb bg-sb svg-box20",
  })
)`
  cursor: pointer;
`;
const Row: StyledComponent<"div", Record<string, unknown>> = styled.div.attrs<{
  className: string;
}>({
  className: "flex",
})``;

const RemoveMessage: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "mb4",
})``;

export const editAndDeleteActionFormatter: (
  value: string,
  row: Readonly<Record<string, string>>,
  rowIndex: number,
  key: Readonly<IHeaderConfig>
) => JSX.Element = (
  _value: string,
  row: Readonly<Record<string, string>>,
  _rowIndex: number,
  key: Readonly<IHeaderConfig>
): JSX.Element => {
  function handleDelete(): void {
    if (key.deleteFunction !== undefined) {
      key.deleteFunction(row);
    }
  }

  function handleEdit(event: React.FormEvent<HTMLButtonElement>): void {
    if (key.editFunction !== undefined) {
      event.stopPropagation();
      key.editFunction(row);
    }
  }

  return (
    <Row>
      <ActionButton aria-label={"pen-button"} onClick={handleEdit}>
        <FontAwesomeIcon icon={faPen} />
      </ActionButton>
      <ConfirmDialog
        message={
          <RemoveMessage>
            {translate.t(
              "profile.credentialsModal.formatters.actions.removeCredentials.confirmModal.message"
            )}
          </RemoveMessage>
        }
        title={translate.t(
          "profile.credentialsModal.formatters.actions.removeCredentials.confirmModal.title"
        )}
      >
        {(confirm): React.ReactNode => {
          function handleClick(): void {
            confirm(handleDelete);
          }

          return (
            <ActionButton aria-label={"trash-button"} onClick={handleClick}>
              <FontAwesomeIcon icon={faTrashAlt} />
            </ActionButton>
          );
        }}
      </ConfirmDialog>
    </Row>
  );
};
