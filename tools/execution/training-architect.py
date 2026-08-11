#!/usr/bin/env python3
"""
Training Architect Tool Execution Handler

This handler executes training session design and periodization
planning requests using the skill's training framework and
periodization principles.
"""

import sys
import os
from typing import Dict, Any, List
from enum import Enum
from datetime import datetime, timedelta


class SessionType(Enum):
    """Types of training sessions"""
    TACTICAL = "tactical"
    TECHNICAL = "technical"
    CONDITIONING = "conditioning"
    RECOVERY = "recovery"
    MATCH_PREP = "match-prep"
    SET_PIECE = "set-piece"
    PERIODIZATION = "periodization"


class Intensity(Enum):
    """Training intensity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


def execute_training_design(request: Dict[str, Any]) -> Dict[str, Any]:
    """Execute training session/periodization design"""

    try:
        # Validate input
        if "session_type" not in request:
            raise ValueError("Missing required field: 'session_type'")

        session_type = SessionType(request["session_type"])

        # Get optional parameters
        duration = request.get("duration", 90)
        intensity = Intensity(request.get("intensity", "medium"))
        focus_topic = request.get("focus_topic")
        formation = request.get("formation")
        player_availability = request.get("player_availability", {})
        periodization_request = request.get("periodization_request", {})
        constraints = request.get("constraints", {})
        next_match = request.get("next_match", {})

        # Route to appropriate handler
        if session_type == SessionType.PERIODIZATION:
            return execute_periodization_design(periodization_request, next_match)
        else:
            return execute_session_design(
                session_type,
                duration,
                intensity,
                focus_topic,
                formation,
                player_availability,
                constraints,
                next_match
            )

    except Exception as e:
        return {
            "error": str(e),
            "error_type": type(e).__name__,
            "fallback": get_fallback_training(request)
        }


def execute_session_design(
    session_type: SessionType,
    duration: int,
    intensity: Intensity,
    focus_topic: str,
    formation: str,
    player_availability: Dict[str, Any],
    constraints: Dict[str, Any],
    next_match: Dict[str, Any]
) -> Dict[str, Any]:
    """Execute training session design"""

    session_plan = {
        "session_type": session_type.value,
        "duration": duration,
        "intensity": intensity.value,
        "load_calculation": duration * intensity_value(intensity)
    }

    # Warm-up (typically 15-20% of session)
    warm_up_duration = max(10, duration // 5)
    session_plan["warm_up"] = {
        "duration": warm_up_duration,
        "activity": get_warm_up_activity(session_type, intensity),
        "exercises": [
            {"exercise": "Ball circulation", "duration": 5, "description": "Passing in groups of 3"},
            {"exercise": "Dynamic stretches", "duration": 3, "description": "Mobility and activation"},
            {"exercise": "Progressive sprints", "duration": 2, "description": "Build up to match intensity"}
        ],
        "coaching_points": "Gradual increase in intensity, focus on ball feeling"
    }

    # Cool-down (typically 10-15% of session)
    cool_down_duration = max(10, duration // 8)
    session_plan["cool_down"] = {
        "duration": cool_down_duration,
        "activity": "Recovery and reflection",
        "exercises": [
            {"exercise": "Light jogging", "duration": 3, "description": "Gradual cool down"},
            {"exercise": "Static stretching", "duration": 5, "description": "Focus on tight areas"},
            {"exercise": "Foam rolling", "duration": 2, "description": "Self-myofascial release"}
        ],
        "recovery_focus": "Hydration, nutrition, and rest emphasized"
    }

    # Main content duration
    main_duration = duration - warm_up_duration - cool_down_duration

    # Design main phases based on session type
    phases = []

    if session_type == SessionType.TACTICAL:
        phases = design_tactical_session(main_duration, focus_topic, formation, intensity)
    elif session_type == SessionType.TECHNICAL:
        phases = design_technical_session(main_duration, focus_topic, intensity)
    elif session_type == SessionType.CONDITIONING:
        phases = design_conditioning_session(main_duration, intensity)
    elif session_type == SessionType.RECOVERY:
        phases = design_recovery_session(main_duration)
    elif session_type == SessionType.MATCH_PREP:
        phases = design_match_prep_session(main_duration, next_match, formation)
    elif session_type == SessionType.SET_PIECE:
        phases = design_set_piece_session(main_duration, focus_topic, intensity)

    session_plan["phases"] = phases

    # Add formation and personnel info
    if formation:
        session_plan["formation"] = formation

    if player_availability:
        total_players = player_availability.get("total_players", 20)
        session_plan["player_numbers"] = {
            "total": total_players,
            "available": total_players - len(player_availability.get("unavailable_players", [])),
            "goalkeepers": player_availability.get("goalkeepers", 2)
        }

    # Add match context if available
    if next_match:
        session_plan["match_context"] = {
            "opponent": next_match.get("opponent", "Unknown"),
            "days_until_match": next_match.get("days_until_match", 7),
            "importance": next_match.get("match_importance", "medium"),
            "alignment": "Session aligned to prepare for opponent"
        }

    return {
        "session_plan": session_plan
    }


def execute_periodization_design(
    periodization_request: Dict[str, Any],
    next_match: Dict[str, Any]
) -> Dict[str, Any]:
    """Execute periodization planning"""

    phase = periodization_request.get("phase", "in-season")
    weeks = periodization_request.get("weeks", 4)
    matches_per_week = periodization_request.get("matches_per_week", 1)
    focus_area = periodization_request.get("focus_area", "balanced")
    key_dates = periodization_request.get("key_dates", [])

    periodization_plan = {
        "phase": phase,
        "duration_weeks": weeks,
        "focus_area": focus_area,
        "weeks": []
    }

    # Generate weekly plans
    for week_num in range(1, weeks + 1):
        week_plan = generate_week_plan(
            week_num,
            phase,
            matches_per_week,
            focus_area,
            key_dates,
            next_match
        )
        periodization_plan["weeks"].append(week_plan)

    return {
        "periodization_plan": periodization_plan
    }


def generate_week_plan(
    week_num: int,
    phase: str,
    matches_per_week: int,
    focus_area: str,
    key_dates: List[Dict[str, Any]],
    next_match: Dict[str, Any]
) -> Dict[str, Any]:
    """Generate weekly training plan"""

    week_plan = {
        "week_number": week_num,
        "focus": get_week_focus(week_num, phase, focus_area),
        "days": []
    }

    # Standard week structure (can be adjusted based on match schedule)
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    for day in days:
        day_plan = generate_day_plan(
            day,
            week_num,
            phase,
            matches_per_week,
            focus_area
        )
        week_plan["days"].append(day_plan)

    return week_plan


def generate_day_plan(
    day: str,
    week_num: int,
    phase: str,
    matches_per_week: int,
    focus_area: str
) -> Dict[str, Any]:
    """Generate daily training plan"""

    # Adjust based on typical match day (Saturday)
    if day == "Monday":
        return {
            "day": day,
            "session": {
                "type": "recovery",
                "duration": 45,
                "intensity": "low",
                "focus": "Recovery from match, video analysis"
            }
        }
    elif day == "Tuesday":
        return {
            "day": day,
            "session": {
                "type": "tactical",
                "duration": 75,
                "intensity": "medium",
                "focus": "Tactical training, medium conditioning"
            }
        }
    elif day == "Wednesday":
        return {
            "day": day,
            "session": {
                "type": "conditioning",
                "duration": 60,
                "intensity": "high",
                "focus": "High-intensity conditioning, set-pieces"
            }
        }
    elif day == "Thursday":
        return {
            "day": day,
            "session": {
                "type": "match-prep",
                "duration": 60,
                "intensity": "medium-high",
                "focus": "Tactical preparation for opponent"
            }
        }
    elif day == "Friday":
        return {
            "day": day,
            "session": {
                "type": "match-prep",
                "duration": 45,
                "intensity": "low",
                "focus": "Light preparation, set-piece rehearsal"
            }
        }
    elif day == "Saturday":
        return {
            "day": day,
            "session": {
                "type": "match",
                "duration": 90,
                "intensity": "maximum",
                "focus": "Competitive match"
            }
        }
    elif day == "Sunday":
        return {
            "day": day,
            "session": {
                "type": "recovery",
                "duration": 30,
                "intensity": "very-low",
                "focus": "Rest / Light recovery"
            }
        }

    return {"day": day, "session": None}


def intensity_value(intensity: Intensity) -> float:
    """Get numeric value for intensity (for load calculation)"""
    values = {
        Intensity.LOW: 5,
        Intensity.MEDIUM: 7,
        Intensity.HIGH: 9
    }
    return values.get(intensity, 7)


def get_warm_up_activity(session_type: SessionType, intensity: Intensity) -> str:
    """Get appropriate warm-up activity"""

    if session_type == SessionType.RECOVERY:
        return "Light activation and mobility"
    elif intensity == Intensity.HIGH:
        return "High-intensity activation with sprints"
    else:
        return "Standard warm-up with ball work"


def design_tactical_session(
    duration: int,
    focus_topic: str,
    formation: str,
    intensity: Intensity
) -> List[Dict[str, Any]]:
    """Design tactical session phases"""

    return [
        {
            "name": "Phase 1: Shape Training",
            "duration": duration // 3,
            "objective": "Establish defensive/attacking shape",
            "setup": f"{'Full pitch' if duration > 60 else 'Half pitch'} with positional markers",
            "activity": "Shadow play and positional movements",
            "coaching_points": [
                "Maintain spacing and compactness",
                "Communicate positioning",
                "Understand movement triggers"
            ],
            "progressions": [
                "Walk through without opposition",
                "Add passive opposition",
                "Game-speed repetitions"
            ]
        },
        {
            "name": "Phase 2: Tactical Game",
            "duration": duration // 2,
            "objective": "Apply tactical principles in game situation",
            "setup": f"{'6v6' if duration < 50 else '8v8'} with goalkeepers",
            "activity": f"{'Small-sided game' if duration < 60 else 'Phase play'} focused on {focus_topic or 'tactical principles'}",
            "coaching_points": [
                "Apply training session tactical points",
                "Game management and decision making",
                "Transition moments"
            ],
            "regressions": "Reduce numbers if quality drops"
        }
    ]


def design_technical_session(
    duration: int,
    focus_topic: str,
    intensity: Intensity
) -> List[Dict[str, Any]]:
    """Design technical session phases"""

    return [
        {
            "name": "Phase 1: Technical Drill",
            "duration": duration // 2,
            "objective": "Improve technical proficiency",
            "setup": f"{focus_topic or 'Passing'} drills in 30x30m area",
            "activity": "Repetitions with technical focus",
            "coaching_points": [
                "Quality of touch",
                "Body shape",
                "Decision making",
                "Execution under pressure"
            ]
        },
        {
            "name": "Phase 2: Technical Application",
            "duration": duration // 2,
            "objective": "Apply technical skills in game context",
            "setup": "Small-sided game with technical constraints",
            "activity": "Game with specific technical focus",
            "coaching_points": [
                "Execute skills at game speed",
                "Maintain technical quality",
                "Make good decisions"
            ]
        }
    ]


def design_conditioning_session(
    duration: int,
    intensity: Intensity
) -> List[Dict[str, Any]]:
    """Design conditioning session phases"""

    if intensity == Intensity.HIGH:
        return [
            {
                "name": "Phase 1: High-Intensity Intervals",
                "duration": duration // 2,
                "objective": "Develop anaerobic capacity",
                "setup": "Shuttle runs or sprint intervals",
                "activity": "30s work / 30s rest intervals",
                "coaching_points": [
                    "Maximum effort on work intervals",
                    "Maintain technique",
                    "Recovery management"
                ]
            },
            {
                "name": "Phase 2: Tactical Conditioning",
                "duration": duration // 2,
                "objective": "Apply fitness to tactical situations",
                "setup": "Small-sided game with intensity requirement",
                "activity": "High-intensity game with minimal breaks",
                "coaching_points": [
                    "Maintain intensity throughout",
                    "Tactical execution under fatigue",
                    "Concentration management"
                ]
            }
        ]
    else:
        return [
            {
                "name": "Phase 1: Endurance Work",
                "duration": duration,
                "objective": "Build aerobic capacity",
                "setup": "Continuous running or interval training",
                "activity": "Moderate-intensity conditioning",
                "coaching_points": [
                    "Maintain consistent effort",
                    "Pacing strategy",
                    "Technical focus under fatigue"
                ]
            }
        ]


def design_recovery_session(duration: int) -> List[Dict[str, Any]]:
    """Design recovery session phases"""

    return [
        {
            "name": "Regeneration Activities",
            "duration": duration,
            "objective": "Promote recovery and regeneration",
            "setup": "Pool, cycling, or light pitch activities",
            "activity": "Low-intensity regeneration work",
            "coaching_points": [
                "Focus on recovery process",
                "Stay hydrated",
                "Communication with staff on physical state"
            ]
        }
    ]


def design_match_prep_session(
    duration: int,
    next_match: Dict[str, Any],
    formation: str
) -> List[Dict[str, Any]]:
    """Design match preparation session phases"""

    opponent = next_match.get("opponent", "Unknown")
    opponent_style = next_match.get("opponent_style", "balanced")

    return [
        {
            "name": "Phase 1: Opponent Analysis",
            "duration": duration // 3,
            "objective": "Understand opponent tendencies",
            "setup": "Video analysis or walkthrough",
            "activity": f"Prepare for {opponent} ({opponent_style})",
            "coaching_points": [
                "Identify key opponent strengths",
                "Plan tactical responses",
                "Understand pressing triggers"
            ]
        },
        {
            "name": "Phase 2: Set-Piece Rehearsal",
            "duration": duration // 4,
            "objective": "Prepare set-piece routines",
            "setup": "Full set-piece rehearsal",
            "activity": "2 attacking and 2 defensive routines",
            "coaching_points": [
                "Timing of movements",
                "Delivery quality",
                "Defensive organization"
            ]
        },
        {
            "name": "Phase 3: Match Simulation",
            "duration": duration // 2,
            "objective": "Simulate match situations",
            "setup": f"{'Starting XI' if duration > 45 else 'Small-sided'} vs shadow opponent",
            "activity": "Match scenarios and situations",
            "coaching_points": [
                "Game management",
                "Communication",
                "Match focus"
            ]
        }
    ]


def design_set_piece_session(
    duration: int,
    focus_topic: str,
    intensity: Intensity
) -> List[Dict[str, Any]]:
    """Design set-piece session phases"""

    set_piece_type = focus_topic or "corners"

    return [
        {
            "name": "Phase 1: Attacking Routines",
            "duration": duration // 2,
            "objective": f"Practice {set_piece_type} attacking routines",
            "setup": f"Full {set_piece_type} setup with defenders",
            "activity": "3-4 different routines with repetitions",
            "coaching_points": [
                "Delivery quality and consistency",
                "Timing of runs",
                "Competition for the ball",
                "Second ball anticipation"
            ]
        },
        {
            "name": "Phase 2: Defensive Organization",
            "duration": duration // 2,
            "objective": f"Practice {set_piece_type} defensive setup",
            "setup": f"Defensive organization vs {set_piece_type}",
            "activity": "Defensive positioning and clearances",
            "coaching_points": [
                "Individual responsibilities",
                "Communication",
                "Clearing decisiveness",
                "Second reactions"
            ]
        }
    ]


def get_week_focus(week_num: int, phase: str, focus_area: str) -> str:
    """Get weekly training focus"""

    focus_progression = {
        "fitness": ["Base endurance", "Aerobic power", "Anaerobic capacity", "Match fitness"],
        "tactical": ["Shape", "Pressing", "Transitions", "Set-pieces"],
        "technical": ["Passing", "First touch", "Decision making", "Combinations"],
        "balanced": ["Mixed focus", "Balanced development", "Integration", "Refinement"]
    }

    progression = focus_progression.get(focus_area, focus_progression["balanced"])
    index = (week_num - 1) % len(progression)

    return progression[index]


def get_fallback_training(request: Dict[str, Any]) -> Dict[str, Any]:
    """Provide fallback training recommendation"""

    session_type = request.get("session_type", "tactical")

    return {
        "session_plan": {
            "type": session_type,
            "duration": 90,
            "intensity": "medium",
            "warm_up": {
                "duration": 15,
                "activity": "Standard warm-up"
            },
            "phases": [
                {
                    "name": "Main Session",
                    "duration": 60,
                    "activity": "Balanced training session",
                    "coaching_points": ["Focus on execution", "Maintain intensity"]
                }
            ],
            "cool_down": {
                "duration": 15,
                "activity": "Standard cool-down"
            },
            "note": "Fallback session due to error"
        }
    }


if __name__ == "__main__":
    # Example execution
    example_request = {
        "session_type": "tactical",
        "duration": 90,
        "intensity": "medium",
        "focus_topic": "defensive-shape",
        "formation": "4-3-3",
        "next_match": {
            "opponent": "Manchester City",
            "days_until_match": 4,
            "match_importance": "high"
        }
    }

    result = execute_training_design(example_request)

    if "error" in result:
        print(f"Error: {result['error']}")
        print(f"Fallback: {result['fallback']}")
    else:
        print("Training Design Result:")
        if "session_plan" in result:
            print(f"Type: {result['session_plan']['session_type']}")
            print(f"Duration: {result['session_plan']['duration']}min")
            print(f"Phases: {len(result['session_plan']['phases'])}")
        elif "periodization_plan" in result:
            print(f"Weeks: {len(result['periodization_plan']['weeks'])}")
