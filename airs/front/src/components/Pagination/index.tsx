import React from "react";
import ReactPaginate from "react-paginate";

interface IPaginator {
  onChange: (prop: { selected: number }) => void;
  pageCount: number;
}

export const Pagination: React.FC<IPaginator> = ({
  onChange,
  pageCount,
}: IPaginator): JSX.Element => (
  <ReactPaginate
    activeClassName={"active"}
    breakClassName={"page-item"}
    breakLabel={"..."}
    breakLinkClassName={"page-link"}
    containerClassName={"pagination-container"}
    nextClassName={"page-item"}
    nextLabel={">"}
    nextLinkClassName={"page-link"}
    onPageChange={onChange}
    pageClassName={"page-item"}
    pageCount={pageCount}
    pageLinkClassName={"page-link"}
    pageRangeDisplayed={2}
    previousClassName={"page-item"}
    previousLabel={"<"}
    previousLinkClassName={"page-link"}
  />
);
