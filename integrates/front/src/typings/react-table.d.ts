import { ColumnMeta } from "@tanstack/react-table";

declare module "@tanstack/react-table" {
  interface ColumnMeta {
    filterType: "dateRange" | "number" | "numberRange" | "select" | "text";
  }
}
