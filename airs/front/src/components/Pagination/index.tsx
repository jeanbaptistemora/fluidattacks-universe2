import React from "react";
import { FiChevronLeft, FiChevronRight } from "react-icons/fi";
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
    nextLabel={<FiChevronRight />}
    nextLinkClassName={"page-link"}
    onPageChange={onChange}
    pageClassName={"page-item"}
    pageCount={pageCount}
    pageLinkClassName={"page-link"}
    pageRangeDisplayed={5}
    previousClassName={"page-item"}
    previousLabel={<FiChevronLeft />}
    previousLinkClassName={"page-link"}
  />
);
