// Array Visualizer - BOX STYLE (matching user's image)
// Clean, simple boxes with comparison arrows

import React from 'react';
import './ArrayVisualizer.css';

const ArrayVisualizer = ({ data, highlights }) => {
    // Handle different data formats:
    // 1. Direct array: [64, 25, 12, 22, 11]
    // 2. Object with values: {values: [64, 25, 12, 22, 11], highlights: {...}}
    let arrayData;

    // Normalize highlights to handle both formats:
    // Format 1: Simple array [1, 2] (from Linear/Sentinel Search)
    // Format 2: Object {indices: [1, 2], colors: [...], labels: [...]} (from Binary Search)
    const normalizeHighlights = (h) => {
        if (!h) return { indices: [], colors: [], labels: [] };
        if (Array.isArray(h)) {
            // Simple array format - convert to object
            return {
                indices: h,
                colors: h.map(() => '#3498db'),  // Default blue
                labels: h.map(() => null)
            };
        }
        // Already in object format
        return h;
    };

    if (Array.isArray(data)) {
        // Direct array from sorting/searching
        // Use highlights from props (passed separately by ModulePage)
        arrayData = {
            values: data,
            highlights: normalizeHighlights(highlights),
            name: ''
        };
    } else if (data && data.values) {
        // Object with values property
        // Merge highlights from props with data.highlights
        const mergedHighlights = {
            ...normalizeHighlights(data.highlights),
            ...normalizeHighlights(highlights)
        };
        arrayData = {
            ...data,
            highlights: mergedHighlights
        };
    } else {
        // No data
        return (
            <div className="array-visualizer">
                <div className="empty-message">No data to visualize</div>
            </div>
        );
    }

    if (!arrayData.values || arrayData.values.length === 0) {
        return (
            <div className="array-visualizer">
                <div className="empty-message">No data to visualize</div>
            </div>
        );
    }

    return (
        <div className="array-visualizer">
            <div className="structure-label">{arrayData.name}</div>

            <div className="array-boxes-container">
                {arrayData.values.map((value, index) => {
                    const isHighlighted = arrayData.highlights?.indices?.includes(index);
                    const highlightIndex = arrayData.highlights?.indices?.indexOf(index);

                    // Simple color logic: highlighted = blue, normal = green
                    const color = isHighlighted && highlightIndex !== -1
                        ? (arrayData.highlights.colors?.[highlightIndex] || '#3498db')
                        : '#2ecc71';  // Default green

                    const label = isHighlighted && highlightIndex !== -1
                        ? arrayData.highlights.labels?.[highlightIndex]
                        : null;

                    return (
                        <div key={index} className="array-box-wrapper">
                            {label && <div className="box-label">{label}</div>}

                            <div
                                className={`array-box ${isHighlighted ? 'active' : ''}`}
                                style={{
                                    backgroundColor: color,
                                    borderColor: color
                                }}
                            >
                                <div className="box-value">{value}</div>
                            </div>

                            <div className="box-index">i={index}</div>
                        </div>
                    );
                })}
            </div>

            {arrayData.comparison && <div className="comparison-info">{arrayData.comparison}</div>}
        </div>
    );
};

export default ArrayVisualizer;
