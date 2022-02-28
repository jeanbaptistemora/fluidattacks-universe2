import styled from "styled-components";

import { FormikText } from "utils/forms/fields";

const SearchContainer = styled.div`
  background-color: #e9e9ed;
  border-radius: 4px;
  color: #b0b0bf;
  font-size: 16px;
  margin-right: 5px;
  padding-left: 12px;
`;

const SearchInput = styled(FormikText)`
  background-color: #e9e9ed;
  border-color: transparent !important;
  border: none;
  color: #2e2e38 !important;
  transition: ease-in-out, width 0.35s ease-in-out !important;
  width: 120px !important;

  :focus {
    border-color: transparent !important;
    width: 180px !important;
  }

  ::placeholder {
    color: #b0b0bf;
  }
`;

export { SearchContainer, SearchInput };
