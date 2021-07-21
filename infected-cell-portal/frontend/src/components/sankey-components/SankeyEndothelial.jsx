import React, { Component } from "react";
import Plot from "react-plotly.js";

const graphData = {
  masterGraph: {
    title: "Endothelial",
    model: "",
    xAxis: "X-Axis",
    yAxis: "Y-Axis",
    zAxis: "Z-Axis",
  },
};

class MySankeyEndothelialComponent extends Component {
  render() {
    return (
      <Plot
        data={[
          {
            type: "sankey",
            orientation: "h",
            node: {
              color: [
                "#e7ba52",
                "#6baed6",
                "#843c39",
                "#e7969c",
                "#3182bd",
                "#7b4173",
                "#9c9ede",
                "#969696",
                "#31a354",
                "#393b79",
                "#8c6d31",
                "#fd8d3c",
                "#fee187",
                "#fee187",
                "#fee187",
                "#fee187",
                "#fee187",
                "#fee187",
                "#fee187",
                "#fee187",
                "#fee187",
              ],
              label: [
                "Muscle",
                "Small_Intestine",
                "Vasculature",
                "Bladder",
                "Lung",
                "Kidney",
                "Thymus",
                "Trachea",
                "Large_Intestine",
                "Spleen",
                "Lymph_Node",
                "Pancreas",
                "lung microvascular endothelial cell",
                "vein endothelial cell",
                "endothelial cell",
                "endothelial cell of artery",
                "capillary endothelial cell",
                "endothelial cell of vascular tree",
                "endothelial cell of lymphatic vessel",
                "capillary aerocyte",
                "gut endothelial cell",
              ],
              line: {
                color: "black",
                width: 0.5,
              },
              pad: 15,
              thickness: 20,
            },
            link: {
              source: [
                3,
                3,
                3,
                5,
                8,
                4,
                4,
                4,
                4,
                4,
                4,
                10,
                0,
                0,
                0,
                0,
                11,
                1,
                9,
                6,
                6,
                6,
                6,
                7,
                2,
              ],
              target: [
                16,
                18,
                13,
                14,
                20,
                19,
                16,
                15,
                18,
                12,
                13,
                14,
                16,
                15,
                18,
                17,
                14,
                20,
                14,
                16,
                15,
                18,
                13,
                14,
                14,
              ],
              value: [
                66,
                73,
                266,
                95,
                23,
                571,
                968,
                189,
                50,
                490,
                513,
                16,
                1502,
                98,
                56,
                3111,
                268,
                31,
                158,
                988,
                181,
                15,
                663,
                33,
                1549,
              ],
            },
          },
        ]}
        layout={{
          width: 800,
          height: 800,
          margin: {
            l: 50,
            r: 50,
            b: 80,
            t: 90,
            pad: 4,
          },
          title: graphData.masterGraph.title,
          annotations: [
            {
              text: graphData.masterGraph.model,
              font: {
                size: 14,
                color: "#444444",
              },
              showarrow: false,
              align: "center",
              x: 0.5,
              y: 1.1,
              xref: "paper",
              yref: "paper",
            },
          ],
          scene: {
            xaxis: {
              title: graphData.masterGraph.xAxis,
              titlefont: {
                family: "Courier New, monospace",
                size: 12,
                color: "#444444",
              },
            },
            yaxis: {
              title: graphData.masterGraph.yAxis,
              titlefont: {
                family: "Courier New, monospace",
                size: 12,
                color: "#444444",
              },
            },
            zaxis: {
              title: graphData.masterGraph.zAxis,
              titlefont: {
                family: "Courier New, monospace",
                size: 12,
                color: "#444444",
              },
            },
          },
        }}
      />
    );
  }
}

export default MySankeyEndothelialComponent;
