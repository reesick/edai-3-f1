import React from 'react';
import './StackVisualizer.css';

export default function StackVisualizer({ data, highlights = {} }) {
    // ModulePage passes data as {values: [...], highlights: {...}}
    // Extract values - handle both {values: [...]} and direct array
    const values = data?.values || (Array.isArray(data) ? data : []);

    if (!values || values.length === 0) {
        return (
            <div className="stack-visualizer">
                <div className="stack-container">
                    <div className="empty-stack">
                        <div className="stack-base">EMPTY STACK</div>
                    </div>
                </div>
            </div>
        );
    }

    // Stack displays bottom-to-top, so reverse for visualization
    // values[0] = bottom, values[n-1] = top
    const stackElements = [...values].reverse(); // Top element first visually

    return (
        <div className="stack-visualizer">
            <div className="stack-container">
                {stackElements.map((value, visualIndex) => {
                    // Actual index in original array (before reverse)
                    const actualIndex = values.length - 1 - visualIndex;
                    const isHighlighted = highlights.indices?.includes(actualIndex);
                    const color = isHighlighted ? highlights.colors?.[highlights.indices.indexOf(actualIndex)] : '#2ecc71';
                    const label = isHighlighted ? highlights.labels?.[highlights.indices.indexOf(actualIndex)] : '';
                    const isTop = actualIndex === values.length - 1;

                    return (
                        <div key={actualIndex} className="stack-element-wrapper">
                            {label && <div className="stack-label">{label}</div>}
                            <div
                                className={`stack-element ${isTop ? 'top-element' : ''}`}
                                style={{
                                    backgroundColor: color,
                                    borderColor: color
                                }}
                            >
                                <span className="stack-value">{value}</span>
                            </div>
                            {isTop && <div className="top-indicator">← TOP</div>}
                        </div>
                    );
                })}
                <div className="stack-base">BOTTOM</div>
            </div>
        </div>
    );
}
