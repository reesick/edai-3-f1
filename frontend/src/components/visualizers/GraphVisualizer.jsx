// Graph Visualizer - Nodes and edges visualization
// Used for BFS, DFS, Dijkstra, etc.

import React from 'react';
import './GraphVisualizer.css';

const GraphVisualizer = ({ data }) => {
    if (!data || !data.nodes || data.nodes.length === 0) return null;

    const margin = 60;
    const maxX = Math.max(...data.nodes.map(n => n.x)) + margin;
    const maxY = Math.max(...data.nodes.map(n => n.y)) + margin;

    return (
        <div className="graph-visualizer">
            <div className="structure-label">{data.name} ({data.type})</div>
            <svg
                className="graph-svg"
                viewBox={`0 0 ${maxX} ${maxY}`}
                preserveAspectRatio="xMidYMid meet"
            >
                {/* Draw edges */}
                {data.edges?.map((edge, index) => {
                    const fromNode = data.nodes.find(n => n.id === edge.from_node);
                    const toNode = data.nodes.find(n => n.id === edge.to_node);

                    if (!fromNode || !toNode) return null;

                    const edgeColor = edge.highlighted ? '#4f9bff' : '#555';

                    return (
                        <g key={`edge-${index}`}>
                            <line
                                x1={fromNode.x}
                                y1={fromNode.y}
                                x2={toNode.x}
                                y2={toNode.y}
                                className={`graph-edge ${edge.highlighted ? 'highlighted' : ''}`}
                                stroke={edgeColor}
                                markerEnd={edge.directed ? 'url(#arrowhead)' : ''}
                            />
                            {edge.weight !== null && edge.weight !== undefined && (
                                <text
                                    x={(fromNode.x + toNode.x) / 2}
                                    y={(fromNode.y + toNode.y) / 2}
                                    className="edge-weight"
                                    fill="#ffd700"
                                >
                                    {edge.weight}
                                </text>
                            )}
                        </g>
                    );
                })}

                {/* Arrowhead marker for directed graphs */}
                <defs>
                    <marker
                        id="arrowhead"
                        markerWidth="10"
                        markerHeight="10"
                        refX="5"
                        refY="3"
                        orient="auto"
                    >
                        <polygon points="0 0, 10 3, 0 6" fill="#555" />
                    </marker>
                </defs>

                {/* Draw nodes */}
                {data.nodes.map(node => {
                    const nodeColor = node.highlighted
                        ? (node.color === 'default' ? '#4f9bff' : node.color)
                        : (node.color === 'default' ? '#3498db' : node.color);

                    return (
                        <g key={`node-${node.id}`} className="graph-node-group">
                            <circle
                                cx={node.x}
                                cy={node.y}
                                r="30"
                                fill={nodeColor}
                                className={`graph-node ${node.highlighted ? 'highlighted' : ''}`}
                                stroke="#fff"
                                strokeWidth="2"
                            />
                            <text
                                x={node.x}
                                y={node.y}
                                className="graph-node-text"
                                textAnchor="middle"
                                dominantBaseline="central"
                            >
                                {node.label}
                            </text>
                        </g>
                    );
                })}
            </svg>
        </div>
    );
};

export default GraphVisualizer;
