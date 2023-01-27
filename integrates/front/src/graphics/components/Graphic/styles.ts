import styled from "styled-components";

const GraphicButton = styled.button.attrs({
  className: "dim dib pointer pr3 pl3 pt2 pb2 outline-0",
  type: "button",
})`
  border: 1px solid #ccc;
  color: #333;
  min-width: 100%;
`;

const GraphicIframe = styled.iframe.attrs({
  className: "frame bn h-100 overflow-hidden w-100",
})``;

const GraphicLoading = styled.div.attrs({
  className: "absolute lh-solid tc",
})`
  color: #eee;
  left: 50%;
  transform: translate(-50%);
`;

const GraphicPanelCollapse = styled.div.attrs({
  className: "mb4 items-center" as string,
})``;

const GraphicPanelCollapseBody = styled.div.attrs({
  className: "pa2 items-center panel-cb",
})``;

const GraphicPanelCollapseHeader = styled.div.attrs({
  className: "ph3 flex items-center panel-ch",
})`
  height: 67px;
`;

export {
  GraphicButton,
  GraphicIframe,
  GraphicLoading,
  GraphicPanelCollapse,
  GraphicPanelCollapseBody,
  GraphicPanelCollapseHeader,
};
