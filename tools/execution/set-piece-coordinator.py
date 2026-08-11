#!/usr/bin/env python3
"""
Set-Piece Coordinator Tool Execution Handler

This handler executes set-piece strategy design requests for corners,
free kicks, throw-ins, and penalties, providing comprehensive
attacking and defensive routines.
"""

import sys
import os
from typing import Dict, Any, List
from enum import Enum


class SetPieceType(Enum):
    """Types of set-pieces"""
    CORNER = "corner"
    FREE_KICK = "free-kick"
    THROW_IN = "throw-in"
    PENALTY = "penalty"


def execute_set_piece_design(request: Dict[str, Any]) -> Dict[str, Any]:
    """Execute set-piece strategy design request"""

    try:
        # Validate input
        required_fields = ["set_piece_type", "attacking_or_defending"]
        for field in required_fields:
            if field not in request:
                raise ValueError(f"Missing required field: '{field}'")

        set_piece_type = SetPieceType(request["set_piece_type"])
        attacking_or_defending = request["attacking_or_defending"]

        # Get optional parameters
        field_position = request.get("field_position", {})
        personnel = request.get("personnel", {})
        opponent_weakness = request.get("opponent_weakness", {})
        game_state = request.get("game_state", {})

        # Generate set-piece strategy
        if attacking_or_defending == "attacking":
            strategy = generate_attacking_strategy(
                set_piece_type,
                field_position,
                personnel,
                opponent_weakness,
                game_state
            )
        else:
            strategy = generate_defensive_strategy(
                set_piece_type,
                field_position,
                personnel,
                opponent_weakness,
                game_state
            )

        return {
            "strategy": strategy
        }

    except Exception as e:
        return {
            "error": str(e),
            "error_type": type(e).__name__,
            "fallback": get_fallback_set_piece(request)
        }


def generate_attacking_strategy(
    set_piece_type: SetPieceType,
    field_position: Dict[str, Any],
    personnel: Dict[str, Any],
    opponent_weakness: Dict[str, Any],
    game_state: Dict[str, Any]
) -> Dict[str, Any]:
    """Generate attacking set-piece strategy"""

    strategy = {
        "type": set_piece_type.value,
        "setup": {},
        "delivery_zones": [],
        "movements": [],
        "coaching_points": []
    }

    if set_piece_type == SetPieceType.CORNER:
        strategy["setup"] = {
            "near_post": "Strong header (5-7m from goal line)",
            "middle": "Target man (8-10m from goal line)",
            "far_post": "Secondary header (11-13m from goal line)",
            "edge_of_box": "2 players for second balls"
        }

        strategy["delivery_zones"] = [
            {
                "zone": "Near Post",
                "percentage": 40,
                "trajectory": "Low, driven",
                "target": "Glanced header or volley"
            },
            {
                "zone": "Middle",
                "percentage": 35,
                "trajectory": "Medium, hanging",
                "target": "Power header or knock-down"
            },
            {
                "zone": "Far Post",
                "percentage": 20,
                "trajectory": "High, deep",
                "target": "Header back across goal"
            },
            {
                "zone": "Short",
                "percentage": 5,
                "trajectory": "Pass to edge",
                "target": "Retain possession"
            }
        ]

        strategy["movements"] = [
            {"player": "Near Post Attacker", "movement": "Wait, then sprint when ball is kicked"},
            {"player": "Middle Attacker", "movement": "Start wider, curve run to penalty spot"},
            {"player": "Far Post Attacker", "movement": "Start at near post, backpedal then sprint"},
            {"player": "Edge Players", "movement": "Hold position, attack loose balls"}
        ]

        strategy["coaching_points"] = [
            "Synchronize runs with delivery",
            "Attack ball at highest point",
            "Second balls are crucial",
            "Be ready for quick combinations if short corner"
        ]

    elif set_piece_type == SetPieceType.FREE_KICK:
        distance = field_position.get("distance_from_goal", 25)

        if distance < 25:
            strategy["setup"] = {
                "shooter": "Direct shot specialist",
                "wall_jumpers": "Every other player in wall",
                "goalkeeper": "Post farthest from shooter"
            }

            strategy["delivery_zones"] = [
                {
                    "zone": "Direct Shot",
                    "percentage": 60,
                    "trajectory": "Over/around wall",
                    "target": "Top corner farthest from goalkeeper"
                }
            ]
        else:
            strategy["setup"] = {
                "delivery": "Cross specialist",
                "attackers": "3-4 in penalty area",
                "edge": "2 players for second balls"
            }

            strategy["delivery_zones"] = [
                {
                    "zone": "Near Post",
                    "percentage": 40,
                    "trajectory": "Driven low",
                    "target": "Near post run"
                },
                {
                    "zone": "Far Post",
                    "percentage": 35,
                    "trajectory": "Lofted high",
                    "target": "Far post run"
                },
                {
                    "zone": "Short Pass",
                    "percentage": 15,
                    "trajectory": "Pass to nearby player",
                    "target": "Retain possession"
                }
            ]

        strategy["movements"] = [
            {"player": "Attackers", "movement": "Make curved runs to lose markers"},
            {"player": "Edge Players", "movement": "Arrive at edge of box for second balls"}
        ]

        strategy["coaching_points"] = [
            "Quality of delivery is paramount",
            "Timing of runs is critical",
            "Be ready for second balls",
            "Deception can create space"
        ]

    elif set_piece_type == SetPieceType.THROW_IN:
        strategy["setup"] = {
            "thrower": "Long throw specialist (30-35m from goal)",
            "attackers": "3-4 in penalty area",
            "edge": "1-2 at edge of box"
        }

        strategy["delivery_zones"] = [
            {
                "zone": "Near Post",
                "percentage": 40,
                "trajectory": "Low, flat",
                "target": "Attacker flicks toward goal"
            },
            {
                "zone": "Middle",
                "percentage": 35,
                "trajectory": "Higher trajectory",
                "target": "Attacker at highest point"
            },
            {
                "zone": "Far Post",
                "percentage": 20,
                "trajectory": "Highest, longest",
                "target": "Long run to far post"
            }
        ]

        strategy["coaching_points"] = [
            "Thrower can move along touchline",
            "Attackers can screen (block defenders)",
            "Second ball opportunities",
            "Quick combinations from short throws"
        ]

    # Adjust for opponent weaknesses
    if opponent_weakness.get("aerial_weakness"):
        strategy["coaching_points"].append("Exploit aerial weakness - more balls into box")

    if opponent_weakness.get("zonal_marking"):
        strategy["coaching_points"].append("Against zonal - find spaces between markers")

    return strategy


def generate_defensive_strategy(
    set_piece_type: SetPieceType,
    field_position: Dict[str, Any],
    personnel: Dict[str, Any],
    opponent_weakness: Dict[str, Any],
    game_state: Dict[str, Any]
) -> Dict[str, Any]:
    """Generate defensive set-piece strategy"""

    strategy = {
        "type": set_piece_type.value,
        "setup": {},
        "positioning": {},
        "responsibilities": []
    }

    if set_piece_type == SetPieceType.CORNER:
        goalkeeper_positioning = opponent_weakness.get("goalkeeper_positioning", "conservative")

        strategy["setup"] = {
            "marking_system": "Zonal marking with man-marking mix",
            "line_distance": "6-8m from goal line",
            "number_in_box": "6-7 players"
        }

        strategy["positioning"] = {
            "near_post": "5-7m from goal, front post zone",
            "middle_front": "8-10m from goal, penalty spot",
            "middle_back": "10-12m from goal, behind penalty spot",
            "far_post": "12-14m from goal, back post zone",
            "edge": "Edge of penalty area for clearances"
        }

        if goalkeeper_positioning == "aggressive":
            strategy["positioning"]["goalkeeper"] = "Starts on line, attacks high balls"
        elif goalkeeper_positioning == "conservative":
            strategy["positioning"]["goalkeeper"] = "Stays on line, protects goal"

        strategy["responsibilities"] = [
            "Each marker owns their zone",
            "Attack ball when it enters zone",
            "Don't follow runners, protect space",
            "Goalkeeper communicates claims",
            "1-2 man-mark dangerous runners"
        ]

    elif set_piece_type == SetPieceType.FREE_KICK:
        distance = field_position.get("distance_from_goal", 25)

        if distance < 25:
            num_players = max(3, distance // 3)

            strategy["setup"] = {
                "wall_size": f"{num_players} players",
                "wall_distance": "9-10m from ball",
                "goalkeeper": "Post farthest from shooter"
            }

            strategy["positioning"] = {
                "end_player": "Behind wall, ready to step",
                "jumping_players": "Every other player in wall",
                "non_jumping": "Cover ground balls"
            }

            strategy["responsibilities"] = [
                "Organize wall quickly",
                "Goalkeeper signals which post to cover",
                "End player covers near post angle",
                "Maintain focus until ball is cleared"
            ]
        else:
            strategy["setup"] = {
                "defensive_shape": f"{'Low' if distance > 35 else 'Mid'} block",
                "players_in_box": "6-7",
                "edge_players": "2-3 for clearances"
            }

            strategy["responsibilities"] = [
                "Protect penalty area",
                "Win first and second balls",
                "Clear decisively",
                "Be ready for counter-attack"
            ]

    elif set_piece_type == SetPieceType.PENALTY:
        strategy["setup"] = {
            "goalkeeper": "Position on line (4-6m from goal)",
            "attackers": "Outside box for rebounds",
            "defenders": "Edge of box for clearance"
        }

        strategy["positioning"] = {
            "goalkeeper": "Center of goal, slightly forward",
            "attackers": "Ready to follow up",
            "defenders": "Ready to clear if saved"
        }

        strategy["responsibilities"] = [
            "Goalkeeper: Wait for shot, don't commit early",
            "Attackers: Follow up all shots",
            "Defenders: Be ready for saves/rebounds"
        ]

    return strategy


def get_fallback_set_piece(request: Dict[str, Any]) -> Dict[str, Any]:
    """Provide fallback set-piece recommendation"""

    set_piece_type = request.get("set_piece_type", "corner")
    attacking_or_defending = request.get("attacking_or_defending", "attacking")

    return {
        "type": set_piece_type,
        "setup": {
            "note": "Standard setup based on set-piece type"
        },
        "delivery_zones": [
            {
                "zone": "Primary Zone",
                "percentage": 60,
                "trajectory": "Standard delivery",
                "target": "Standard target"
            }
        ],
        "movements": [
            {"player": "All Players", "movement": "Standard movements"}
        ],
        "coaching_points": [
            "Quality delivery",
            "Timing of runs",
            "Attack the ball"
        ],
        "note": "Fallback strategy due to error"
    }


if __name__ == "__main__":
    # Example execution
    example_request = {
        "set_piece_type": "corner",
        "attacking_or_defending": "attacking",
        "field_position": {
            "side": "left",
            "distance_from_goal": 30
        },
        "opponent_weakness": {
            "goalkeeper_positioning": "conservative",
            "aerial_weakness": True,
            "zonal_marking": True
        }
    }

    result = execute_set_piece_design(example_request)

    if "error" in result:
        print(f"Error: {result['error']}")
        print(f"Fallback: {result['fallback']}")
    else:
        print("Set-Piece Strategy Result:")
        print(f"Type: {result['strategy']['type']}")
        print(f"Delivery Zones: {len(result['strategy']['delivery_zones'])}")
        print(f"Coaching Points: {len(result['strategy']['coaching_points'])}")
