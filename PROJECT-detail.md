# PROJECT-detail.md — Football (Soccer) Strategy Advisor

## 1. Problem Statement

A skill supporting coaches, analysts, and enthusiasts with tactical analysis: formation design, pressing structures, set-piece strategy, and data-driven performance evaluation, grounded in established football tactical theory and sports analytics research.

## 2. Target Users

Describe the primary user personas for this skill (fill in based on real usage once built): e.g., students, professionals, hobbyists, or practitioners in the relevant domain.

## 3. Functional Specification

### 3.1 Core Capabilities

- Analyze and recommend formations/systems (4-3-3, 3-5-2, etc.) for a given squad profile
- Design pressing and defensive-block strategies (high press, mid-block, low block)
- Evaluate set-piece strategy (corners, free kicks) using positional-play principles
- Apply expected goals (xG) and possession-value metrics to evaluate performance
- Analyze opponent tendencies and suggest exploitable weaknesses
- Design training-session periodization aligned with tactical objectives

### 3.2 Key Methodologies & Frameworks Applied

- **Positional Play / Juego de Posición principles**
- **Expected Goals (xG) and possession-value analytics**
- **Pressing-trigger and defensive-block theory (Guardiola/Klopp schools, cited conceptually)**
- **Periodization theory (Bondarchuk / Matveyev) for training design**
- **Game-model and playing-identity frameworks used in elite academies**

Each framework above should be operationalized as a concrete step, checklist, or template inside the skill's SKILL.md and reference files once this scaffold is turned into a runnable skill (see `DEVELOPMENT-TASK-BY-PHASES.md`).

### 3.3 Expected Input

Typical user requests this skill should handle (fill in with real example prompts during development and testing).

### 3.4 Expected Output Format

Define the structured output format(s) this skill should produce (e.g., structured report, checklist, scored recommendation, memo). Align with the methodologies above so outputs are consistent and auditable.

## 4. Out of Scope / Guardrails

General guardrails apply — remain factual, avoid unsupported certainty, and encourage professional consultation where the topic genuinely warrants it.

## 5. Knowledge Base Dependency

This skill's reasoning quality depends on the research foundations catalogued in `SECOND-BRAIN-KNOWLEDGE-PAPER.md`. When building the actual skill (SKILL.md + references/), extract the operational principles from each paper into concrete reference files rather than leaving them as a flat reading list.

## 6. Success Criteria

- Output correctly applies the named methodologies rather than generic reasoning.
- Output is well-structured and consistent across repeated runs on similar inputs.
- Domain-appropriate guardrails/disclaimers are respected in every response.
- Test prompts (see `DEVELOPMENT-TASK-BY-PHASES.md`, Phase 5) produce outputs a subject-matter-competent reviewer would rate as sound.
