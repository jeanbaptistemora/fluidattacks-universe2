import type { ChangeEvent, ReactElement } from "react";
import React from "react";

import type { IPagMenuProps } from "./types";

export const PagMenu = <TData extends object>(
  props: IPagMenuProps<TData>
): JSX.Element => {
  const { table } = props;

  function firstPage(): void {
    table.setPageIndex(0);
  }
  function prevPage(): void {
    table.previousPage();
  }
  function nextPage(): void {
    table.nextPage();
  }
  function lastPage(): void {
    table.setPageIndex(table.getPageCount() - 1);
  }
  function pageIndex(event: ChangeEvent<HTMLInputElement>): void {
    const page = event.target.value ? Number(event.target.value) - 1 : 0;
    table.setPageIndex(page);
  }
  function pageRecords(event: ChangeEvent<HTMLSelectElement>): void {
    table.setPageSize(Number(event.target.value));
  }

  return (
    <div>
      <button disabled={!table.getCanPreviousPage()} onClick={firstPage}>
        {"<<"}
      </button>
      <button disabled={!table.getCanPreviousPage()} onClick={prevPage}>
        {"<"}
      </button>
      <button disabled={!table.getCanNextPage()} onClick={nextPage}>
        {">"}
      </button>
      <button disabled={!table.getCanPreviousPage()} onClick={lastPage}>
        {">>"}
      </button>
      <span>
        <strong>
          {`${
            table.getState().pagination.pageIndex + 1
          } of ${table.getPageCount()}`}
        </strong>
      </span>
      <span>
        {"Page: "}
        <input
          defaultValue={table.getState().pagination.pageIndex + 1}
          onChange={pageIndex}
          type={"number"}
        />
      </span>
      <select
        onChange={pageRecords}
        value={table.getState().pagination.pageSize}
      >
        {[10, 20].map(
          (pageSize): ReactElement => (
            <option key={pageSize} value={pageSize}>
              {`Show ${pageSize}`}
            </option>
          )
        )}
      </select>
      {`${table.getRowModel().rows.length} Rows`}
    </div>
  );
};
