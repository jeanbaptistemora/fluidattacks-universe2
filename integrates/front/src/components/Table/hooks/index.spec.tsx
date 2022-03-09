import { mount } from "enzyme";
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
          bordered={false}
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
      expect(typeof useRowExpand).toStrictEqual("function");
    });

    it("should expand", (): void => {
      expect.hasAssertions();

      const wrapper = mount(<TestComponent />);

      expect(wrapper.find({ id: "expanded" })).toHaveLength(0);

      const rows = wrapper.find("tbody").find("tr");
      rows.slice(0, 2).forEach((row): void => {
        const expandBtn = row.find("td").at(0);
        expandBtn.simulate("click");
      });

      expect(wrapper.find({ id: "expanded" })).toHaveLength(2);

      sessionStorage.clear();
    });

    it("should expand all", (): void => {
      expect.hasAssertions();

      const wrapper = mount(<TestComponent />);

      expect(wrapper.find({ id: "expanded" })).toHaveLength(0);

      const expandBtn = wrapper.find("thead").find("tr").find("th").at(0);
      expandBtn.simulate("click");

      const totalRows = 3;

      expect(wrapper.find({ id: "expanded" })).toHaveLength(totalRows);

      sessionStorage.clear();
    });
  });
});
