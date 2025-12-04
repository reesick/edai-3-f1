// LinkedListVisualizer - Nodes with arrows (simple version)
import React from 'react';
import './LinkedListVisualizer.css';

const LinkedListVisualizer = ({ data }) => {
    if (!data || !data.values || data.values.length === 0) return null;

    return (
        <div className="ll-visualizer">
            <div className="ll-nodes-container">
                {data.values.map((value, index) => {
                    const isHighlighted = data.highlights?.indices?.includes(index);
                    const highlightIndex = data.highlights?.indices?.indexOf(index);
                    const color = isHighlighted ? (data.highlights.colors[highlightIndex] || '#3498db') : '#2ecc71';
                    const label = isHighlighted ? data.highlights.labels[highlightIndex] : null;

                    return (
                        <React.Fragment key={index}>
                            <div className="ll-node-box">
                                {label && <div className="ll-label">{label}</div>}
                                <div className="ll-node" style={{ backgroundColor: color }}>
                                    {value}
                                </div>
                            </div>
                            {index < data.values.length - 1 && <div className="ll-arrow">→</div>}
                        </React.Fragment>
                    );
                })}
                <div className="ll-null">NULL</div>
            </div>
        </div>
    );
};

export default LinkedListVisualizer;
