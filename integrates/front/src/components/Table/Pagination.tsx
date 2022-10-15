/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { faAngleLeft, faAngleRight } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { RowData, Table } from "@tanstack/react-table";
import _ from "lodash";
import React, { useCallback } from "react";
import styled from "styled-components";

import type { ITableProps } from "./types";

import { Button } from "components/Button";
import { Text } from "components/Text";

interface IPaginationProps<TData extends RowData>
  extends Pick<ITableProps<TData>, "onNextPage"> {
  size: number;
  table: Table<TData>;
}

const PaginationBox = styled.div.attrs({
  className: "comp-table-pagination",
})`
  align-items: center;
  background-color: #2e2e38;
  border-radius: 4px;
  display: flex;
  margin-top: 4px;
  padding: 4px;
`;

const Pagination = <TData extends RowData>({
  onNextPage = undefined,
  size,
  table,
}: Readonly<IPaginationProps<TData>>): JSX.Element => {
  const pageCount = table.getPageCount();
  const { pageIndex, pageSize } = table.getState().pagination;
  const isInLast = pageIndex === pageCount - 2;

  const goToNext = useCallback((): void => {
    if (isInLast && onNextPage) {
      void onNextPage().finally((): void => {
        table.setPageIndex(pageIndex + 1);
      });
    } else {
      table.setPageIndex(pageIndex + 1);
    }
  }, [isInLast, onNextPage, pageIndex, table]);

  const indexes = _.range(
    Math.max(pageIndex - 2, 0),
    Math.min(pageIndex + 2, pageCount - 1) + 1
  );

  return (
    <PaginationBox>
      {[10, 20, 50, Math.min(100, size)]
        .filter((el): boolean => el <= size)
        .map(
          (el: number): JSX.Element => (
            <Button
              key={el}
              onClick={function fn(): void {
                if (el === size && onNextPage) {
                  void onNextPage().finally((): void => {
                    table.setPageSize(el);
                  });
                } else {
                  table.setPageSize(el);
                }
              }}
              size={"sm"}
              variant={"secondary"}
            >
              {el}
            </Button>
          )
        )}
      <Text ml={3} size={"xs"} tone={"light"}>
        {`${pageSize * pageIndex + 1} - ${Math.min(
          pageSize * (pageIndex + 1),
          size
        )} of ${size} items`}
      </Text>
      <Button
        disabled={!table.getCanPreviousPage()}
        onClick={function fn(): void {
          table.previousPage();
        }}
        size={"sm"}
        variant={"secondary"}
      >
        <FontAwesomeIcon icon={faAngleLeft} />
      </Button>
      {indexes.map(
        (el: number): JSX.Element => (
          <Button
            key={el}
            onClick={function fn(): void {
              if (el === pageCount - 1 && onNextPage) {
                void onNextPage().finally((): void => {
                  table.setPageIndex(el);
                });
              } else {
                table.setPageIndex(el);
              }
            }}
            size={"sm"}
            variant={"secondary"}
          >
            {el + 1}
          </Button>
        )
      )}
      <Button
        disabled={!table.getCanNextPage()}
        onClick={goToNext}
        size={"sm"}
        variant={"secondary"}
      >
        <FontAwesomeIcon icon={faAngleRight} />
      </Button>
    </PaginationBox>
  );
};

export { Pagination };