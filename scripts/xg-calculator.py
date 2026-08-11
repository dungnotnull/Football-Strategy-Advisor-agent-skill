#!/usr/bin/env python3
"""
xG Calculator — Expected Goals calculation and analysis

This script calculates expected goals (xG) for shots based on location,
shot type, and contextual factors. Supports both individual shots and
match-level analysis.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import math
import json


class ShotType(Enum):
    """Types of shots"""
    LEFT_FOOT = "left-foot"
    RIGHT_FOOT = "right-foot"
    HEADER = "header"
    VOLLEY = "volley"
    OTHER = "other"


class AssistType(Enum):
    """Types of assists leading to shots"""
    PASS = "pass"
    CROSS = "cross"
    THROUGH_BALL = "through-ball"
    DRIBBLE = "dribble"
    REBOUND = "rebound"
    NONE = "none"


class Outcome(Enum):
    """Shot outcomes"""
    GOAL = "goal"
    SAVED = "saved"
    BLOCKED = "blocked"
    MISSED = "missed"
    POST = "post"


@dataclass
class Location:
    """Shot location on the pitch"""
    x: float  # Distance from goal line (0-120m)
    y: float  # Horizontal position from center (-40 to 40m)


@dataclass
class Shot:
    """Individual shot data"""
    team: str  # "home" or "away"
    player: str
    minute: int
    location: Location
    shot_type: ShotType
    assist_type: AssistType
    defenders: int  # Number of defenders between shooter and goal
    outcome: Outcome
    game_state: Optional[Tuple[int, int]] = None  # (home_goals, away_goals)


@dataclass
class xGCalculation:
    """xG calculation result"""
    shot: Shot
    base_xg: float
    modifiers: Dict[str, float]
    final_xg: float
    breakdown: Dict[str, any]


@dataclass
class MatchAnalysis:
    """Match-level xG analysis"""
    home_xg: float
    away_xg: float
    home_goals: int
    away_goals: int
    home_shots: int
    away_shots: int
    xg_timeline: List[Dict[str, any]]
    player_xg: Dict[str, float]
    performance_summary: str


class xGCalculator:
    """Calculate expected goals based on shot data"""

    def __init__(self):
        self.zone_boundaries = self._define_zone_boundaries()
        self.base_xg_values = self._calculate_base_xg_values()

    def _define_zone_boundaries(self) -> Dict[str, Tuple[float, float]]:
        """Define shooting zones based on distance from goal"""

        return {
            "zone_1": (0, 6),    # Six-yard box
            "zone_2": (6, 12),   # Penalty spot area
            "zone_3": (12, 20),  # Edge of box
            "zone_4": (20, 120)  # Outside box
        }

    def _calculate_base_xg_values(self) -> Dict[str, float]:
        """Base xG values for each zone"""

        return {
            "zone_1": 0.40,  # Six-yard box
            "zone_2": 0.22,  # Penalty spot
            "zone_3": 0.10,  # Edge of box
            "zone_4": 0.03   # Outside box
        }

    def calculate_shot_xg(self, shot: Shot) -> xGCalculation:
        """Calculate xG for a single shot"""

        # Determine zone and get base xG
        zone = self._determine_zone(shot.location.x)
        base_xg = self._get_zone_base_xg(zone)

        # Calculate modifiers
        modifiers = self._calculate_modifiers(shot, zone)

        # Calculate final xG
        final_xg = base_xg
        for modifier_value in modifiers.values():
            final_xg += modifier_value

        # Ensure xG is within valid range
        final_xg = max(0.01, min(final_xg, 0.99))

        # Create breakdown
        breakdown = {
            "zone": zone,
            "base_xg": base_xg,
            "distance": shot.location.x,
            "angle": self._calculate_angle(shot.location),
            "modifiers": modifiers.copy(),
            "shot_type": shot.shot_type.value,
            "assist_type": shot.assist_type.value,
            "defenders": shot.defenders
        }

        return xGCalculation(
            shot=shot,
            base_xg=base_xg,
            modifiers=modifiers,
            final_xg=round(final_xg, 3),
            breakdown=breakdown
        )

    def _determine_zone(self, distance: float) -> str:
        """Determine which zone a shot is in based on distance"""

        for zone, (min_dist, max_dist) in self.zone_boundaries.items():
            if min_dist <= distance < max_dist:
                return zone
        return "zone_4"  # Default to outside box

    def _get_zone_base_xg(self, zone: str) -> float:
        """Get base xG for a zone"""

        return self.base_xg_values.get(zone, 0.03)

    def _calculate_angle(self, location: Location) -> float:
        """Calculate angle to goal (0 = center, 90 = extreme angle)"""

        if location.y == 0:
            return 0.0

        goal_width = 7.32  # Standard goal width in meters
        angle = math.degrees(math.atan(abs(location.y) / max(location.x, 0.1)))
        return angle

    def _calculate_modifiers(self, shot: Shot, zone: str) -> Dict[str, float]:
        """Calculate xG modifiers based on shot context"""

        modifiers = {}

        # Assist type modifier
        assist_modifiers = {
            AssistType.THROUGH_BALL: 0.05,
            AssistType.DRIBBLE: 0.03,
            AssistType.CROSS: 0.02,
            AssistType.PASS: 0.00,
            AssistType.REBOUND: 0.04,
            AssistType.NONE: -0.02
        }
        modifiers["assist_type"] = assist_modifiers.get(shot.assist_type, 0.0)

        # Defensive pressure modifier
        if shot.defenders == 0:
            modifiers["defenders"] = 0.03
        elif shot.defenders == 1:
            modifiers["defenders"] = 0.00
        elif shot.defenders == 2:
            modifiers["defenders"] = -0.05
        else:
            modifiers["defenders"] = -0.08

        # Shot type modifier
        if zone == "zone_1":  # Close range
            if shot.shot_type == ShotType.HEADER:
                modifiers["shot_type"] = 0.02
            elif shot.shot_type == ShotType.VOLLEY:
                modifiers["shot_type"] = -0.03
        elif zone == "zone_4":  # Long range
            if shot.shot_type in [ShotType.LEFT_FOOT, ShotType.RIGHT_FOOT]:
                modifiers["shot_type"] = 0.01
            elif shot.shot_type == ShotType.HEADER:
                modifiers["shot_type"] = -0.05

        # Angle modifier (wider angle = lower xG)
        angle = self._calculate_angle(shot.location)
        if angle > 45:
            modifiers["angle"] = -0.05
        elif angle > 30:
            modifiers["angle"] = -0.02

        # Game state modifier
        if shot.game_state:
            home_goals, away_goals = shot.game_state

            if shot.team == "home":
                goal_diff = home_goals - away_goals
            else:
                goal_diff = away_goals - home_goals

            if goal_diff > 0:
                modifiers["game_state"] = -0.02  # Leading, might be cautious
            elif goal_diff < 0:
                modifiers["game_state"] = 0.02  # Trailing, might be desperate

        return modifiers

    def calculate_match_xg(self, shots: List[Shot]) -> MatchAnalysis:
        """Calculate xG for an entire match"""

        home_shots_data = [s for s in shots if s.team == "home"]
        away_shots_data = [s for s in shots if s.team == "away"]

        # Calculate total xG
        home_xg = sum(self.calculate_shot_xg(s).final_xg for s in home_shots_data)
        away_xg = sum(self.calculate_shot_xg(s).final_xg for s in away_shots_data)

        # Count goals
        home_goals = sum(1 for s in home_shots_data if s.outcome == Outcome.GOAL)
        away_goals = sum(1 for s in away_shots_data if s.outcome == Outcome.GOAL)

        # Count shots
        home_shots_count = len(home_shots_data)
        away_shots_count = len(away_shots_data)

        # Build timeline (15-minute segments)
        xg_timeline = self._build_xg_timeline(shots)

        # Player xG
        player_xg = self._calculate_player_xg(shots)

        # Performance summary
        performance_summary = self._generate_performance_summary(
            home_xg, away_xg, home_goals, away_goals
        )

        return MatchAnalysis(
            home_xg=round(home_xg, 2),
            away_xg=round(away_xg, 2),
            home_goals=home_goals,
            away_goals=away_goals,
            home_shots=home_shots_count,
            away_shots=away_shots_count,
            xg_timeline=xg_timeline,
            player_xg=player_xg,
            performance_summary=performance_summary
        )

    def _build_xg_timeline(self, shots: List[Shot]) -> List[Dict[str, any]]:
        """Build xG timeline in 15-minute segments"""

        timeline = []
        segments = [
            (0, 15), (15, 30), (30, 45), (45, 60),
            (60, 75), (75, 90)
        ]

        for start, end in segments:
            segment_shots = [s for s in shots if start <= s.minute < end]

            home_segment_xg = sum(
                self.calculate_shot_xg(s).final_xg
                for s in segment_shots if s.team == "home"
            )
            away_segment_xg = sum(
                self.calculate_shot_xg(s).final_xg
                for s in segment_shots if s.team == "away"
            )

            timeline.append({
                "period": f"{start}-{end}'",
                "home_xg": round(home_segment_xg, 2),
                "away_xg": round(away_segment_xg, 2),
                "net_xg": round(home_segment_xg - away_segment_xg, 2)
            })

        return timeline

    def _calculate_player_xg(self, shots: List[Shot]) -> Dict[str, float]:
        """Calculate xG per player"""

        player_xg = {}

        for shot in shots:
            shot_xg = self.calculate_shot_xg(shot).final_xg

            if shot.player in player_xg:
                player_xg[shot.player] += shot_xg
            else:
                player_xg[shot.player] = shot_xg

        # Round to 2 decimal places
        return {player: round(xg, 2) for player, xg in player_xg.items()}

    def _generate_performance_summary(
        self,
        home_xg: float,
        away_xg: float,
        home_goals: int,
        away_goals: int
    ) -> str:
        """Generate human-readable performance summary"""

        xg_difference = home_xg - away_xg
        goal_difference = home_goals - away_goals

        summary_parts = []

        # Overall match summary
        summary_parts.append(f"Final Score: {home_goals}-{away_goals} (xG: {home_xg}-{away_xg})")

        # xG performance
        if xg_difference > 0.5:
            summary_parts.append("Home team dominated xG creation")
        elif xg_difference < -0.5:
            summary_parts.append("Away team dominated xG creation")
        else:
            summary_parts.append("Even xG performance")

        # Finishing performance
        home_conversion = home_goals / max(home_xg, 0.01) if home_xg > 0 else 0
        away_conversion = away_goals / max(away_xg, 0.01) if away_xg > 0 else 0

        if home_conversion > 1.2:
            summary_parts.append("Home team clinical in finishing (overperformance)")
        elif home_conversion < 0.8:
            summary_parts.append("Home team wasteful in finishing (underperformance)")

        if away_conversion > 1.2:
            summary_parts.append("Away team clinical in finishing (overperformance)")
        elif away_conversion < 0.8:
            summary_parts.append("Away team wasteful in finishing (underperformance)")

        # Result fairness
        if abs(xg_difference - goal_difference) > 1.0:
            summary_parts.append("Result does not reflect xG performance")

        return ". ".join(summary_parts) + "."

    def export_to_json(self, analysis: MatchAnalysis, filepath: str):
        """Export match analysis to JSON file"""

        data = {
            "home_xg": analysis.home_xg,
            "away_xg": analysis.away_xg,
            "home_goals": analysis.home_goals,
            "away_goals": analysis.away_goals,
            "home_shots": analysis.home_shots,
            "away_shots": analysis.away_shots,
            "xg_timeline": analysis.xg_timeline,
            "player_xg": analysis.player_xg,
            "performance_summary": analysis.performance_summary
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)


def load_shots_from_dict(shots_data: List[Dict]) -> List[Shot]:
    """Load shots from dictionary data"""

    shots = []

    for shot_data in shots_data:
        location = Location(
            x=shot_data["location"]["x"],
            y=shot_data["location"]["y"]
        )

        shot = Shot(
            team=shot_data["team"],
            player=shot_data["player"],
            minute=shot_data.get("minute", 0),
            location=location,
            shot_type=ShotType(shot_data.get("shot_type", "right-foot")),
            assist_type=AssistType(shot_data.get("assist_type", "pass")),
            defenders=shot_data.get("defenders", 0),
            outcome=Outcome(shot_data["outcome"]),
            game_state=tuple(shot_data["game_state"]) if shot_data.get("game_state") else None
        )

        shots.append(shot)

    return shots


def main():
    """Example usage of the xG calculator"""

    calculator = xGCalculator()

    # Example shots data
    example_shots = [
        Shot(
            team="home",
            player="Mohamed Salah",
            minute=15,
            location=Location(x=8, y=3),
            shot_type=ShotType.RIGHT_FOOT,
            assist_type=AssistType.THROUGH_BALL,
            defenders=1,
            outcome=Outcome.GOAL,
            game_state=(0, 0)
        ),
        Shot(
            team="away",
            player="Harry Kane",
            minute=32,
            location=Location(x=10, y=-2),
            shot_type=ShotType.LEFT_FOOT,
            assist_type=AssistType.PASS,
            defenders=2,
            outcome=Outcome.SAVED,
            game_state=(1, 0)
        ),
        Shot(
            team="home",
            player="Sadio Mané",
            minute=58,
            location=Location(x=15, y=8),
            shot_type=ShotType.HEADER,
            assist_type=AssistType.CROSS,
            defenders=1,
            outcome=Outcome.GOAL,
            game_state=(1, 0)
        )
    ]

    # Calculate individual shot xG
    print("Individual Shot xG:\n")
    for shot in example_shots:
        calculation = calculator.calculate_shot_xg(shot)
        print(f"{shot.player} ({shot.minute}'):")
        print(f"  Base xG: {calculation.base_xg:.3f}")
        print(f"  Modifiers: {calculation.modifiers}")
        print(f"  Final xG: {calculation.final_xg:.3f}")
        print(f"  Outcome: {shot.outcome.value}")
        print()

    # Calculate match xG
    print("\nMatch xG Analysis:\n")
    match_analysis = calculator.calculate_match_xg(example_shots)

    print(f"Home xG: {match_analysis.home_xg}")
    print(f"Away xG: {match_analysis.away_xg}")
    print(f"Home Goals: {match_analysis.home_goals}")
    print(f"Away Goals: {match_analysis.away_goals}")
    print(f"\nPerformance Summary:")
    print(match_analysis.performance_summary)

    print("\nxG Timeline:")
    for segment in match_analysis.xg_timeline:
        print(f"  {segment['period']}: Home {segment['home_xg']} - Away {segment['away_xg']} (Net: {segment['net_xg']})")

    print("\nPlayer xG:")
    for player, xg in sorted(match_analysis.player_xg.items(), key=lambda x: x[1], reverse=True):
        print(f"  {player}: {xg}")


if __name__ == "__main__":
    main()
