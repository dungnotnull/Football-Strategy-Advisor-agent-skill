---
name: football-strategy-advisor
description: Tactical analysis and strategy support for football (soccer) — formation design, pressing structures, set-piece optimization, xG analytics, opponent scouting, and training periodization grounded in elite coaching methodology and sports analytics research. ALWAYS use this skill whenever the user mentions football tactics, soccer strategy, formations, pressing, set pieces, coaching, match analysis, opponent analysis, training sessions, or any request related to football/soccer tactical decision-making even if they don't explicitly use these exact terms.
compatibility:
  - python>=3.8
  - claude-code>=1.0
---

# Football Strategy Advisor

A production-grade skill for football (soccer) tactical analysis, supporting coaches, analysts, and enthusiasts with evidence-based strategy recommendations grounded in elite coaching methodology and sports analytics research.

## Skill Registry

This skill uses a modular sub-agent architecture. Each sub-agent specializes in a specific domain of football tactics:

| Sub-Agent | Domain | Trigger Keywords |
|------------|--------|------------------|
| `formation-analyzer` | Formation/system design | formation, system, lineup, shape, structure |
| `pressing-specialist` | Pressing & defensive blocks | press, pressing, defensive block, counter-press, gegenpress |
| `set-piece-coordinator` | Set-piece strategy | corner, free kick, set piece, dead ball |
| `analytics-engine` | Match analytics & xG | xG, expected goals, analytics, stats, performance |
| `training-architect` | Training periodization | training, session, periodization, fitness, conditioning |

## Routing Logic

When a request arrives, analyze the primary intent and route to the appropriate sub-agent:

1. **Formation Analysis** → `formation-analyzer`
   - Squad profile analysis
   - Formation recommendations based on personnel
   - System matchups and counters

2. **Pressing & Defensive Structure** → `pressing-specialist`
   - High press, mid-block, low block design
   - Pressing triggers and coordination
   - Defensive transition organization

3. **Set-Piece Strategy** → `set-piece-coordinator`
   - Corner kick routines (attack/defense)
   - Free kick strategies
   - Positioning and movement patterns

4. **Match Analytics** → `analytics-engine`
   - Expected goals (xG) analysis
   - Possession-value evaluation
   - Opponent tendency analysis
   - Performance metrics

5. **Training Design** → `training-architect`
   - Session design based on tactical objectives
   - Periodization planning
   - Training load management

**Multi-domain requests:** If a request spans multiple domains, synthesize inputs from relevant sub-agents and present an integrated recommendation.

## Core Methodologies

All recommendations in this skill are grounded in established frameworks. Always cite the methodology being applied:

### Positional Play (Juego de Posición)
Reference: `references/formations/positional-play.md`

### Expected Goals (xG) Framework
Reference: `references/analytics/xg-framework.md`

### Pressing Triggers & Block Theory
Reference: `references/pressing/pressing-triggers.md`

### Periodization (Bondarchuk/Matveyev)
Reference: `references/training/periodization.md`

### Set-Piece Optimization
Reference: `references/set-pieces/set-piece-catalog.md`

## Input Validation

All inputs must be validated against their respective schemas before processing:

- **Formation Analysis:** `references/schemas/formation-input.json`
- **Pressing Structure:** `references/schemas/pressing-input.json`
- **Set-Piece Design:** `references/schemas/set-piece-input.json`
- **Analytics Query:** `references/schemas/analytics-input.json`
- **Training Request:** `references/schemas/training-input.json`

If validation fails, return a structured error with:
- The specific validation error
- Expected format
- Example of correct input

## Output Structure

All outputs must follow these templates for consistency:

### Formation Recommendation Report
Template: `assets/templates/formation-report.md`

### Pressing Structure Plan
Template: `assets/templates/pressing-plan.md`

### Set-Piece Strategy Sheet
Template: `assets/templates/set-piece-strategy.md`

### Match Analytics Report
Template: `assets/templates/analytics-report.md`

### Training Session Plan
Template: `assets/templates/training-session.md`

## Error Handling

When LLM calls fail or unexpected errors occur:

1. **Graceful Degradation:** Return partial results with clear disclaimers
2. **Fallback Reasoning:** Apply base frameworks without real-time data
3. **Error Reporting:** Log the error, inform the user, and suggest alternatives
4. **Validation:** Always validate outputs against schemas before returning

## Context Management

To optimize token usage:

1. **Lazy Loading:** Only load reference files when explicitly needed
2. **Progressive Disclosure:** Start with metadata, load body on demand
3. **Caching:** Cache frequently used frameworks in memory
4. **Summarization:** Summarize research papers into operational principles

## Logging

All operations must log with appropriate levels:

- **INFO:** Normal operations, routing decisions
- **WARN:** Validation failures, fallback modes activated
- **ERROR:** LLM call failures, data integrity issues
- **DEBUG:** Detailed execution flow (development only)

## Knowledge Base Consultation

Before making recommendations, always consult:

1. **`SECOND-BRAIN-KNOWLEDGE-PAPER.md`** — Research foundations
2. **Domain reference files** — Operational principles
3. **Validation schemas** — Input/output contracts

## When to Consult Sub-Agents

Use sub-agents for specialized analysis rather than handling everything in the main flow:

- **Complex calculations:** xG, possession value, training load
- **Domain-specific optimization:** Formation matchups, pressing triggers
- **Multi-step scenarios:** Set-piece routines, opponent scouting
- **Large data processing:** Match event analysis, pattern recognition

## Quality Standards

All outputs must meet these criteria:

1. **Evidence-Based:** Cite the methodology/framework being applied
2. **Actionable:** Provide concrete steps, not abstract concepts
3. **Context-Aware:** Consider squad level, opponent, match context
4. **Guardrailed:** Include appropriate disclaimers where certainty is limited
5. **Structured:** Follow the defined templates exactly

## Execution Flow

When this skill is triggered:

1. **Parse Intent:** Identify the primary domain(s) from the request
2. **Route:** Direct to appropriate sub-agent(s)
3. **Validate:** Check inputs against schemas
4. **Consult:** Load relevant reference files and frameworks
5. **Execute:** Apply methodologies to generate recommendations
6. **Validate Output:** Ensure outputs match schema requirements
7. **Format:** Apply the appropriate output template
8. **Return:** Present structured, actionable recommendations

## Extension Points

This skill can be extended by:

1. **Adding Sub-Agents:** New specialized domains (e.g., goalkeeper coaching, sports psychology)
2. **New Frameworks:** Additional research methodologies
3. **Custom Templates:** Domain-specific output formats
4. **Enhanced Schemas:** More granular validation rules

## References

- **Research Base:** `SECOND-BRAIN-KNOWLEDGE-PAPER.md`
- **Project Specification:** `PROJECT-detail.md`
- **Development Tracking:** `PROJECT-DEVELOPMENT-PHASE-TRACKING.md`
- **Operating Instructions:** `CLAUDE.md`

