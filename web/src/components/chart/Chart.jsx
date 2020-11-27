import React from 'react';
import * as d3 from 'd3';
import './Chart.scss';
import {useD3} from "../../hooks/useD3";

function LineChart({ data, height, width, normal, axis, strokeColor, strokeWidth }) {
    const ref = useD3(
        (svg) => {
            svg.selectAll("svg > *").remove();

            let margin = { top: 2, right: 2, bottom: 2, left: 2 };
            if (axis) {
                margin = { top: 30, right: 2, bottom: 50, left: 40 };
            }

            // normalization
            if (normal) data = normalize(data);

            const x = d3
                .scaleTime()
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
                .attr("class", "line-graph")
                .attr("fill", "none")
                .attr("stroke", strokeColor? strokeColor: "#c6b74c")
                .attr("stroke-width", strokeWidth? strokeWidth: 2.5)
                .attr("stroke-linejoin", "round")
                .attr("stroke-linecap", "round")
                .attr("d", line);

            // axes
            if (axis) {
                const xAxis = g => g
                    .attr("class", "xaxis axis")
                    .attr("transform", `translate(0, ${height - margin.bottom})`)
                    .call(d3.axisBottom(x)
                        .ticks(width / 40)
                        // .tickValues(data.map(d => d.x))
                        .tickSizeOuter(0)
                        .tickSizeInner(5)
                        .tickFormat(d3.timeFormat("%Y-%m-%d"))
                    );

                const yAxis = g => g
                    .attr("class", "yaxis axis")
                    .attr("transform", `translate(${margin.left}, 0)`)
                    .call(d3.axisLeft(y))
                    .call(g => g.select(".domain").remove())
                    .call(g => g.select(".tick:last-of-type text").clone()
                        .attr("x", 3)
                        .attr("text-anchor", "start")
                        .attr("font-weight", "bold")
                        .text(data.y));

                svg.append("g")
                    .call(xAxis);

                svg.append("g")
                    .call(yAxis);

                svg.selectAll(".xaxis text")
                    .attr("transform", function(d) {
                        return `translate(${ this.getBBox().height*-2 }, ${ this.getBBox().height+5})rotate(-45)`;
                    })
                    .attr("font-size", "8px");
            }
        },
        data
    );

    return (
        <svg
            ref={ref}
            viewBox={`0 0 ${width} ${height}`}
            preserveAspectRatio="xMidYMid meet"
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

let normalize = (data) => {
    const yAvg = getAvg(data.map(v => v.y));
    const yStd = getStd(data.map(v => v.y));
    return data.map(v => ({
        x: v.x,
        y: (v.y - yAvg) / yStd,
    }));
};

export default LineChart;