import React, { Component } from "react";
import Plot from "react-plotly.js";

const graphData = {
  masterGraph: {
    title: "Epithelial",
    model: "",
    xAxis: "X-Axis",
    yAxis: "Y-Axis",
    zAxis: "Z-Axis",
  },
};

class MySankeyEpithelialComponent extends Component {
  render() {
    return (
      <Plot
        data={[
          {
            type: "sankey",
            orientation: "h",
            node: {
              color: [
                "#6baed6",
                "#843c39",
                "#e7969c",
                "#3182bd",
                "#7b4173",
                "#9c9ede",
                "#969696",
                "#31a354",
                "#fd8d3c",
                "#feab49",
                "#feab49",
                "#feab49",
                "#feab49",
                "#feab49",
                "#feab49",
                "#feab49",
                "#feab49",
                "#feab49",
                "#feab49",
                "#feab49",
                "#feab49",
                "#feab49",
                "#feab49",
                "#feab49",
                "#feab49",
                "#feab49",
                "#feab49",
                "#feab49",
                "#feab49",
                "#feab49",
                "#feab49",
                "#feab49",
                "#feab49",
                "#feab49",
                "#feab49",
                "#feab49",
                "#feab49",
                "#feab49",
                "#feab49",
                "#feab49",
              ],
              label: [
                "Small_Intestine",
                "Vasculature",
                "Bladder",
                "Lung",
                "Kidney",
                "Thymus",
                "Trachea",
                "Large_Intestine",
                "Pancreas",
                "intestinal transient amplifying cell",
                "medullary thymic epithelial cell",
                "ciliated cell",
                "mesothelial cell",
                "kidney epithelial cell",
                "duodenum glandular cell",
                "pancreatic pp cell",
                "basal cell",
                "paneth cell of epithelium of small intestine",
                "goblet cell",
                "intestinal tuft cell",
                "respiratory goblet cell",
                "pancreatic alpha cell",
                "pancreatic delta cell",
                "club cell",
                "secretory cell",
                "serous cell of epithelium of bronchus",
                "bladder urothelial cell",
                "pancreatic beta cell",
                "mature enterocyte",
                "epithelial cell",
                "lung ciliated cell",
                "intestinal crypt stem cell",
                "paneth cell of epithelium of large intestine",
                "type i pneumocyte",
                "pancreatic ductal cell",
                "type ii pneumocyte",
                "immature enterocyte",
                "intestinal enteroendocrine cell",
                "pancreatic acinar cell",
                "ionocyte",
              ],
              line: { color: "black", width: 0.5 },
              pad: 15,
              thickness: 20,
            },
            link: {
              source: [
                2,
                4,
                7,
                7,
                7,
                7,
                7,
                7,
                7,
                7,
                3,
                3,
                3,
                3,
                3,
                3,
                3,
                3,
                3,
                8,
                8,
                8,
                8,
                8,
                8,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                5,
                5,
                6,
                6,
                6,
                6,
                1,
              ],
              target: [
                26,
                13,
                18,
                36,
                31,
                37,
                9,
                19,
                28,
                32,
                16,
                23,
                39,
                30,
                12,
                20,
                25,
                33,
                35,
                38,
                21,
                27,
                22,
                34,
                15,
                14,
                18,
                36,
                31,
                37,
                9,
                19,
                28,
                17,
                10,
                12,
                16,
                11,
                18,
                24,
                29,
              ],
              value: [
                2874,
                8354,
                166,
                920,
                143,
                36,
                156,
                21,
                545,
                57,
                2197,
                1051,
                22,
                605,
                17,
                760,
                15,
                213,
                5334,
                4816,
                71,
                87,
                9,
                1619,
                71,
                46,
                66,
                371,
                102,
                46,
                100,
                22,
                573,
                477,
                27,
                12,
                3913,
                39,
                85,
                78,
                26,
              ],
            },
          },
        ]}
        layout={{
          width: 800,
          height: 900,
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

export default MySankeyEpithelialComponent;
