import type {
  FlattenInterpolation,
  StyledComponent,
  ThemeProps,
} from "styled-components";
import styled, { css } from "styled-components";

import SearchBoxMain from "../SearchBox";
import { SearchResult } from "../SearchResults";

interface IThemeProps {
  theme: {
    background?: string;
    faded?: string;
    foreground?: string;
  };
}

const StyledSearchRoot: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    fr
    mr3
    pr2
    pv4
    mv1
  `,
})``;

const open = css`
  background: ${({ theme }: IThemeProps): string => theme.background as string};
  cursor: text;
  margin-left: -1.6em;
  padding-left: 1.6em;
  width: 10em;
`;

const closed = css`
  background: transparent;
  cursor: pointer;
  margin-left: -1em;
  padding-left: 1em;
  width: 0;
`;

const StyledSearchBox = styled(SearchBoxMain)`
  align-items: center;
  display: flex;
  flex-direction: row-reverse;
  margin-bottom: 0;

  .SearchInput {
    border: ${({ hasFocus }: { hasFocus: boolean }): string =>
      hasFocus ? "auto" : "none"};
    border-radius: 2px;
    color: ${({ theme }: IThemeProps): string => theme.foreground as string};
    font-size: 1em;
    outline: none;
    transition: 100ms;

    ::placeholder {
      color: ${({ theme }: IThemeProps): string => theme.faded as string};
    }
    ${({ hasFocus }): FlattenInterpolation<ThemeProps<string>> =>
      hasFocus ? open : closed}
  }

  .SearchIcon {
    color: ${({ theme }: IThemeProps): string => theme.foreground as string};
    margin: 0.3em;
    pointer-events: none;
    width: 1em;
  }
`;

const Popover = css`
  background: ${({ theme }: IThemeProps): string => theme.background as string};
  border-radius: 2px;
  box-shadow: 0 0 5px 0;
  margin-top: 0.5em;
  max-height: 80vh;
  max-width: 30em;
  overflow-y: auto;
  padding: 1em;
  position: absolute;
  right: 0;
  top: 100%;
  width: 80vw;
  z-index: 2;
`;

const StyledSearchResult = styled(SearchResult).attrs({})<{ show: boolean }>`
  display: ${(props): string => (props.show ? `block` : `none`)};
  ${Popover}
  .HitCount {
    display: flex;
    justify-content: flex-end;
  }

  .Hits {
    ul {
      list-style: none;
      margin-left: 0;
    }

    li.ais-Hits-item {
      margin-bottom: 1em;

      a {
        color: ${({ theme }: IThemeProps): string =>
          theme.foreground as string};

        h4 {
          margin-bottom: 0.2em;
        }
      }
    }
  }

  .ais-PoweredBy {
    display: flex;
    font-size: 80%;
    justify-content: flex-end;

    svg {
      width: 70px;
    }
  }
`;
export { StyledSearchBox, StyledSearchResult, StyledSearchRoot };
