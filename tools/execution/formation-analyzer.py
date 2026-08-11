#!/usr/bin/env python3
"""
Formation Analyzer Tool Execution Handler

This handler executes formation analysis requests by coordinating
the formation calculator script with the skill's reference materials.
"""

import sys
import os
from typing import Dict, Any, List

# Add scripts directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../scripts'))

from formation_calculator import (
    FormationCalculator,
    Player,
    Position,
    Formation,
    PlayingStyle,
    load_players_from_dict
)


def execute_formation_analysis(request: Dict[str, Any]) -> Dict[str, Any]:
    """Execute formation analysis request"""

    try:
        # Validate input
        if "players" not in request:
            raise ValueError("Missing required field: 'players'")

        if "playing_style" not in request:
            raise ValueError("Missing required field: 'playing_style'")

        # Load players from request
        players_data = request["players"]
        players = load_players_from_dict(players_data)

        # Get playing style
        playing_style = PlayingStyle(request.get("playing_style", "balanced"))

        # Get preferred formation if specified
        preferred_formation = None
        if "preferred_formation" in request:
            preferred_formation = Formation(request["preferred_formation"])

        # Initialize calculator
        calculator = FormationCalculator()

        # Calculate best formations
        formation_scores = calculator.calculate_best_formation(
            players=players,
            playing_style=playing_style,
            preferred_formation=preferred_formation
        )

        # Format results
        result = {
            "formations": [],
            "recommendation": None
        }

        for score in formation_scores[:5]:  # Top 5 formations
            formation_data = {
                "formation": score.formation.value,
                "score": score.score,
                "positioning": score.positioning,
                "reasoning": score.reasoning,
                "strengths": score.strengths,
                "weaknesses": score.weaknesses
            }
            result["formations"].append(formation_data)

        # Set top recommendation
        if formation_scores:
            top_score = formation_scores[0]
            result["recommendation"] = {
                "formation": top_score.formation.value,
                "reasoning": ". ".join(top_score.reasoning),
                "tactical_notes": top_score.strengths + ["Note: " + w for w in top_score.weaknesses]
            }

        # Add opponent analysis if provided
        if "opponent_style" in request:
            opponent = request["opponent_style"]
            result["opponent_analysis"] = analyze_opponent_matchup(
                formation_scores[0],
                opponent
            )

        return result

    except Exception as e:
        # Graceful error handling
        return {
            "error": str(e),
            "error_type": type(e).__name__,
            "fallback": get_fallback_formation(request)
        }


def analyze_opponent_matchup(top_formation, opponent_style: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze matchup against opponent"""

    analysis = {
        "advantages": [],
        "disadvantages": [],
        "adjustments": []
    }

    formation = top_formation.formation.value
    opponent_formation = opponent_style.get("formation", "unknown")
    opponent_style_play = opponent_style.get("playing_style", "balanced")

    # Analyze based on opponent style
    if opponent_style_play == "possession":
        analysis["adjustments"].append("Press high to disrupt build-up")
        analysis["advantages"].append("Counter-attack opportunities")
    elif opponent_style_play == "counter-attack":
        analysis["adjustments"].append("Maintain defensive balance")
        analysis["disadvantages"].append("Vulnerable to transitions")
    elif opponent_style_play == "direct":
        analysis["adjustments"].append("Win aerial duels")
        analysis["advantages"].append("Control possession")

    return analysis


def get_fallback_formation(request: Dict[str, Any]) -> Dict[str, Any]:
    """Provide fallback formation recommendation"""

    playing_style = request.get("playing_style", "balanced")

    style_formation_map = {
        "possession": "4-3-3",
        "counter-attack": "4-4-2",
        "direct": "4-4-2",
        "balanced": "4-2-3-1"
    }

    fallback_formation = style_formation_map.get(playing_style, "4-4-2")

    return {
        "formation": fallback_formation,
        "reasoning": "Fallback formation based on playing style preference",
        "note": "Error occurred during detailed analysis. Using simplified recommendation."
    }


def validate_output(output: Dict[str, Any]) -> bool:
    """Validate output against schema"""

    required_fields = ["formations", "recommendation"]

    for field in required_fields:
        if field not in output:
            return False

    return True


if __name__ == "__main__":
    # Example execution
    example_request = {
        "players": [
            {
                "name": "Player 1",
                "position": "GK",
                "rating": 85
            },
            {
                "name": "Player 2",
                "position": "RB",
                "rating": 82,
                "attributes": {"pace": 80, "passing": 75}
            }
        ],
        "playing_style": "balanced"
    }

    result = execute_formation_analysis(example_request)

    if "error" in result:
        print(f"Error: {result['error']}")
        print(f"Fallback: {result['fallback']}")
    else:
        print("Formation Analysis Result:")
        print(f"Recommendation: {result['recommendation']['formation']}")
        print(f"Reasoning: {result['recommendation']['reasoning']}")
