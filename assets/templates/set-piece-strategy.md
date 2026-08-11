# Set-Piece Strategy Sheet

**Generated:** {{timestamp}}
**Set-Piece Type:** {{set_piece_type}}
**Attacking/Defending:** {{attacking_or_defending}}
**Field Position:** {{field_position}}

---

## Executive Summary

{{summary}}

---

## {{set_piece_type}} Strategy

### Setup

**Personnel:**

| Role | Player | Responsibility |
|------|--------|----------------|
{{personnel_assignments}}

**Positioning:**

```
{{positioning_diagram}}
```

---

## Delivery Zones

### Zone {{zone_number}}: {{zone_name}} ({{percentage}}% of deliveries)

**Delivery Type:** {{delivery_type}}
**Trajectory:** {{trajectory}}

**Target:**

{{target_description}}

**Movement Pattern:**

{{#each movements}}
- **{{this.player}}:** {{this.movement}}
{{/each}}

---

## Attacking Routines

### Routine 1: {{routine_1_name}}

**Setup:** {{routine_1_setup}}

**Execution:**

1. {{routine_1_step_1}}
2. {{routine_1_step_2}}
3. {{routine_1_step_3}}

**Coaching Points:** {{routine_1_coaching_points}}

### Routine 2: {{routine_2_name}}

**Setup:** {{routine_2_setup}}

**Execution:**

1. {{routine_2_step_1}}
2. {{routine_2_step_2}}
3. {{routine_2_step_3}}

**Coaching Points:** {{routine_2_coaching_points}}

---

## Defensive Organization

### {{defensive_system}} Marking System

**Setup:** {{defensive_setup}}

**Positioning:**

```
{{defensive_diagram}}
```

**Responsibilities:**

{{#each defensive_responsibilities}}
- **{{this.position}}:** {{this.responsibility}}
{{/each}}

**Key Principles:**

{{#each defensive_principles}}
- {{this}}
{{/each}}

---

## xG Analysis

**Set-Piece xG:** {{xg_value}}

**Breakdown:**

- **Base xG:** {{base_xg}}
- **Delivery Quality:** {{delivery_modifier}}
- **Personnel Quality:** {{personnel_modifier}}
- **Opponent Weakness:** {{opponent_modifier}}

**Optimization Opportunities:**

{{optimization_opportunities}}

---

## Game State Adaptations

| Game State | Approach | Adjustment |
|------------|----------|------------|
{{game_state_adjustments}}

---

## Opponent Analysis

### {{opponent}} Set-Piece Profile

**Strengths:**

{{#each opponent_strengths}}
- {{this}}
{{/each}}

**Weaknesses:**

{{#each opponent_weaknesses}}
- {{this}}
{{/each}}

**Exploitation Strategy:**

{{exploitation_strategy}}

---

## Training Focus

**Key Elements to Train:**

{{#each training_elements}}
- **{{this.element}}:** {{this.focus}}
{{/each}}

**Drill Progression:**

1. {{drill_step_1}}
2. {{drill_step_2}}
3. {{drill_step_3}}

**Success Criteria:**

{{#each success_criteria}}
- {{this}}
{{/each}}

---

## Performance Tracking

**Metrics to Monitor:**

- **Shots per Set-Piece:** Target {{target_shots}}
- **xG per Set-Piece:** Target {{target_xg}}
- **Conversion Rate:** Target {{target_conversion}}

**Recent Performance:**

{{recent_performance}}

---

## Methodology

This set-piece strategy is based on:

- **Delivery Optimization:** Targeting high-probability zones
- **Movement Coordination:** Synchronized attacking runs
- **Defensive Organization:** Structured marking systems
- **xG Analysis:** Evidence-based decision making

**References:**
- Set-Piece Framework: `references/set-pieces/set-piece-catalog.md`
- xG Analysis: `references/analytics/xg-framework.md`

---

**Disclaimer:** Set-piece strategies should be adjusted based on opponent defensive organization, goalkeeper positioning, and match state. Regular review and adaptation are essential for continued effectiveness.

