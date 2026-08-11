#!/usr/bin/env python3
"""
Pressing Specialist Tool Execution Handler

This handler executes pressing structure design requests by coordinating
with the skill's pressing reference materials and providing comprehensive
pressing and defensive organization recommendations.
"""

import sys
import os
from typing import Dict, Any, List
from enum import Enum


class PressingStyle(Enum):
    """Pressing intensity styles"""
    HIGH_PRESS = "high-press"
    MID_BLOCK = "mid-block"
    LOW_BLOCK = "low-block"
    MIXED = "mixed"


class DefensiveBlock(Enum):
    """Defensive block heights"""
    HIGH = "high"
    MID = "mid"
    LOW = "low"


def execute_pressing_design(request: Dict[str, Any]) -> Dict[str, Any]:
    """Execute pressing structure design request"""

    try:
        # Validate input
        required_fields = ["formation", "pressing_style"]
        for field in required_fields:
            if field not in request:
                raise ValueError(f"Missing required field: '{field}'")

        formation = request["formation"]
        pressing_style_str = request["pressing_style"]
        pressing_style = PressingStyle(pressing_style_str)

        # Get optional parameters
        opponent_buildup = request.get("opponent_buildup", "mix")
        game_state = request.get("game_state", {})

        # Generate pressing plan
        pressing_plan = generate_pressing_plan(
            formation,
            pressing_style,
            opponent_buildup,
            game_state
        )

        # Generate defensive organization
        defensive_org = generate_defensive_organization(
            formation,
            pressing_style,
            game_state
        )

        return {
            "pressing_plan": pressing_plan,
            "defensive_organization": defensive_org
        }

    except Exception as e:
        return {
            "error": str(e),
            "error_type": type(e).__name__,
            "fallback": get_fallback_pressing(request)
        }


def generate_pressing_plan(
    formation: str,
    pressing_style: PressingStyle,
    opponent_buildup: str,
    game_state: Dict[str, Any]
) -> Dict[str, Any]:
    """Generate pressing plan"""

    plan = {
        "style": pressing_style.value,
        "zones": [],
        "triggers": [],
        "coordination": "",
        "counter_pressing": {}
    }

    # Define zones based on pressing style
    if pressing_style == PressingStyle.HIGH_PRESS:
        plan["zones"] = [
            {
                "name": "Zone 1: High Press",
                "area": "Opponent's final third",
                "objective": "Win ball back immediately after losing it"
            },
            {
                "name": "Zone 2: Mid-Block",
                "area": "Middle third",
                "objective": "Compress space, force opponent wide"
            }
        ]

        plan["triggers"] = [
            {"trigger": "Backward Pass", "action": "All players step up 3-5m"},
            {"trigger": "Poor Touch", "action": "Nearest player sprints to press (0-2s)"},
            {"trigger": "Touchline Trap", "action": "Nearest player presses to sideline"},
            {"trigger": "Aerial Duel", "action": "Nearest player presses first touch"}
        ]

        plan["coordination"] = "High press with counter-pressing emphasis. Immediate reaction to losing possession in opponent's half."

    elif pressing_style == PressingStyle.MID_BLOCK:
        plan["zones"] = [
            {
                "name": "Zone 1: Mid-Block",
                "area": "Middle third",
                "objective": "Compress space, force opponent wide"
            },
            {
                "name": "Zone 2: Low Block",
                "area": "Defensive third",
                "objective": "Protect penalty area, force crosses"
            }
        ]

        plan["triggers"] = [
            {"trigger": "Backward Pass to Fullback", "action": "Midfielders shift to press"},
            {"trigger": "Slow Build-Up", "action": "Midfielders engage, delay then shift"},
            {"trigger": "Switch of Play", "action": "Delay then shift as a unit"}
        ]

        plan["coordination"] = "Mid-block with compact lateral shifting. Press on triggers, maintain defensive balance."

    else:  # LOW_BLOCK
        plan["zones"] = [
            {
                "name": "Zone 1: Low Block",
                "area": "Defensive third",
                "objective": "Protect penalty area, force crosses"
            }
        ]

        plan["triggers"] = [
            {"trigger": "Final Third Entry", "action": "Delay and funnel to outside"},
            {"trigger": "Switch to Wide", "action": "Delay and funnel to wide areas"},
            {"trigger": "Cross Imminent", "action": "Position for header/clearance"}
        ]

        plan["coordination"] = "Low block protecting penalty area. Force crosses, win second balls."

    # Add counter-pressing
    plan["counter_pressing"] = {
        "trigger": "When possession is lost in opponent's half",
        "coordination": {
            "0-2s": "Nearest player: Immediate sprint to press",
            "2-4s": "Supporting players: Cut passing lanes",
            "4-6s": "Distant players: Recover defensive shape",
            "max_duration": "5 seconds maximum commitment"
        }
    }

    # Adjust for game state
    if game_state:
        score = game_state.get("score", "0-0")
        time = game_state.get("time", 0)

        # Adjust pressing intensity based on score and time
        if "-" in score:
            parts = score.split("-")
            if len(parts) == 2:
                try:
                    home_goals = int(parts[0])
                    away_goals = int(parts[1])
                    goal_diff = home_goals - away_goals

                    if goal_diff > 0 and time > 60:
                        plan["coordination"] += " Leading late - drop intensity slightly."
                    elif goal_diff < 0 and time > 60:
                        plan["coordination"] += " Trailing late - increase intensity."
                except ValueError:
                    pass

    return plan


def generate_defensive_organization(
    formation: str,
    pressing_style: PressingStyle,
    game_state: Dict[str, Any]
) -> Dict[str, Any]:
    """Generate defensive organization"""

    org = {
        "block_shape": "",
        "compactness": "",
        "positioning": {},
        "transition_plan": ""
    }

    # Determine block shape based on formation and pressing style
    if pressing_style == PressingStyle.HIGH_PRESS:
        org["block_shape"] = "High block (45-60m from goal)"
        org["compactness"] = "8-12m between lines"

        # Positioning for high press
        org["positioning"] = {
            "front_three": "Press opponent's back four",
            "midfield": "Shadow opponent's midfield, screen #6",
            "back_four": "Step up to compress mid-block"
        }

        org["transition_plan"] = "If opponent bypasses first press, drop to mid-block shape. Counter-press for 5 seconds maximum."

    elif pressing_style == PressingStyle.MID_BLOCK:
        org["block_shape"] = "Mid-block (35-45m from goal)"
        org["compactness"] = "8-12m between lines"

        org["positioning"] = {
            "front_three": "Drop into mid-block",
            "midfield": "Protect central areas, force wide",
            "back_four": "Edge of penalty area"
        }

        org["transition_plan"] = "Maintain compact shape. If opponent progresses, drop to low block."

    else:  # LOW_BLOCK
        org["block_shape"] = "Low block (25-35m from goal)"
        org["compactness"] = "Protect box, compact width"

        org["positioning"] = {
            "front_three": "Block passes into fullbacks",
            "midfield": "Block passing lanes into #10",
            "back_four": "On edge of penalty area"
        }

        org["transition_plan"] = "Protect penalty area at all costs. Force crosses, win second balls."

    return org


def get_fallback_pressing(request: Dict[str, Any]) -> Dict[str, Any]:
    """Provide fallback pressing recommendation"""

    formation = request.get("formation", "4-4-2")
    pressing_style = request.get("pressing_style", "mid-block")

    return {
        "pressing_plan": {
            "style": pressing_style,
            "zones": [
                {
                    "name": "Standard Mid-Block",
                    "area": "Middle third",
                    "objective": "Protect central areas"
                }
            ],
            "triggers": [
                {"trigger": "General", "action": "Press on triggers, maintain shape"}
            ],
            "coordination": "Standard mid-block organization",
            "note": "Fallback pressing plan due to error"
        },
        "defensive_organization": {
            "block_shape": "Mid-block",
            "compactness": "8-12m between lines",
            "positioning": {
                "note": "Standard positioning based on formation"
            },
            "transition_plan": "Recover defensive shape when possession is lost"
        }
    }


if __name__ == "__main__":
    # Example execution
    example_request = {
        "formation": "4-3-3",
        "pressing_style": "high-press",
        "opponent_buildup": "short-passing",
        "game_state": {
            "score": "0-0",
            "time": 30,
            "target": "win"
        }
    }

    result = execute_pressing_design(example_request)

    if "error" in result:
        print(f"Error: {result['error']}")
        print(f"Fallback: {result['fallback']}")
    else:
        print("Pressing Design Result:")
        print(f"Pressing Plan: {result['pressing_plan']['style']}")
        print(f"Zones: {len(result['pressing_plan']['zones'])}")
        print(f"Triggers: {len(result['pressing_plan']['triggers'])}")
