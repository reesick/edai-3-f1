// Linked List Visualizer - Horizontal nodes with arrows
// Used for linked list operations

import React from 'react';
import './LinkedListVisualizer.css';

const LinkedListVisualizer = ({ data }) => {
    if (!data || !data.nodes || data.nodes.length === 0) return null;

    return (
        <div className="linkedlist-visualizer">
            <div className="structure-label">{data.name} ({data.type})</div>
            <div className="linkedlist-container">
                {data.nodes.map((node, index) => {
                    const hasNext = node.next !== null && node.next !== undefined;
                    const nodeColor = node.highlighted
                        ? (node.color === 'default' ? '#4f9bff' : node.color)
                        : (node.color === 'default' ? '#3498db' : node.color);

                    return (
                        <React.Fragment key={index}>
                            <div
                                className={`linkedlist-node ${node.highlighted ? 'highlighted' : ''}`}
                                style={{ backgroundColor: nodeColor }}
                            >
                                <div className="node-value">{node.value}</div>
                                {index === 0 && (
                                    <div className="node-label head-label">head</div>
                                )}
                                {index === data.nodes.length - 1 && (
                                    <div className="node-label tail-label">tail</div>
                                )}
                                <div className="node-next-box">→</div>
                            </div>
                            {hasNext && (
                                <div className="linkedlist-arrow">
                                    <svg width="40" height="20" viewBox="0 0 40 20">
                                        <line x1="0" y1="10" x2="30" y2="10" stroke="#4f9bff" strokeWidth="2" />
                                        <polygon points="30,10 25,7 25,13" fill="#4f9bff" />
                                    </svg>
                                </div>
                            )}
                            {!hasNext && (
                                <div className="linkedlist-arrow">
                                    <div className="linkedlist-null">NULL</div>
                                </div>
                            )}
                        </React.Fragment>
                    );
                })}
            </div>
        </div>
    );
};

export default LinkedListVisualizer;
