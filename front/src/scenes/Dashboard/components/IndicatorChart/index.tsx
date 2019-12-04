import { AxisProps } from "@nivo/axes";
import { LegendProps } from "@nivo/legends";
import { LineDatum, LineSerieData, ResponsiveLine } from "@nivo/line";
import React from "react";
import translate from "../../../../utils/translations/translate";
import { default as style } from "./index.css";

/**
 * Indicator's Chart properties
 */
interface IChartProps {
    dataChart: LineDatum[][];
}
/**
 * Project Indicator Chart
 */
const indicatorChart: React.FunctionComponent<IChartProps> =
    (props: IChartProps): JSX.Element => {
        const dataPoints: LineSerieData[] = [
            {
                color: style.styleColorFound,
                data: props.dataChart[0],
                id: translate.t("search_findings.tab_indicators.data_chart_found"),
            },
            {
                color: style.styleColorClosed,
                data: props.dataChart[3],
                id: translate.t("search_findings.tab_indicators.data_chart_assumed_closed"),
            },
            {
                color: style.styleColorClosed,
                data: props.dataChart[2],
                id: translate.t("search_findings.tab_indicators.data_chart_closed"),
            },
        ];

        const dataAxisLeft: AxisProps = {
            legend: translate.t("search_findings.tab_indicators.data_chart_legend_vulnerabilities"),
            legendOffset: -48,
            legendPosition: "middle",
            tickPadding: 5,
            tickRotation: 0,
            tickSize: 5,
        };

        const dataAxisBotton: AxisProps = {
            legend: translate.t("search_findings.tab_indicators.data_chart_legend_week"),
            legendOffset: 60,
            legendPosition: "end",
            tickPadding: 6,
            tickRotation: -39,
            tickSize: 0,
        };

        const dataLegend: LegendProps[] = [{
            anchor: "right",
            direction: "column",
            effects: [
                {
                    on: "hover",
                    style: {
                        itemBackground: "rgba(0, 0, 0, .03)",
                        itemOpacity: 1,
                    },
                },
            ],
            itemDirection: "left-to-right",
            itemHeight: 28,
            itemOpacity: 0.75,
            itemWidth: 72,
            itemsSpacing: 10,
            justify: false,
            symbolShape: "circle",
            symbolSize: 15,
            translateX: 80,
            translateY: 0,
        }];

        return (
            <React.StrictMode>
                <div className={style.styleChart} >
                    <ResponsiveLine
                        data={dataPoints}
                        xScale={{ type: "point" }}
                        yScale={{ type: "linear", stacked: false, min: 0, max: "auto" }}
                        margin={{ top: 10, right: 130, bottom: 87, left: 60 }}
                        lineWidth={3}
                        axisRight={undefined}
                        axisTop={undefined}
                        axisLeft={dataAxisLeft}
                        axisBottom={dataAxisBotton}
                        colors={{ scheme: "category10" }}
                        pointSize={10}
                        pointColor={{ theme: "background" }}
                        pointBorderWidth={2}
                        enableSlices="x"
                        pointBorderColor={{ from: "serieColor" }}
                        useMesh={true}
                        legends={dataLegend}
                        animate={true}
                        motionStiffness={100}
                        motionDamping={15}
                    />
                </div>
            </React.StrictMode>
        );
    };
export { indicatorChart as IndicatorChart };
