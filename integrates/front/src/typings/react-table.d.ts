import { ColumnMeta } from "@tanstack/react-table";

declare module "@tanstack/react-table" {
  interface ColumnMeta {
    filterType: "date" | "number" | "select" | "text";
  }
}
