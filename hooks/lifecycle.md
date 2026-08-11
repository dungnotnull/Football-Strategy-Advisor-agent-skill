# Lifecycle Hooks — Agent Lifecycle Management

## Overview

Lifecycle hooks provide control points throughout the agent execution flow, allowing for custom behavior at key stages of operation.

## Hook Types

### Initialization Hooks

**`on_skill_load`**
- **Trigger:** When the skill is first loaded into context
- **Purpose:** Initialize resources, validate configuration, set up logging
- **Parameters:** `config` (configuration object)
- **Return:** `initialized_state` (object with initialized resources)

```python
def on_skill_load(config):
    """Initialize skill resources"""
    logger = setup_logging(config.logging)
    schemas = load_validation_schemas()
    return {"logger": logger, "schemas": schemas}
```

### Request Hooks

**`on_request_start`**
- **Trigger:** When a new user request arrives
- **Purpose:** Validate input, log request start, initialize request context
- **Parameters:** `request` (user request object), `state` (current agent state)
- **Return:** `request_context` (initialized request context)

```python
def on_request_start(request, state):
    """Initialize request processing"""
    logger = state["logger"]
    logger.info(f"Processing request: {request.intent}")
    
    validated_input = validate_input(request.input_data, state["schemas"])
    request_context = {
        "validated_input": validated_input,
        "start_time": current_time(),
        "request_id": generate_id()
    }
    return request_context
```

**`on_routing_decision`**
- **Trigger:** When determining which sub-agent(s) to invoke
- **Purpose:** Analyze request intent, select appropriate sub-agent(s)
- **Parameters:** `request_context` (current request context), `state` (agent state)
- **Return:** `routing_decision` (selected sub-agents and execution plan)

```python
def on_routing_decision(request_context, state):
    """Determine routing to sub-agents"""
    intent = request_context["validated_input"]["intent"]
    
    if intent in ["formation", "lineup", "system"]:
        return {"sub_agents": ["formation-analyzer"], "mode": "sequential"}
    elif intent in ["pressing", "defensive", "block"]:
        return {"sub_agents": ["pressing-specialist"], "mode": "sequential"}
    elif intent in ["corner", "free-kick", "set-piece"]:
        return {"sub_agents": ["set-piece-coordinator"], "mode": "sequential"}
    elif intent in ["xg", "analytics", "opponent"]:
        return {"sub_agents": ["analytics-engine"], "mode": "sequential"}
    elif intent in ["training", "session", "periodization"]:
        return {"sub_agents": ["training-architect"], "mode": "sequential"}
    else:
        return {"sub_agents": [], "mode": "error"}
```

### Execution Hooks

**`on_sub_agent_start`**
- **Trigger:** When a sub-agent begins execution
- **Purpose:** Log sub-agent start, initialize sub-agent context
- **Parameters:** `sub_agent_name` (name of sub-agent), `request_context` (request context)
- **Return:** `sub_agent_context` (initialized sub-agent context)

```python
def on_sub_agent_start(sub_agent_name, request_context):
    """Initialize sub-agent execution"""
    logger.info(f"Starting sub-agent: {sub_agent_name}")
    
    sub_agent_context = {
        "sub_agent": sub_agent_name,
        "start_time": current_time(),
        "parent_request_id": request_context["request_id"]
    }
    return sub_agent_context
```

**`on_sub_agent_complete`**
- **Trigger:** When a sub-agent completes execution
- **Purpose:** Log completion, validate output, update request context
- **Parameters:** `sub_agent_context` (sub-agent context), `output` (sub-agent output)
- **Return:** `updated_context` (updated request context)

```python
def on_sub_agent_complete(sub_agent_context, output):
    """Process sub-agent completion"""
    logger.info(f"Sub-agent {sub_agent_context['sub_agent']} completed")
    
    # Validate output
    validated_output = validate_output(output, schemas)
    
    # Update context
    updated_context = {
        "outputs": sub_agent_context.get("outputs", []) + [validated_output],
        "completion_time": current_time()
    }
    return updated_context
```

**`on_sub_agent_error`**
- **Trigger:** When a sub-agent encounters an error
- **Purpose:** Log error, determine recovery strategy, attempt graceful fallback
- **Parameters:** `sub_agent_context` (sub-agent context), `error` (error object)
- **Return:** `error_recovery` (recovery strategy and fallback response)

```python
def on_sub_agent_error(sub_agent_context, error):
    """Handle sub-agent error"""
    logger.error(f"Sub-agent {sub_agent_context['sub_agent']} error: {error}")
    
    # Determine recovery strategy
    if is_recoverable(error):
        fallback_response = generate_fallback_response(sub_agent_context)
        return {
            "strategy": "fallback",
            "response": fallback_response,
            "error_logged": True
        }
    else:
        return {
            "strategy": "propagate",
            "error": error,
            "error_logged": True
        }
```

### Response Hooks

**`on_response_generation`**
- **Trigger:** When generating the final response to the user
- **Purpose:** Synthesize outputs, format response, apply templates
- **Parameters:** `request_context` (request context), `outputs` (all sub-agent outputs)
- **Return:** `formatted_response` (final formatted response)

```python
def on_response_generation(request_context, outputs):
    """Generate final response"""
    logger.info("Generating final response")
    
    # Synthesize outputs
    synthesized = synthesize_outputs(outputs)
    
    # Apply template
    formatted = apply_template(synthesized, request_context["validated_input"])
    
    return formatted
```

**`on_response_complete`**
- **Trigger:** When the response is complete and ready to send
- **Purpose:** Final validation, logging, metrics collection
- **Parameters:** `response` (formatted response), `request_context` (request context)
- **Return:** `final_response` (validated final response)

```python
def on_response_complete(response, request_context):
    """Final response preparation"""
    # Validate response
    validated_response = validate_final_response(response)
    
    # Collect metrics
    duration = current_time() - request_context["start_time"]
    logger.info(f"Request completed in {duration}s")
    
    return validated_response
```

### Cleanup Hooks

**`on_request_cleanup`**
- **Trigger:** After response is sent to the user
- **Purpose:** Clean up resources, release memory, final logging
- **Parameters:** `request_context` (request context)
- **Return:** `cleanup_status` (status of cleanup)

```python
def on_request_cleanup(request_context):
    """Clean up after request"""
    logger.info(f"Cleaning up request {request_context['request_id']}")
    
    # Release resources
    release_resources(request_context)
    
    return {"status": "cleaned", "request_id": request_context["request_id"]}
```

**`on_skill_unload`**
- **Trigger:** When the skill is being unloaded from context
- **Purpose:** Final cleanup, resource release, state persistence
- **Parameters:** `state` (current agent state)
- **Return:** `cleanup_status` (status of cleanup)

```python
def on_skill_unload(state):
    """Clean up skill resources"""
    logger.info("Unloading skill")
    
    # Persist any necessary state
    persist_state(state)
    
    # Release resources
    release_all_resources(state)
    
    return {"status": "unloaded"}
```

## Error Handling

All hooks should implement error handling with these principles:

1. **Log First:** Always log errors before attempting recovery
2. **Graceful Degradation:** Provide fallback responses when possible
3. **Error Propagation:** Propagate critical errors that cannot be handled
4. **State Preservation:** Maintain state consistency even during errors

```python
def hook_with_error_handling(param):
    try:
        # Hook logic
        result = process(param)
        return result
    except RecoverableError as e:
        logger.warning(f"Recoverable error: {e}")
        return fallback_response(param)
    except CriticalError as e:
        logger.error(f"Critical error: {e}")
        raise e
```

## Performance Considerations

1. **Minimize Hook Overhead:** Keep hooks lightweight and focused
2. **Avoid Blocking Operations:** Use async operations where possible
3. **Cache When Appropriate:** Cache results of expensive hook operations
4. **Monitor Hook Performance:** Track hook execution times

## Hook Configuration

Hooks can be configured via the skill configuration:

```json
{
  "hooks": {
    "enabled": [
      "on_skill_load",
      "on_request_start",
      "on_routing_decision",
      "on_sub_agent_start",
      "on_sub_agent_complete",
      "on_sub_agent_error",
      "on_response_generation",
      "on_response_complete",
      "on_request_cleanup",
      "on_skill_unload"
    ],
    "disabled": [],
    "custom_hooks": {}
  }
}
```

