import React from 'react';
import * as d3 from 'd3';
import {useD3} from "../hooks/useD3";
import './Chart.scss';

function LineChart({ data, height, width }) {
    const ref = useD3(
        (svg) => {
            const margin = { top: 2, right: 2, bottom: 2, left: 2 };

            const yAvg = getAvg(data.map(v => v.y));
            const yStd = getStd(data.map(v => v.y));
            data = data.map(v => ({
                x: v.x,
                y: (v.y - yAvg) / yStd,
            }));

            const x = d3
                .scaleLinear()
                .domain(d3.extent(data, d => d.x))
                .range([margin.left, width - margin.right]);

            const y = d3
                .scaleLinear()
                .domain([d3.min(data, d => d.y), d3.max(data, d => d.y)]).nice()
                .range([height - margin.bottom, margin.top]);

            const line = d3.line()
                .defined(d => !isNaN((d.y)))
                .x(d => x(d.x))
                .y(d => y(d.y));

            svg.append("path")
                .datum(data)
                .attr("fill", "none")
                .attr("stroke", "steelblue")
                .attr("stroke-width", 1.5)
                .attr("stroke-linejoin", "round")
                .attr("stroke-linecap", "round")
                .attr("d", line);
        },
        data
    );

    return (
        <svg
            ref={ref}
            height="100%"
            width="100%"
            // height={42}
            // width={70}
            className={"chart"}
        >
        </svg>
    );
}

let getAvg = (data) => {
    return data.reduce((sum, v) => sum + v / data.length, 0);
};

let getStd = (data) => {
    let avg = getAvg(data);
    let avgSqDiff = getAvg(data.map((v) => (v - avg)**2));
    return Math.sqrt(avgSqDiff);
};

export default LineChart;