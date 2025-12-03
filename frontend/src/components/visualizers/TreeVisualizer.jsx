// Tree Visualizer - SVG hierarchical tree layout
// Used for binary trees, BST operations

import React from 'react';
import './TreeVisualizer.css';

const TreeVisualizer = ({ data }) => {
    if (!data || !data.nodes || data.nodes.length === 0) return null;

    const nodeMap = new Map(data.nodes.map(node => [node.id, node]));

    // Calculate SVG viewBox
    const margin = 60;
    const maxX = Math.max(...data.nodes.map(n => n.x)) + margin;
    const maxY = Math.max(...data.nodes.map(n => n.y)) + margin;

    return (
        <div className="tree-visualizer">
            <div className="structure-label">{data.name} ({data.type})</div>
            <svg
                className="tree-svg"
                viewBox={`0 0 ${maxX} ${maxY}`}
                preserveAspectRatio="xMidYMid meet"
            >
                {/* Draw edges first (so they appear under nodes) */}
                {data.nodes.map(node => {
                    const lines = [];

                    // Left child edge
                    if (node.left_child_id !== null && node.left_child_id !== undefined) {
                        const leftChild = nodeMap.get(node.left_child_id);
                        if (leftChild) {
                            lines.push(
                                <line
                                    key={`edge-${node.id}-left`}
                                    x1={node.x}
                                    y1={node.y}
                                    x2={leftChild.x}
                                    y2={leftChild.y}
                                    className="tree-edge"
                                    stroke={node.highlighted ? '#4f9bff' : '#555'}
                                />
                            );
                        }
                    }

                    // Right child edge
                    if (node.right_child_id !== null && node.right_child_id !== undefined) {
                        const rightChild = nodeMap.get(node.right_child_id);
                        if (rightChild) {
                            lines.push(
                                <line
                                    key={`edge-${node.id}-right`}
                                    x1={node.x}
                                    y1={node.y}
                                    x2={rightChild.x}
                                    y2={rightChild.y}
                                    className="tree-edge"
                                    stroke={node.highlighted ? '#4f9bff' : '#555'}
                                />
                            );
                        }
                    }

                    return lines;
                })}

                {/* Draw nodes */}
                {data.nodes.map(node => {
                    const nodeColor = node.highlighted
                        ? (node.color === 'default' ? '#4f9bff' : node.color)
                        : (node.color === 'default' ? '#3498db' : node.color);

                    return (
                        <g key={`node-${node.id}`} className="tree-node-group">
                            <circle
                                cx={node.x}
                                cy={node.y}
                                r="25"
                                fill={nodeColor}
                                className={`tree-node ${node.highlighted ? 'highlighted' : ''}`}
                                stroke="#fff"
                                strokeWidth="2"
                            />
                            <text
                                x={node.x}
                                y={node.y}
                                className="tree-node-text"
                                textAnchor="middle"
                                dominantBaseline="central"
                            >
                                {node.value}
                            </text>
                        </g>
                    );
                })}
            </svg>
        </div>
    );
};

export default TreeVisualizer;
