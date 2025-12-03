// Stack Visualizer - Vertical LIFO stack
// Used for stack operations

import React from 'react';
import './StackVisualizer.css';

const StackVisualizer = ({ data }) => {
    if (!data || !data.values) return null;

    const reversedValues = [...data.values].reverse(); // Top at array end

    return (
        <div className="stack-visualizer">
            <div className="structure-label">{data.name}</div>
            <div className="stack-container">
                {reversedValues.map((value, index) => {
                    const actualIndex = data.values.length - 1 - index;
                    const isHighlighted = data.highlights?.indices?.includes(actualIndex);
                    const isTop = actualIndex === data.values.length - 1;

                    return (
                        <div
                            key={index}
                            className={`stack-element ${isHighlighted ? 'highlighted' : ''} ${isTop ? 'top' : ''}`}
                        >
                            <div className="stack-value">{value}</div>
                            {isTop && <div className="top-label">TOP</div>}
                        </div>
                    );
                })}
                {data.values.length === 0 && (
                    <div className="stack-empty">Stack is empty</div>
                )}
            </div>
        </div>
    );
};

export default StackVisualizer;
