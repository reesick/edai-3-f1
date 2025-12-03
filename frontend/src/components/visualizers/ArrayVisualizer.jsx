// Array Visualizer - Horizontal bar visualization
// Used for searching and sorting algorithms

import React from 'react';
import './ArrayVisualizer.css';

const ArrayVisualizer = ({ data }) => {
    if (!data || !data.values || data.values.length === 0) return null;

    const maxValue = Math.max(...data.values.map(v => Math.abs(v))) || 1;

    return (
        <div className="array-visualizer">
            <div className="structure-label">{data.name}</div>
            <div className="array-container">
                {data.values.map((value, index) => {
                    const isHighlighted = data.highlights?.indices?.includes(index);
                    const highlightIndex = data.highlights?.indices?.indexOf(index);
                    const color = isHighlighted && highlightIndex !== -1
                        ? data.highlights.colors[highlightIndex]
                        : '#3498db';
                    const label = isHighlighted && highlightIndex !== -1
                        ? data.highlights.labels[highlightIndex]
                        : null;

                    const barHeight = (Math.abs(value) / maxValue) * 120;

                    return (
                        <div key={index} className="array-element">
                            {label && <div className="element-label">{label}</div>}
                            <div
                                className={`array-bar ${isHighlighted ? 'highlighted' : ''}`}
                                style={{
                                    backgroundColor: color,
                                    height: `${barHeight}px`
                                }}
                            >
                                <span className="array-value">{value}</span>
                            </div>
                            <div className="array-index">{index}</div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

export default ArrayVisualizer;
