// Queue Visualizer - Horizontal FIFO queue
// Used for queue operations

import React from 'react';
import './QueueVisualizer.css';

const QueueVisualizer = ({ data }) => {
    if (!data || !data.values) return null;

    return (
        <div className="queue-visualizer">
            <div className="structure-label">{data.name}</div>
            <div className="queue-container">
                {data.values.map((value, index) => {
                    const isFront = index === data.front_index;
                    const isRear = index === data.rear_index;
                    const isHighlighted = data.highlights?.indices?.includes(index);

                    return (
                        <div
                            key={index}
                            className={`queue-element ${isHighlighted ? 'highlighted' : ''}`}
                        >
                            {isFront && <div className="queue-label front-label">FRONT</div>}
                            {isRear && <div className="queue-label rear-label">REAR</div>}
                            <div className="queue-value">{value}</div>
                            <div className="queue-index">{index}</div>
                        </div>
                    );
                })}
                {data.values.length === 0 && (
                    <div className="queue-empty">Queue is empty</div>
                )}
            </div>
        </div>
    );
};

export default QueueVisualizer;
