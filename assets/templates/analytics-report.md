# Match Analytics Report

**Generated:** {{timestamp}}
**Match:** {{home_team}} vs {{away_team}}
**Date:** {{match_date}}

---

## Executive Summary

{{summary}}

---

## Final Score

**{{home_goals}} - {{away_goals}}** (xG: {{home_xg}} - {{away_xg}})

**xG Difference:** {{xg_difference}}

**Performance:** {{performance_assessment}}

---

## xG Analysis

### Total xG

| Team | xG For | Goals | xG Against | Conversion |
|------|--------|-------|------------|------------|
| {{home_team}} | {{home_xg}} | {{home_goals}} | {{home_xg_against}} | {{home_conversion}}% |
| {{away_team}} | {{away_xg}} | {{away_goals}} | {{away_xg_against}} | {{away_conversion}}% |

### xG Timeline

| Period | Home xG | Away xG | Net xG |
|--------|---------|---------|--------|
{{xg_timeline}}

---

## Shot Analysis

### Shot Summary

| Team | Total Shots | On Target | xG/Shot |
|------|-------------|-----------|---------|
| {{home_team}} | {{home_shots}} | {{home_on_target}} | {{home_xg_per_shot}} |
| {{away_team}} | {{away_shots}} | {{away_on_target}} | {{away_xg_per_shot}} |

### Shot Quality Distribution

**{{home_team}}:**

{{home_shot_distribution}}

**{{away_team}}:**

{{away_shot_distribution}}

---

## Player Performance

### Top Performers (xG)

| Player | xG | Goals | xG - G |
|--------|-----|-------|--------|
{{top_performers}}

### Passing Performance

| Player | Passes | Acc % | Key Passes | xA |
|--------|--------|-------|------------|-----|
{{passing_performers}}

---

## Possession Analysis

### Possession Statistics

| Team | Possession % | Passes | Pass Acc % | Progressive Passes |
|------|--------------|--------|-------------|-------------------|
| {{home_team}} | {{home_possession}} | {{home_passes}} | {{home_pass_acc}} | {{home_progressive}} |
| {{away_team}} | {{away_possession}} | {{away_passes}} | {{away_pass_acc}} | {{away_progressive}} |

### Possession Value Chains

**High Value Chains (+0.30+):**

{{#each high_value_chains}}
- **{{this.players}}:** +{{this.value}} ({{this.description}})
{{/each}}

**Negative Chains (-0.10-):**

{{#each negative_chains}}
- **{{this.players}}:** {{this.value}} ({{this.description}})
{{/each}}

---

## Set-Piece Analysis

### Set-Piece xG

| Team | Corners | Free Kicks | xG | Goals |
|------|---------|------------|-----|-------|
| {{home_team}} | {{home_corners}} | {{home_fk}} | {{home_sp_xg}} | {{home_sp_goals}} |
| {{away_team}} | {{away_corners}} | {{away_fk}} | {{away_sp_xg}} | {{away_sp_goals}} |

### Set-Piece Efficiency

**{{home_team}}:** {{home_sp_efficiency}}

**{{away_team}}:** {{away_sp_efficiency}}

---

## Pressing Analysis

### PPDA (Passes Per Defensive Action)

| Team | PPDA | Press Intensity | High Turnovers |
|------|------|-----------------|----------------|
| {{home_team}} | {{home_ppda}} | {{home_press_intensity}} | {{home_high_turnovers}} |
| {{away_team}} | {{away_ppda}} | {{away_press_intensity}} | {{away_high_turnovers}} |

### Counter-Press Recovery

**{{home_team}}:** {{home_counter_press}}% recovery rate

**{{away_team}}:** {{away_counter_press}}% recovery rate

---

## Key Moments

### Goals

{{#each goals}}
- **{{this.minute}}':** {{this.team}} - {{this.player}} ({{this.type}})
  - xG: {{this.xg}}
  - Build-up: {{this.buildup}}
{{/each}}

### High xG Chances

{{#each high_xg_chances}}
- **{{this.minute}}':** {{this.team}} - {{this.player}}
  - xG: {{this.xg}}
  - Outcome: {{this.outcome}}
{{/each}}

### Turning Points

{{#each turning_points}}
- **{{this.minute}}':** {{this.description}}
  - Impact: {{this.impact}}
{{/each}}

---

## Tactical Observations

### {{home_team}} Tactics

**Formation:** {{home_formation}}

**Strengths:**

{{#each home_strengths}}
- {{this}}
{{/each}}

**Weaknesses:**

{{#each home_weaknesses}}
- {{this}}
{{/each}}

### {{away_team}} Tactics

**Formation:** {{away_formation}}

**Strengths:**

{{#each away_strengths}}
- {{this}}
{{/each}}

**Weaknesses:**

{{#each away_weaknesses}}
- {{this}}
{{/each}}

---

## Recommendations

### For {{home_team}}

{{#each home_recommendations}}
- {{this}}
{{/each}}

### For {{away_team}}

{{#each away_recommendations}}
- {{this}}
{{/each}}

---

## Methodology

This analysis is based on:

- **Expected Goals (xG):** Probability-based chance quality assessment
- **Possession Value Framework:** Action value analysis throughout possession chains
- **Pressing Metrics:** PPDA and counter-press recovery tracking
- **Set-Piece xG:** Quality assessment of set-piece situations

**Data Processing:**
- xG Calculator: `scripts/xg-calculator.py`
- Opponent Analyzer: `scripts/opponent-analyzer.py`

**References:**
- xG Framework: `references/analytics/xg-framework.md`
- Analytics Research: `SECOND-BRAIN-KNOWLEDGE-PAPER.md`

---

**Disclaimer:** Analytics provide insights but don't capture all aspects of football performance. Context matters: game state, fatigue, substitutions, and tactical adaptations all influence outcomes. Use analytics to inform decisions, not make them automatically.

