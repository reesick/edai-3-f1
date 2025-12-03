// Tree Visualizer - SVG hierarchical tree layout
// Used for binary trees, BST operations

import React from 'react';
import './TreeVisualizer.css';

const TreeVisualizer = ({ data }) => {
    if (!data || !data.nodes || data.nodes.length === 0) return null;

    const nodeMap = new Map(data.nodes.map(node => [node.id, node]));

    // Extract highlights
    const highlights = data.highlights || { node_ids: [], colors: [], labels: [] };
    const highlightMap = new Map();

    // Build highlight map for quick lookup
    if (highlights.node_ids) {
        highlights.node_ids.forEach((nodeId, index) => {
            highlightMap.set(nodeId, {
                color: highlights.colors?.[index] || '#f39c12',
                label: highlights.labels?.[index] || null
            });
        });
    }

    // Calculate SVG viewBox
    const margin = 60;
    const maxX = Math.max(...data.nodes.map(n => n.x)) + margin;
    const maxY = Math.max(...data.nodes.map(n => n.y)) + margin;

    return (
        <div className="tree-visualizer">
            <div className="structure-label">{data.name}</div>
            <svg
                className="tree-svg"
                viewBox={`0 0 ${maxX} ${maxY}`}
                preserveAspectRatio="xMidYMid meet"
            >
                {/* Draw edges first (so they appear under nodes) */}
                {data.nodes.map(node => {
                    const lines = [];
                    const isHighlighted = highlightMap.has(node.id);

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
                                    stroke={isHighlighted ? '#95a5a6' : '#555'}
                                    strokeWidth={isHighlighted ? '3' : '2'}
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
                                    stroke={isHighlighted ? '#95a5a6' : '#555'}
                                    strokeWidth={isHighlighted ? '3' : '2'}
                                />
                            );
                        }
                    }

                    return lines;
                })}

                {/* Draw nodes */}
                {data.nodes.map(node => {
                    const highlight = highlightMap.get(node.id);
                    const nodeColor = highlight ? highlight.color : '#3498db';
                    const isHighlighted = highlight !== undefined;

                    return (
                        <g key={`node-${node.id}`} className="tree-node-group">
                            {/* Node circle with glow effect for highlighted nodes */}
                            <circle
                                cx={node.x}
                                cy={node.y}
                                r="25"
                                fill={nodeColor}
                                className={`tree-node ${isHighlighted ? 'highlighted' : ''}`}
                                stroke="#fff"
                                strokeWidth="2"
                                style={isHighlighted ? {
                                    filter: 'drop-shadow(0 0 8px ' + nodeColor + ')'
                                } : {}}
                            />

                            {/* Node value */}
                            <text
                                x={node.x}
                                y={node.y}
                                className="tree-node-text"
                                textAnchor="middle"
                                dominantBaseline="central"
                            >
                                {node.value}
                            </text>

                            {/* Label above node */}
                            {highlight && highlight.label && (
                                <text
                                    x={node.x}
                                    y={node.y - 40}
                                    className="tree-node-label"
                                    textAnchor="middle"
                                    fill={nodeColor}
                                    fontWeight="bold"
                                    fontSize="12"
                                >
                                    {highlight.label}
                                </text>
                            )}
                        </g>
                    );
                })}
            </svg>
        </div>
    );
};

export default TreeVisualizer;
