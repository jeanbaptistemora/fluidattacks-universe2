import styled from "styled-components";

const ImageBlockContainer = styled.div`
  img {
    display: block;
    margin: auto;
  }

  p {
    font-size: 0.75rem;
    text-align: center;
  }
`;

const TableBlockContainer = styled.div`
  overflow-x: auto;

  p {
    font-size: 0.75rem;
    text-align: center;
  }

  table {
    border-collapse: collapse;
    overflow-x: auto;
    border-spacing: 0;
    text-align: left;
    width: 100%;

    thead {
      border-bottom: solid 2px #535365;
    }

    thead th {
      color: #2e2e38;
      font-size: 20px;
      font-weight: 700;
      padding: 1rem;
    }

    tbody tr {
      background-color: #fff;
      position: relative;
    }

    tbody tr:nth-child(even) {
      background-color: #f4f4f6;
    }

    tbody td {
      border-bottom: solid 1px #b0b0bf;
      color: #535365;
      padding: 1rem;
    }
  }
`;

const VideoBlockContainer = styled.div`
  position: relative;
  overflow: hidden;
  width: 100%;
  padding-top: 56.25%;

  iframe {
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
    width: 100%;
    height: 100%;
  }
`;

export { ImageBlockContainer, TableBlockContainer, VideoBlockContainer };
