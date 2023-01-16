import { faFilter } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { RowData, Table } from "@tanstack/react-table";
import React, { useCallback, useState } from "react";

import { DateRangeFilter } from "./DateRangeFilter";
import { NumberFilter } from "./NumberFilter";
import { NumberRangeFilter } from "./NumberRangeFilter";
import { SelectFilter } from "./SelectFilter";
import { TextFilter } from "./TextFilter";

import { Button } from "components/Button";
import { Col, Row } from "components/Layout";
import { SidePanel } from "components/SidePanel";

interface IFiltersProps<TData extends RowData> {
  table: Table<TData>;
}

const Filters = <TData extends RowData>({
  table,
}: IFiltersProps<TData>): JSX.Element => {
  const [open, setOpen] = useState(false);

  const openPanel = useCallback((): void => {
    setOpen(true);
  }, []);
  const closePanel = useCallback((): void => {
    setOpen(false);
  }, []);

  const columnsToFilter = table
    .getAllLeafColumns()
    .filter(
      (column): boolean => column.getCanFilter() && column.getIsVisible()
    );

  const resetFiltersHandler = useCallback((): ((
    event: React.FormEvent
  ) => void) => {
    table.resetColumnFilters();

    return (event: React.FormEvent): void => {
      event.stopPropagation();
    };
  }, [table]);

  return (
    <React.Fragment>
      <Button id={"filter-config"} onClick={openPanel} variant={"ghost"}>
        <div style={{ width: "55px" }} />
        <FontAwesomeIcon icon={faFilter} />
        &nbsp;
        {"Filter"}
      </Button>
      <SidePanel onClose={closePanel} open={open}>
        <React.Fragment>
          {columnsToFilter.map((column): JSX.Element => {
            const { meta } = column.columnDef;
            const filterType = meta?.filterType;

            if (filterType === "number") {
              return (
                <Row key={column.id}>
                  <Col>
                    <NumberFilter column={column} />
                  </Col>
                </Row>
              );
            }

            if (filterType === "numberRange") {
              return (
                <Row key={column.id}>
                  <Col>
                    <NumberRangeFilter column={column} />
                  </Col>
                </Row>
              );
            }

            if (filterType === "select") {
              return (
                <Row key={column.id}>
                  <Col>
                    <SelectFilter column={column} />
                  </Col>
                </Row>
              );
            }

            if (filterType === "dateRange") {
              return (
                <Row key={column.id}>
                  <Col>
                    <DateRangeFilter column={column} />
                  </Col>
                </Row>
              );
            }

            return (
              <Row key={column.id}>
                <Col>
                  <TextFilter column={column} />
                </Col>
              </Row>
            );
          })}
          <Row>
            <Col>
              <Button onClick={resetFiltersHandler} variant={"secondary"}>
                {"Clear filters"}
              </Button>
            </Col>
          </Row>
        </React.Fragment>
      </SidePanel>
    </React.Fragment>
  );
};

export { Filters };
