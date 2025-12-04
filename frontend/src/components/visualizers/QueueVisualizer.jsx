import React from 'react';
import './QueueVisualizer.css';

export default function QueueVisualizer({ data, highlights = {} }) {
    // Extract values - handle both {values: [...]} and direct array
    const values = data?.values || (Array.isArray(data) ? data : []);

    if (!values || values.length === 0) {
        return (
            <div className="queue-visualizer">
                <div className="queue-container">
                    <div className="empty-queue">EMPTY QUEUE</div>
                </div>
            </div>
        );
    }

    // Queue displays left-to-right: FRONT ← [...] ← REAR
    return (
        <div className="queue-visualizer">
            <div className="queue-header">
                <div className="queue-label front-label">FRONT</div>
                <div className="queue-label rear-label">REAR</div>
            </div>

            <div className="queue-container">
                {values.map((value, index) => {
                    const isHighlighted = highlights.indices?.includes(index);
                    const color = isHighlighted ? highlights.colors?.[highlights.indices.indexOf(index)] : '#2ecc71';
                    const label = isHighlighted ? highlights.labels?.[highlights.indices.indexOf(index)] : '';
                    const isFront = index === 0;
                    const isRear = index === values.length - 1;

                    return (
                        <div key={index} className="queue-element-wrapper">
                            {label && <div className="queue-element-label">{label}</div>}
                            <div
                                className={`queue-element ${isFront ? 'front-element' : ''} ${isRear ? 'rear-element' : ''}`}
                                style={{
                                    backgroundColor: color,
                                    borderColor: color
                                }}
                            >
                                <span className="queue-value">{value}</span>
                            </div>
                        </div>
                    );
                })}
            </div>

            <div className="queue-footer">
                <div className="operation-label dequeue-label">← Dequeue</div>
                <div className="operation-label enqueue-label">Enqueue →</div>
            </div>
        </div>
    );
}
