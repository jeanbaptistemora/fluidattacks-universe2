import {
  faAngleLeft,
  faAngleRight,
  faAnglesLeft,
  faAnglesRight,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { Table } from "@tanstack/react-table";
import _ from "lodash";
import React, { useCallback } from "react";
import styled from "styled-components";

import { Button } from "components/Button";
import { Text } from "components/Text";

interface IPaginationProps<TData>
  extends Pick<
    Table<TData>,
    "getPageCount" | "getState" | "setPageIndex" | "setPageSize"
  > {
  onNextPage?: () => Promise<void>;
  size: number;
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

const Pagination = <TData extends object>({
  getPageCount,
  getState,
  onNextPage = undefined,
  setPageIndex,
  setPageSize,
  size,
}: Readonly<IPaginationProps<TData>>): JSX.Element => {
  const pageCount = getPageCount();
  const { pageIndex, pageSize } = getState().pagination;
  const isInFirst = pageIndex === 0;
  const isInLast = pageIndex === pageCount - 1;

  const goToFirst = useCallback((): void => {
    setPageIndex(0);
  }, [setPageIndex]);
  const goToLast = useCallback((): void => {
    setPageIndex(pageCount - 1);
  }, [pageCount, setPageIndex]);
  const goToNext = useCallback((): void => {
    if (isInLast && onNextPage) {
      void onNextPage().then((): void => {
        setPageIndex(pageIndex + 1);
      });
    } else {
      setPageIndex(pageIndex + 1);
    }
  }, [isInLast, onNextPage, pageIndex, setPageIndex]);
  const goToPrev = useCallback((): void => {
    setPageIndex(pageIndex - 1);
  }, [pageIndex, setPageIndex]);

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
                setPageSize(el);
              }}
              size={"sm"}
              variant={"secondary"}
            >
              {el}
            </Button>
          )
        )}
      <Text ml={3} size={1} tone={"light"}>
        {`${pageSize * pageIndex + 1} - ${Math.min(
          pageSize * (pageIndex + 1),
          size
        )} of ${size} items`}
      </Text>
      <Button
        disabled={isInFirst}
        onClick={goToFirst}
        size={"sm"}
        variant={"secondary"}
      >
        <FontAwesomeIcon icon={faAnglesLeft} />
      </Button>
      <Button
        disabled={isInFirst}
        onClick={goToPrev}
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
              setPageIndex(el);
            }}
            size={"sm"}
            variant={"secondary"}
          >
            {el + 1}
          </Button>
        )
      )}
      <Button
        disabled={isInLast && onNextPage === undefined}
        onClick={goToNext}
        size={"sm"}
        variant={"secondary"}
      >
        <FontAwesomeIcon icon={faAngleRight} />
      </Button>
      <Button
        disabled={isInLast}
        onClick={goToLast}
        size={"sm"}
        variant={"secondary"}
      >
        <FontAwesomeIcon icon={faAnglesRight} />
      </Button>
    </PaginationBox>
  );
};

export { Pagination };
