// Array Visualizer - BOX STYLE (matching user's image)
// Clean, simple boxes with comparison arrows

import React from 'react';
import './ArrayVisualizer.css';

const ArrayVisualizer = ({ data }) => {
    if (!data || !data.values || data.values.length === 0) return null;

    return (
        <div className="array-visualizer">
            <div className="structure-label">{data.name}</div>

            <div className="array-boxes-container">
                {data.values.map((value, index) => {
                    const isHighlighted = data.highlights?.indices?.includes(index);
                    const highlightIndex = data.highlights?.indices?.indexOf(index);

                    // Simple color logic: highlighted = blue, normal = green
                    const color = isHighlighted && highlightIndex !== -1
                        ? (data.highlights.colors[highlightIndex] || '#3498db')
                        : '#2ecc71';  // Default green

                    const label = isHighlighted && highlightIndex !== -1
                        ? data.highlights.labels[highlightIndex]
                        : null;

                    return (
                        <div key={index} className="array-box-wrapper">
                            {label && <div className="box-label">{label}</div>}

                            <div
                                className={`array-box ${isHighlighted ? 'active' : ''}`}
                                style={{ backgroundColor: color }}
                            >
                                <span className="box-value">{value}</span>
                            </div>

                            <div className="box-index">{index}</div>
                        </div>
                    );
                })}
            </div>

            {/* Show comparison arrow between highlighted elements */}
            {data.highlights?.indices?.length === 2 && (
                <div className="comparison-info">
                    Comparing: {data.values[data.highlights.indices[0]]} ↔ {data.values[data.highlights.indices[1]]}
                </div>
            )}
        </div>
    );
};

export default ArrayVisualizer;
