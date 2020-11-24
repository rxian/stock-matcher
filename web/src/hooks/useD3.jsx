import React from 'react';
import * as d3 from 'd3';

export const useD3 = (render, dependencies) => {
    const ref = React.useRef();

    React.useEffect(() => {
        render(d3.select(ref.current));
    }, [dependencies, render]);
    return ref;
};