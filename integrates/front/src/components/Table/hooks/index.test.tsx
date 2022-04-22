import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";

import { useRowExpand } from "./useRowExpand";

import { Table } from "..";

describe("Table hooks", (): void => {
  describe("useRowExpand", (): void => {
    const TestComponent: React.FC = (): JSX.Element => {
      const rows = [{ id: 1 }, { id: 2 }, { id: 3 }];
      const { expandedRows, handleRowExpand, handleRowExpandAll } =
        useRowExpand({
          rowId: "id",
          rows,
          storageKey: "expandedRows",
        });

      const renderer = (): JSX.Element => <div id={"expanded"} />;

      return (
        <Table
          dataset={rows}
          expandRow={{
            expanded: expandedRows,
            onExpand: handleRowExpand,
            onExpandAll: handleRowExpandAll,
            renderer,
            showExpandColumn: true,
          }}
          exportCsv={false}
          headers={[{ dataField: "id", header: "id" }]}
          id={"testTable"}
          pageSize={10}
          search={false}
        />
      );
    };

    it("should return a function", (): void => {
      expect.hasAssertions();
      expect(typeof useRowExpand).toBe("function");
    });

    it("should expand", async (): Promise<void> => {
      expect.hasAssertions();

      const { container } = render(<TestComponent />);

      expect(container.querySelectorAll("#expanded")).toHaveLength(0);

      userEvent.click(
        within(screen.getByRole("row", { name: "1" })).getAllByRole("cell")[0]
      );
      userEvent.click(
        within(screen.getByRole("row", { name: "2" })).getAllByRole("cell")[0]
      );
      await waitFor((): void => {
        expect(container.querySelectorAll("#expanded")).toHaveLength(2);
      });

      sessionStorage.clear();
      jest.clearAllMocks();
    });

    it("should expand all", async (): Promise<void> => {
      expect.hasAssertions();

      const { container } = render(<TestComponent />);

      expect(container.querySelectorAll("#expanded")).toHaveLength(0);

      userEvent.click(
        within(screen.getAllByRole("row")[0]).getAllByRole("columnheader")[0]
      );
      const totalRows = 3;
      await waitFor((): void => {
        expect(container.querySelectorAll("#expanded")).toHaveLength(totalRows);
      });

      sessionStorage.clear();
      jest.clearAllMocks();
    });
  });
});
