# Expected Goals (xG) & Possession Value Analytics — Framework Reference

## Core Concepts

Expected Goals (xG) measures the quality of a chance based on historical data of similar shots. Possession value frameworks extend this to value player actions throughout the possession chain.

### Expected Goals (xG)

**Definition:** The probability that a shot will result in a goal, based on historical data of similar shots.

**Key Factors:**
- Shot location (distance and angle from goal)
- Shot type (header, foot, volley, etc.)
- Assist type (through-ball, cross, pass, dribble)
- Defensive pressure (number of defenders between shooter and goal)
- Game state (score, time, home/away)

## xG Models

### Basic xG Model (Location-Based)

**Factors:**
1. **Distance from Goal:** Closer = higher xG
2. **Angle to Goal:** More central = higher xG
3. **Shot Type:** Header vs footed shot

**Approximate xG Values by Zone:**

| Zone | Distance | xG Range | Example |
|------|----------|----------|---------|
| **Zone 1 (Six-yard box)** | 0-6m | 0.30-0.50 | Tap-ins, rebounds |
| **Zone 2 (Penalty spot)** | 6-12m | 0.15-0.30 | First-time shots, headers |
| **Zone 3 (Edge of box)** | 12-20m | 0.05-0.15 | Driven shots, placed shots |
| **Zone 4 (Outside box)** | 20m+ | 0.01-0.05 | Long shots, speculative efforts |

**Calculation Formula (Simplified):**
```
xG = (Distance Factor) × (Angle Factor) × (Shot Type Factor) × (Pressure Factor)
```

### Advanced xG Model (Multi-Factor)

**Additional Factors:**
1. **Assist Type:**
   - Through-ball: +0.05 xG (better than average chance)
   - Cross: +0.02 xG (slightly above average)
   - Pass: baseline (no adjustment)
   - Dribble: +0.03 xG (beats defender)

2. **Defensive Pressure:**
   - No pressure: +0.03 xG (unopposed)
   - Light pressure (1 defender): baseline
   - Heavy pressure (2+ defenders): -0.05 xG (crowded)

3. **Game State:**
   - Leading by 1+: -0.02 xG (caution)
   - Trailing by 1+: +0.02 xG (desperation)
   - Drawn: baseline

**Full Formula:**
```
xG = Base xG (Location)
    + Assist Type Modifier
    + Pressure Modifier
    + Game State Modifier
```

## xG Performance Analysis

### Team xG Metrics

**xG For (xGF):** Expected goals for your team
- High xGF = creating good chances
- Low xGF = not creating enough quality chances

**xG Against (xGA):** Expected goals for opponents
- High xGA = conceding too many good chances
- Low xGA = solid defensive organization

**xG Difference (xGD):** xGF - xGA
- Positive xGD = outperforming opponents in chance quality
- Negative xGD = underperforming opponents

**xG Conversion Rate:** Goals / xGF
- Above 100% = clinical finishing (overperformance)
- Below 100% = poor finishing (underperformance)
- Sustainable level: 90-110% (regresses to 100% over time)

### Player xG Metrics

**xG per 90:** xG / minutes played × 90
- Elite strikers: 0.60+ xG/90
- Good strikers: 0.45-0.60 xG/90
- Average strikers: 0.30-0.45 xG/90

**xG - Goals:** Difference between expected and actual goals
- Positive (+0.5): Finishing below expectation, due for improvement
- Negative (-0.5): Finishing above expectation, due for regression
- Sustained difference indicates quality finishing or poor finishing

**Shot Location Quality:** Average distance of shots
- Elite: <12m average (high-quality shots)
- Good: 12-16m average
- Average: 16-20m average

## Possession Value Frameworks

### VAEP (Valuing Actions by Estimating Probabilities)

**Concept:** Every action in possession adds or subtracts value based on how it changes the probability of scoring within the next 10 seconds.

**Action Types:**
1. **Pass:** +Value if progressive, -Value if backward/square
2. **Dribble:** +Value if beats defender, -Value if dispossession
3. **Shot:** +Value if high xG, -Value if low xG (missed opportunity)
4. **Defensive Action:** +Value if turnover, -Value if bypassed

**VAEP Scoring (Approximate):**

| Action | VAEP Score | Example |
|--------|------------|---------|
| **Progressive Pass** | +0.02 to +0.05 | Pass into final third |
| **Assist** | +0.10 to +0.30 | Pre-assist + goal |
| **Successful Dribble** | +0.01 to +0.03 | Beating defender |
| **Shot (Goal)** | +0.80 to +1.00 | Scoring |
| **Shot (Saved)** | +0.10 to +0.30 | High xG shot |
| **Shot (Miss)** | -0.05 to -0.15 | Wasted possession |
| **Turnover** | -0.10 to -0.30 | Giving ball away |
| **Tackle** | +0.05 to +0.15 | Winning possession |
| **Interception** | +0.03 to +0.10 | Reading play |

### Possession Value Chain Analysis

**Chain:** Player → Action → Value → Next Action → Value → ...

**Example Possession Chain:**
```
Player A: Progressive pass (+0.03)
Player B: Dribble (+0.02)
Player C: Through-ball pass (+0.05)
Player D: Shot for goal (+0.80)
Total Value: +0.90 (dominant possession)
```

**Chain Value Analysis:**
- **High Value Chains (+0.30+):** Lead to shots or high-quality chances
- **Medium Value Chains (+0.10 to +0.30):** Progress possession into dangerous areas
- **Low Value Chains (-0.10 to +0.10):** Maintaining possession without penetration
- **Negative Chains (-0.10-):** Losing possession or wasting opportunities

## Opposition Analysis Using xG

### Scouting Opponent xG Profile

**Analyze Last 5 Matches:**

1. **xG For Trend:** Are they creating chances?
   - Rising xGF: Dangerous form, creating more chances
   - Stable xGF: Consistent chance creation
   - Falling xGF: Declining form, struggling to create

2. **xG Against Trend:** Are they conceding chances?
   - Rising xGA: Defensive vulnerability
   - Stable xGA: Solid defensive organization
   - Falling xGA: Defensive improvement

3. **Conversion Rate:** Clinical finishing?
   - High conversion (>110%): Due for regression (expect fewer goals)
   - Normal conversion (90-110%): Sustainable performance
   - Low conversion (<90%): Due for improvement (expect more goals)

**Tactical Implications:**

| Opponent xG Profile | Tactical Approach |
|---------------------|-------------------|
| High xGF, High xGA | Open games, chances both ends, attacking approach |
| High xGF, Low xGA | Dominant team, need counter-attack, compact block |
| Low xGF, High xGA | Vulnerable, press high, force mistakes |
| Low xGF, Low xGA | Low-scoring, set-piece battle, patience |

### Exploiting xG Weaknesses

**High xGA (Conceding Good Chances):**
- Target their defensive weaknesses
- Exploit transitions
- Direct play into final third

**Low xGF (Not Creating Chances):**
- Press high to force mistakes
- Deny space in final third
- Low block, force patient build-up

**Poor Conversion (<90%):**
- Don't overreact to conceding early (may regress)
- Keep creating chances, don't change approach

**High Conversion (>110%):**
- Expect regression, don't chase game
- Stay patient, they'll cool off

## Set-Piece xG

### Set-Piece xG Values

| Set-Piece Type | xG Value | Notes |
|----------------|----------|-------|
| **Penalty** | 0.76 | Highest xG action in football |
| **Direct Free Kick** | 0.10 | Specialist dependent |
| **Corner (Near Post)** | 0.05 | Lower xG, crowded box |
| **Corner (Far Post)** | 0.04 | Similar to near post |
| **Corner (Short)** | 0.02 | Lower xG but retains possession |
| **Free Kick (Cross)** | 0.04 | Similar to corner |
| **Deep Free Kick** | 0.03 | Long shot or cross |
| **Throw-in (Final Third)** | 0.02 | Low xG but can create chances |

### Set-Piece Optimization

**Corner Strategy (Maximizing xG):**
1. **Deliver to Near Post:** 40% of corners (5-7m run-up, low trajectory)
2. **Deliver to Far Post:** 35% of corners (attacking run, high trajectory)
3. **Short Corner:** 15% of corners (retain possession, create chance)
4. **Direct Shot:** 10% of corners (near post, volley attempt)

**Free-Kick Strategy (Maximizing xG):**
1. **Shooting Range (<25m):** 60% direct shots (specialist)
2. **Crossing Range (25-35m):** 30% crosses into box
3. **Creative Passing (>35m):** 10% short passes to retain possession

## xG in Match Analysis

### Live Match xG Tracking

**First Half Analysis:**
- Track xG created vs xG conceded
- Identify overperformance/underperformance
- Adjust tactics for second half

**Half-Time xG Decisions:**

| Scenario | Tactical Adjustment |
|----------|-------------------|
| Leading 1-0, xGF 0.3, xGA 0.8 | Fortunate lead, drop to mid-block, protect |
| Trailing 0-1, xGF 1.2, xGA 0.3 | Unlucky to trail, continue creating chances |
| Draw 0-0, xGF 0.1, xGA 0.1 | Low-scoring, set-piece focus, patience |
| Leading 2-0, xGF 1.5, xGA 0.2 | Dominant, conserve energy, maintain shape |

### Post-Match xG Report

**xG Summary:**
- Final Score: [Score] (xGF: [xGF], xGA: [xGA])
- xG Difference: [+/- xGD]
- Performance: [Over/Underperformance]

**Key Moments:**
- [Time]: [Event] ([xG value])

**xG Timeline:**
- 0-15': [xGF] - [xGA] = [Net]
- 15-30': [xGF] - [xGA] = [Net]
- 30-45': [xGF] - [xGA] = [Net]
- 45-60': [xGF] - [xGA] = [Net]
- 60-75': [xGF] - [xGA] = [Net]
- 75-90': [xGF] - [xGA] = [Net]

**Player xG:**
- [Player]: [xG] (Expected Goals)
- [Player]: [xG] (Expected Goals)
- ...

## Training Session Design (xG Focus)

### xG Awareness Session

**Objective:** Help players understand shot quality and decision-making

**Drill 1: xG Zones Game**
- 60x40m pitch with marked xG zones
- 6v6 small-sided game
- Bonus points for shots from high xG zones
- Coaching points: Recognize high xG opportunities, be patient

**Drill 2: Shot Selection**
- 5v5 in final third
- Goals only count from specific xG zones
- Rotate zones every 5 minutes
- Coaching points: Quality over quantity, shoot when good chance

**Drill 3: Chance Creation Chain**
- 8v8 game
- Track possession chains leading to shots
- Reward teams for high-value chains
- Coaching points: Progressive actions, maintain possession, create quality chances

## Limitations and Considerations

### xG Model Limitations

1. **Context Ignored:**
   - Game state not always accounted for
   - Team strength variations
   - Fatigue and substitutions

2. **Sample Size Issues:**
   - Single match xG is noisy
   - Need 5-10 matches for reliable trends
   - Shot type distribution affects accuracy

3. **Defensive Quality:**
   - Doesn't account for goalkeeper quality
   - Defensive positioning not fully captured
   - Set-piece variations not fully modeled

### When Not to Rely on xG

1. **Small Sample Sizes:** <5 matches
2. **Goalkeeper Analysis:** xG doesn't measure shot-stopping
3. **Set-Piece Analysis:** Too many variables
4. **Tactical Execution:** Process vs outcome
5. **Youth Football:** Different patterns, insufficient data

---

**Source Framework:** Research from Spearman et al. (2017), Decroos et al. (2019), and Pappalardo et al. (2019) on xG and possession-value modeling. See *SECOND-BRAIN-KNOWLEDGE-PAPER.md* for full citations.

