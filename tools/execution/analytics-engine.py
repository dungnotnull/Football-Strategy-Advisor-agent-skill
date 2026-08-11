#!/usr/bin/env python3
"""
Analytics Engine Tool Execution Handler

This handler executes analytics queries including xG calculations,
match analysis, and opponent scouting using the skill's analytics
framework and calculation scripts.
"""

import sys
import os
from typing import Dict, Any, List
from enum import Enum

# Add scripts directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../scripts'))

from xg_calculator import (
    xGCalculator,
    Shot,
    Location,
    ShotType,
    AssistType,
    Outcome,
    load_shots_from_dict
)

from opponent_analyzer import (
    OpponentAnalyzer,
    MatchData,
    PlayingStyle,
    PressingIntensity,
    DefensiveBlock,
    load_matches_from_dict
)


class QueryType(Enum):
    """Types of analytics queries"""
    XG_ANALYSIS = "xg-analysis"
    OPPONENT_ANALYSIS = "opponent-analysis"
    PERFORMANCE_ANALYSIS = "performance-analysis"
    POSSESSION_VALUE = "possession-value"


def execute_analytics_query(request: Dict[str, Any]) -> Dict[str, Any]:
    """Execute analytics query"""

    try:
        # Validate input
        if "query_type" not in request:
            raise ValueError("Missing required field: 'query_type'")

        query_type = QueryType(request["query_type"])

        # Route to appropriate handler
        if query_type == QueryType.XG_ANALYSIS:
            return execute_xg_analysis(request)
        elif query_type == QueryType.OPPONENT_ANALYSIS:
            return execute_opponent_analysis(request)
        elif query_type == QueryType.PERFORMANCE_ANALYSIS:
            return execute_performance_analysis(request)
        elif query_type == QueryType.POSSESSION_VALUE:
            return execute_possession_value_analysis(request)
        else:
            raise ValueError(f"Unknown query type: {query_type}")

    except Exception as e:
        return {
            "error": str(e),
            "error_type": type(e).__name__,
            "fallback": get_fallback_analytics(request)
        }


def execute_xg_analysis(request: Dict[str, Any]) -> Dict[str, Any]:
    """Execute xG analysis"""

    calculator = xGCalculator()

    # Check if single shot or match analysis
    if "shot_data" in request:
        # Single shot analysis
        shot_data = request["shot_data"]

        location = Location(
            x=shot_data["location"]["x"],
            y=shot_data["location"]["y"]
        )

        shot = Shot(
            team=shot_data.get("team", "home"),
            player=shot_data.get("player", "Unknown"),
            minute=shot_data.get("minute", 0),
            location=location,
            shot_type=ShotType(shot_data.get("shot_type", "right-foot")),
            assist_type=AssistType(shot_data.get("assist_type", "pass")),
            defenders=shot_data.get("defenders", 0),
            outcome=Outcome(shot_data["outcome"]),
            game_state=tuple(shot_data["game_state"]) if shot_data.get("game_state") else None
        )

        calculation = calculator.calculate_shot_xg(shot)

        return {
            "xg_value": calculation.final_xg,
            "breakdown": calculation.breakdown,
            "shot_analysis": {
                "zone": calculation.breakdown["zone"],
                "base_xg": calculation.base_xg,
                "modifiers": calculation.modifiers,
                "outcome": shot.outcome.value
            }
        }

    elif "match_shots" in request:
        # Match analysis
        shots_data = request["match_shots"]
        shots = load_shots_from_dict(shots_data)

        match_analysis = calculator.calculate_match_xg(shots)

        return {
            "match_analysis": {
                "home_xg": match_analysis.home_xg,
                "away_xg": match_analysis.away_xg,
                "home_goals": match_analysis.home_goals,
                "away_goals": match_analysis.away_goals,
                "home_shots": match_analysis.home_shots,
                "away_shots": match_analysis.away_shots,
                "xg_timeline": match_analysis.xg_timeline,
                "player_xg": match_analysis.player_xg,
                "performance_summary": match_analysis.performance_summary
            }
        }
    else:
        raise ValueError("Must provide either 'shot_data' or 'match_shots'")


def execute_opponent_analysis(request: Dict[str, Any]) -> Dict[str, Any]:
    """Execute opponent analysis"""

    # Validate input
    if "team_name" not in request:
        raise ValueError("Missing required field: 'team_name'")
    if "matches" not in request:
        raise ValueError("Missing required field: 'matches'")

    team_name = request["team_name"]
    matches_data = request["matches"]

    # Load match data
    matches = []
    for match_data in matches_data:
        match = MatchData(
            opponent=match_data.get("opponent", "Unknown"),
            formation=match_data.get("formation", "4-4-2"),
            playing_style=PlayingStyle(match_data.get("playing_style", "balanced")),
            pressing_intensity=PressingIntensity(match_data.get("pressing_intensity", "medium")),
            defensive_block=DefensiveBlock(match_data.get("defensive_block", "mid")),
            xg_for=match_data.get("xg_for", 1.0),
            xg_against=match_data.get("xg_against", 1.0),
            goals_for=match_data.get("goals_for", 1),
            goals_against=match_data.get("goals_against", 1),
            shots_for=match_data.get("shots_for", 10),
            shots_against=match_data.get("shots_against", 10),
            ppda=match_data.get("ppda", 13.0),
            high_turnovers=match_data.get("high_turnovers", 3),
            set_piece_xg_for=match_data.get("set_piece_xg_for", 0.1),
            set_piece_xg_against=match_data.get("set_piece_xg_against", 0.1),
            result=match_data.get("result", "D")
        )
        matches.append(match)

    # Analyze opponent
    analyzer = OpponentAnalyzer()
    profile = analyzer.analyze_opponent(matches, team_name)

    return {
        "profile": {
            "team_name": profile.team_name,
            "recent_form": profile.recent_form,
            "averages": {
                "xg_for": profile.avg_xg_for,
                "xg_against": profile.avg_xg_against,
                "ppda": profile.avg_ppda,
                "high_turnovers": profile.avg_high_turnovers,
                "conversion_rate": profile.conversion_rate
            },
            "tactical_tendencies": profile.tactical_tendencies,
            "strengths": profile.strengths,
            "weaknesses": profile.weaknesses,
            "exploitation_opportunities": profile.exploitation_opportunities,
            "recommended_approach": profile.recommended_approach
        }
    }


def execute_performance_analysis(request: Dict[str, Any]) -> Dict[str, Any]:
    """Execute performance analysis"""

    # This would analyze player or team performance over time
    # For now, provide a structured response

    entity = request.get("entity", "team")
    metrics = request.get("metrics", ["xg", "shots"])
    timeframe = request.get("timeframe", "last-5")

    return {
        "performance": {
            "entity": entity,
            "timeframe": timeframe,
            "metrics": {
                metric: {
                    "value": "N/A (requires match data)",
                    "trend": "N/A"
                }
                for metric in metrics
            },
            "summary": "Performance analysis requires match data input"
        }
    }


def execute_possession_value_analysis(request: Dict[str, Any]) -> Dict[str, Any]:
    """Execute possession value analysis"""

    # This would analyze possession chains using VAEP framework
    # For now, provide a structured response

    if "match_data" not in request or "possessions" not in request["match_data"]:
        return {
            "possession_value": {
                "note": "Possession data required for VAEP analysis",
                "framework": "VAEP (Valuing Actions by Estimating Probabilities)",
                "description": "Analyzes value of each action in possession chain"
            }
        }

    possessions = request["match_data"]["possessions"]

    # Calculate possession values (simplified)
    total_value = 0.0
    high_value_chains = []
    negative_chains = []

    for possession in possessions:
        chain_value = 0.0
        for action in possession.get("actions", []):
            action_type = action.get("action_type", "pass")
            successful = action.get("successful", True)

            # Simplified VAEP scoring
            if action_type == "pass":
                if successful:
                    chain_value += 0.02
                else:
                    chain_value -= 0.05
            elif action_type == "shot":
                chain_value += 0.10
            elif action_type == "turnover":
                chain_value -= 0.10

        total_value += chain_value

        if chain_value > 0.30:
            high_value_chains.append({
                "value": chain_value,
                "duration": possession.get("end_time", 0) - possession.get("start_time", 0)
            })
        elif chain_value < -0.10:
            negative_chains.append({
                "value": chain_value,
                "duration": possession.get("end_time", 0) - possession.get("start_time", 0)
            })

    return {
        "possession_value": {
            "total_value": round(total_value, 2),
            "average_value": round(total_value / max(len(possessions), 1), 2),
            "high_value_chains": len(high_value_chains),
            "negative_chains": len(negative_chains),
            "note": "Full VAEP analysis requires complete event data"
        }
    }


def get_fallback_analytics(request: Dict[str, Any]) -> Dict[str, Any]:
    """Provide fallback analytics recommendation"""

    query_type = request.get("query_type", "xg-analysis")

    fallback_responses = {
        "xg-analysis": {
            "xg_value": "N/A",
            "note": "xG analysis requires shot location and outcome data",
            "required_fields": ["location (x, y)", "shot_type", "outcome"]
        },
        "opponent-analysis": {
            "profile": "N/A",
            "note": "Opponent analysis requires recent match data",
            "required_fields": ["team_name", "matches (xG, PPDA, turnovers, results)"]
        },
        "performance-analysis": {
            "performance": "N/A",
            "note": "Performance analysis requires match history data",
            "required_fields": ["entity", "timeframe", "metrics"]
        },
        "possession-value": {
            "possession_value": "N/A",
            "note": "Possession value analysis requires event data",
            "required_fields": ["possessions (actions with types and outcomes)"]
        }
    }

    return fallback_responses.get(query_type, {
        "error": "Unknown query type",
        "available_types": ["xg-analysis", "opponent-analysis", "performance-analysis", "possession-value"]
    })


if __name__ == "__main__":
    # Example execution
    example_request = {
        "query_type": "xg-analysis",
        "shot_data": {
            "team": "home",
            "player": "Mohamed Salah",
            "minute": 15,
            "location": {"x": 8, "y": 3},
            "shot_type": "right-foot",
            "assist_type": "through-ball",
            "defenders": 1,
            "outcome": "goal",
            "game_state": [0, 0]
        }
    }

    result = execute_analytics_query(example_request)

    if "error" in result:
        print(f"Error: {result['error']}")
        print(f"Fallback: {result['fallback']}")
    else:
        print("Analytics Result:")
        if "xg_value" in result:
            print(f"xG Value: {result['xg_value']}")
        elif "match_analysis" in result:
            print(f"Home xG: {result['match_analysis']['home_xg']}")
            print(f"Away xG: {result['match_analysis']['away_xg']}")
        elif "profile" in result:
            print(f"Opponent: {result['profile']['team_name']}")
            print(f"Avg xG For: {result['profile']['averages']['xg_for']}")
