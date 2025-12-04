import React from 'react';
import VisualizerControls from './VisualizerControls';
import VisualizerFactory from './visualizers/VisualizerFactory';
import ArrayVisualizer from './visualizers/ArrayVisualizer';
import LinkedListVisualizer from './visualizers/LinkedListVisualizer';
import StackVisualizer from './visualizers/StackVisualizer';
import './Visualizer.css';

export default function Visualizer({ module, data, highlights = [], controlsProps }) {
    if (!data) {
        return (
            <div className="visualizer-container">
                <div className="visualizer">
                    <div className="empty-viz">
                        <p className="text-muted">Click "Run" to see visualization</p>
                    </div>
                </div>
                {controlsProps && <VisualizerControls {...controlsProps} />}
            </div>
        );
    }

    // Render based on module type
    const renderVisualization = () => {
        switch (module) {
            case 'array':
            case 'sorting':
            case 'searching':
                return <ArrayVisualizer data={data} highlights={highlights} />;
            case 'linkedlist':
                // Use LinkedListVisualizer for linked lists (horizontal layout)
                return <LinkedListVisualizer data={data} highlights={highlights} />;
            case 'stack':
                // Use StackVisualizer for stacks (VERTICAL layout)
                return <StackVisualizer data={data} highlights={highlights} />;
            case 'bitmask':
                return <BitmaskVisualizer data={data} highlights={highlights} />;
            case 'binaryheap':
                return <HeapVisualizer data={data} highlights={highlights} />;
            case 'trees':
                // Trees use the VisualizerFactory which handles complex frame structures
                return <VisualizerFactory frame={data} currentFrameIndex={controlsProps?.currentStep || 0} totalFrames={controlsProps?.totalSteps || 1} />;
            default:
                return <div>Unsupported module type: {module}</div>;
        }
    };

    return (
        <div className="visualizer-container">
            <div className="visualizer">
                {renderVisualization()}
            </div>
            {controlsProps && <VisualizerControls {...controlsProps} />}
        </div>
    );
}
