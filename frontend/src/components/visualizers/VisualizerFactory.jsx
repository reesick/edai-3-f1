// Visualizer Factory - Dispatcher Component
// Auto-detects data structure type and routes to appropriate visualizer

import React from 'react';
import ArrayVisualizer from './ArrayVisualizer';
import TreeVisualizer from './TreeVisualizer';
import GraphVisualizer from './GraphVisualizer';
import LinkedListVisualizer from './LinkedListVisualizer';
import StackVisualizer from './StackVisualizer';
import QueueVisualizer from './QueueVisualizer';
import './VisualizerFactory.css';

const VariablesPanel = ({ variables }) => {
    if (!variables || variables.length === 0) return null;

    return (
        <div className="variables-panel">
            <div className="structure-label">Variables</div>
            <div className="variables-grid">
                {variables.map((variable, index) => (
                    <div key={index} className="variable-item">
                        <span className="variable-name">{variable.name}</span>
                        <span className="variable-value">{variable.value}</span>
                        <span className="variable-type">{variable.type}</span>
                    </div>
                ))}
            </div>
        </div>
    );
};

const VisualizerFactory = ({ frame, currentFrameIndex, totalFrames }) => {
    if (!frame) {
        return (
            <div className="visualizer-factory">
                <div className="visualizer-placeholder">
                    <div className="placeholder-icon">🎨</div>
                    <div className="placeholder-text">
                        Run your code to see visualization
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="visualizer-factory">
            <div className="visualizer-header">
                <span className="visualizer-title">Visualization</span>
                <span className="frame-counter">
                    Frame {currentFrameIndex + 1} / {totalFrames}
                </span>
            </div>

            <div className="visualizer-content">
                <div className="frame-description">{frame.description}</div>

                <div className="structures-grid">
                    {/* Arrays */}
                    {frame.arrays?.map((arr, index) => (
                        <ArrayVisualizer key={`array-${index}`} data={arr} />
                    ))}

                    {/* Trees */}
                    {frame.trees?.map((tree, index) => (
                        <TreeVisualizer key={`tree-${index}`} data={tree} />
                    ))}

                    {/* Graphs */}
                    {frame.graphs?.map((graph, index) => (
                        <GraphVisualizer key={`graph-${index}`} data={graph} />
                    ))}

                    {/* Linked Lists */}
                    {frame.linked_lists?.map((list, index) => (
                        <LinkedListVisualizer key={`list-${index}`} data={list} />
                    ))}

                    {/* Stacks */}
                    {frame.stacks?.map((stack, index) => (
                        <StackVisualizer key={`stack-${index}`} data={stack} />
                    ))}

                    {/* Queues */}
                    {frame.queues?.map((queue, index) => (
                        <QueueVisualizer key={`queue-${index}`} data={queue} />
                    ))}
                </div>

                {/* Variables Panel */}
                <VariablesPanel variables={frame.variables} />
            </div>
        </div>
    );
};

export default VisualizerFactory;
