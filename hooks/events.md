# Event Hooks — Event Emission and Handling

## Overview

Event hooks provide a publish-subscribe mechanism for communicating state changes, errors, and important moments throughout agent execution.

## Event Types

### Lifecycle Events

**`skill.loaded`**
- **When:** Skill is loaded into context
- **Payload:** `{"version": "1.0.0", "config": {...}}`
- **Subscribers:** Logger, metrics collector, state manager

**`skill.unloaded`**
- **When:** Skill is unloaded from context
- **Payload:** `{"reason": "...", "duration_ms": 1234}`
- **Subscribers:** Logger, state manager

### Request Events

**`request.started`**
- **When:** New user request begins processing
- **Payload:** `{"request_id": "...", "intent": "...", "input": {...}}`
- **Subscribers:** Logger, metrics collector, request tracker

**`request.routing`**
- **When:** Routing decision is made
- **Payload:** `{"request_id": "...", "sub_agents": [...], "mode": "..."}`
- **Subscribers:** Logger, routing analyzer

**`request.completed`**
- **When:** Request processing completes
- **Payload:** `{"request_id": "...", "duration_ms": 1234, "status": "..."}`
- **Subscribers:** Logger, metrics collector, request tracker

**`request.failed`**
- **When:** Request processing fails
- **Payload:** `{"request_id": "...", "error": "...", "duration_ms": 1234}`
- **Subscribers:** Logger, error tracker, alerting system

### Sub-Agent Events

**`sub_agent.started`**
- **When:** Sub-agent begins execution
- **Payload:** `{"sub_agent": "...", "request_id": "...", "input": {...}}`
- **Subscribers:** Logger, sub-agent tracker

**`sub_agent.progress`**
- **When:** Sub-agent makes progress
- **Payload:** `{"sub_agent": "...", "progress": 0.5, "message": "..."}`
- **Subscribers:** Logger, progress tracker

**`sub_agent.completed`**
- **When:** Sub-agent completes successfully
- **Payload:** `{"sub_agent": "...", "request_id": "...", "output": {...}}`
- **Subscribers:** Logger, metrics collector, sub-agent tracker

**`sub_agent.failed`**
- **When:** Sub-agent fails
- **Payload:** `{"sub_agent": "...", "request_id": "...", "error": "..."}`
- **Subscribers:** Logger, error tracker, alerting system

### Validation Events

**`validation.started`**
- **When:** Input/output validation begins
- **Payload:** `{"type": "...", "schema": "...", "data": {...}}`
- **Subscribers:** Logger, validation tracker

**`validation.completed`**
- **When:** Validation completes
- **Payload:** `{"type": "...", "valid": true, "errors": []}`
- **Subscribers:** Logger, validation tracker

**`validation.failed`**
- **When:** Validation fails
- **Payload:** `{"type": "...", "valid": false, "errors": [...]}`
- **Subscribers:** Logger, error tracker, validation reporter

### State Events

**`state.changed`**
- **When:** Agent state changes
- **Payload:** `{"key": "...", "old_value": "...", "new_value": "..."}`
- **Subscribers:** Logger, state tracker, persistence manager

**`state.snapshot`**
- **When:** State snapshot is created
- **Payload:** `{"snapshot_id": "...", "state": {...}}`
- **Subscribers:** Logger, persistence manager

### Performance Events

**`performance.threshold_exceeded`**
- **When:** Performance threshold is exceeded
- **Payload:** `{"metric": "...", "threshold": 123, "actual": 456}`
- **Subscribers:** Logger, performance monitor, alerting system

**`token.usage_warning`**
- **When:** Token usage approaches limit
- **Payload:** `{"used": 45000, "limit": 50000, "percentage": 90}`
- **Subscribers:** Logger, token monitor, alerting system

## Event Emission

Events can be emitted using the event emitter:

```python
class EventEmitter:
    def emit(self, event_type: str, payload: dict):
        """Emit an event to all subscribers"""
        for subscriber in self.subscribers[event_type]:
            subscriber.handle(event_type, payload)
```

### Example Event Emission

```python
# Emit request started event
event_bus.emit("request.started", {
    "request_id": "req-123",
    "intent": "formation-analysis",
    "input": {"formation": "4-3-3", "players": [...]}
})

# Emit sub-agent progress event
event_bus.emit("sub_agent.progress", {
    "sub_agent": "formation-analyzer",
    "progress": 0.6,
    "message": "Analyzing player positioning..."
})

# Emit validation failed event
event_bus.emit("validation.failed", {
    "type": "input",
    "valid": False,
    "errors": [
        "Missing required field: 'players'",
        "Invalid position: 'invalid-pos'"
    ]
})
```

## Event Subscription

Subscribers can register for specific event types:

```python
class EventSubscriber:
    def __init__(self, event_types: List[str]):
        self.event_types = event_types
    
    def handle(self, event_type: str, payload: dict):
        """Handle incoming event"""
        if event_type in self.event_types:
            self.process_event(event_type, payload)
    
    def process_event(self, event_type: str, payload: dict):
        """Process event (override in subclass)"""
        pass
```

### Example Subscribers

**Logger Subscriber**

```python
class LoggerSubscriber(EventSubscriber):
    def __init__(self):
        super().__init__([
            "skill.loaded", "skill.unloaded",
            "request.started", "request.completed",
            "sub_agent.started", "sub_agent.completed"
        ])
    
    def process_event(self, event_type: str, payload: dict):
        if event_type in ["skill.loaded", "skill.unloaded"]:
            logger.info(f"{event_type}: {payload}")
        elif event_type in ["request.started", "request.completed"]:
            logger.info(f"{event_type}: {payload['request_id']}")
        elif event_type in ["sub_agent.started", "sub_agent.completed"]:
            logger.debug(f"{event_type}: {payload['sub_agent']}")
```

**Metrics Subscriber**

```python
class MetricsSubscriber(EventSubscriber):
    def __init__(self):
        super().__init__([
            "request.completed", "request.failed",
            "sub_agent.completed", "sub_agent.failed"
        ])
        self.metrics = {}
    
    def process_event(self, event_type: str, payload: dict):
        if event_type == "request.completed":
            duration = payload.get("duration_ms", 0)
            self.metrics["request_duration"] = duration
        elif event_type == "sub_agent.completed":
            sub_agent = payload["sub_agent"]
            if sub_agent not in self.metrics:
                self.metrics[sub_agent] = {"count": 0, "total_duration": 0}
            self.metrics[sub_agent]["count"] += 1
```

**Alerting Subscriber**

```python
class AlertingSubscriber(EventSubscriber):
    def __init__(self):
        super().__init__([
            "request.failed", "sub_agent.failed",
            "validation.failed", "performance.threshold_exceeded"
        ])
    
    def process_event(self, event_type: str, payload: dict):
        if event_type == "request.failed":
            self.send_alert(f"Request failed: {payload['request_id']}", payload)
        elif event_type == "sub_agent.failed":
            self.send_alert(f"Sub-agent failed: {payload['sub_agent']}", payload)
        elif event_type == "validation.failed":
            self.send_alert("Validation failed", payload)
        elif event_type == "performance.threshold_exceeded":
            self.send_alert(f"Performance issue: {payload['metric']}", payload)
    
    def send_alert(self, message: str, payload: dict):
        """Send alert (implementation depends on alerting system)"""
        logger.warning(f"ALERT: {message}")
```

## Event Bus Configuration

The event bus can be configured via the skill configuration:

```json
{
  "event_bus": {
    "enabled": true,
    "subscribers": [
      "logger",
      "metrics",
      "alerting"
    ],
    "filter_events": [],
    "buffer_size": 1000
  }
}
```

## Event Filtering

Events can be filtered to reduce noise:

```python
class EventFilter:
    def __init__(self, allowed_events: List[str]):
        self.allowed_events = set(allowed_events)
    
    def should_emit(self, event_type: str) -> bool:
        return event_type in self.allowed_events
```

## Event Buffers

For high-frequency events, buffering can be used:

```python
class EventBuffer:
    def __init__(self, buffer_size: int = 1000):
        self.buffer = []
        self.buffer_size = buffer_size
    
    def buffer_event(self, event_type: str, payload: dict):
        """Buffer event for batch processing"""
        self.buffer.append({"type": event_type, "payload": payload})
        
        if len(self.buffer) >= self.buffer_size:
            self.flush_buffer()
    
    def flush_buffer(self):
        """Flush buffered events"""
        for event in self.buffer:
            process_event(event["type"], event["payload"])
        self.buffer.clear()
```

## Best Practices

1. **Event Naming:** Use descriptive, hierarchical event names (e.g., `sub_agent.progress` not `progress`)
2. **Payload Consistency:** Maintain consistent payload structures for similar events
3. **Async Processing:** Handle events asynchronously to avoid blocking
4. **Error Isolation:** Isolate subscriber errors to prevent cascade failures
5. **Event Documentation:** Document all event types and their payloads

