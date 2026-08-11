#!/usr/bin/env python3
"""
Opponent Analyzer — Analyze opponent tactical tendencies and weaknesses

This script analyzes opponent data to identify tactical strengths, weaknesses,
and exploitation opportunities for match preparation.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json
from collections import defaultdict


class PlayingStyle(Enum):
    """Opponent playing styles"""
    POSSESSION = "possession"
    COUNTER_ATTACK = "counter-attack"
    DIRECT = "direct"
    BALANCED = "balanced"


class PressingIntensity(Enum):
    """Pressing intensity levels"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class DefensiveBlock(Enum):
    """Defensive block heights"""
    HIGH = "high"
    MID = "mid"
    LOW = "low"


@dataclass
class MatchData:
    """Individual match data for analysis"""
    opponent: str
    formation: str
    playing_style: PlayingStyle
    pressing_intensity: PressingIntensity
    defensive_block: DefensiveBlock
    xg_for: float
    xg_against: float
    goals_for: int
    goals_against: int
    shots_for: int
    shots_against: int
    ppda: float  # Passes Per Defensive Action
    high_turnovers: int  # Possessions won in final third
    set_piece_xg_for: float
    set_piece_xg_against: float
    result: str  # "W", "D", "L"


@dataclass
class OpponentProfile:
    """Comprehensive opponent tactical profile"""
    team_name: str
    recent_form: List[str]
    avg_xg_for: float
    avg_xg_against: float
    avg_ppda: float
    avg_high_turnovers: float
    conversion_rate: float
    tactical_tendencies: Dict[str, any]
    strengths: List[str]
    weaknesses: List[str]
    exploitation_opportunities: List[str]
    recommended_approach: str


class OpponentAnalyzer:
    """Analyze opponent tactical data for match preparation"""

    def __init__(self):
        self.style_patterns = self._initialize_style_patterns()

    def _initialize_style_patterns(self) -> Dict[PlayingStyle, Dict[str, any]]:
        """Initialize characteristic patterns for each playing style"""

        return {
            PlayingStyle.POSSESSION: {
                "expected_xg_for": 1.3,
                "expected_xg_against": 0.9,
                "expected_ppda": 12.0,
                "typical_strengths": ["build-up", "possession-retention", "combination-play"],
                "typical_weaknesses": ["counter-attacks", "transition-moments", "direct-play"],
                "pressing_intensity": PressingIntensity.HIGH
            },
            PlayingStyle.COUNTER_ATTACK: {
                "expected_xg_for": 1.0,
                "expected_xg_against": 1.1,
                "expected_ppda": 14.0,
                "typical_strengths": ["transitions", "direct-play", "counter-attacks"],
                "typical_weaknesses": ["possession-retention", "build-up", "pressure-resistance"],
                "pressing_intensity": PressingIntensity.MEDIUM
            },
            PlayingStyle.DIRECT: {
                "expected_xg_for": 0.9,
                "expected_xg_against": 1.2,
                "expected_ppda": 16.0,
                "typical_strengths": ["aerial-duels", "second-balls", "set-pieces"],
                "typical_weaknesses": ["possession-retention", "build-up", "passing-combinations"],
                "pressing_intensity": PressingIntensity.LOW
            },
            PlayingStyle.BALANCED: {
                "expected_xg_for": 1.1,
                "expected_xg_against": 1.0,
                "expected_ppda": 13.0,
                "typical_strengths": ["adaptability", "balanced-approach"],
                "typical_weaknesses": ["lack-specialization"],
                "pressing_intensity": PressingIntensity.MEDIUM
            }
        }

    def analyze_opponent(
        self,
        matches: List[MatchData],
        team_name: str
    ) -> OpponentProfile:
        """Analyze opponent from recent match data"""

        if not matches:
            raise ValueError("No match data provided for analysis")

        # Calculate averages
        avg_xg_for = sum(m.xg_for for m in matches) / len(matches)
        avg_xg_against = sum(m.xg_against for m in matches) / len(matches)
        avg_ppda = sum(m.ppda for m in matches) / len(matches)
        avg_high_turnovers = sum(m.high_turnovers for m in matches) / len(matches)

        # Calculate conversion rate
        total_goals = sum(m.goals_for for m in matches)
        total_xg = sum(m.xg_for for m in matches)
        conversion_rate = (total_goals / max(total_xg, 0.01)) * 100 if total_xg > 0 else 0

        # Determine recent form
        recent_form = [m.result for m in matches[-5:]]

        # Identify tactical tendencies
        tactical_tendencies = self._identify_tactical_tendencies(matches)

        # Identify strengths and weaknesses
        strengths, weaknesses = self._identify_strengths_weaknesses(
            matches,
            avg_xg_for,
            avg_xg_against,
            avg_ppda,
            avg_high_turnovers
        )

        # Identify exploitation opportunities
        exploitation_opportunities = self._identify_exploitation_opportunities(
            matches,
            weaknesses,
            tactical_tendencies
        )

        # Recommend approach
        recommended_approach = self._recommend_approach(
            tactical_tendencies,
            strengths,
            weaknesses
        )

        return OpponentProfile(
            team_name=team_name,
            recent_form=recent_form,
            avg_xg_for=round(avg_xg_for, 2),
            avg_xg_against=round(avg_xg_against, 2),
            avg_ppda=round(avg_ppda, 1),
            avg_high_turnovers=round(avg_high_turnovers, 1),
            conversion_rate=round(conversion_rate, 1),
            tactical_tendencies=tactical_tendencies,
            strengths=strengths,
            weaknesses=weaknesses,
            exploitation_opportunities=exploitation_opportunities,
            recommended_approach=recommended_approach
        )

    def _identify_tactical_tendencies(
        self,
        matches: List[MatchData]
    ) -> Dict[str, any]:
        """Identify opponent's tactical tendencies"""

        tendencies = {
            "primary_formation": self._get_most_common([m.formation for m in matches]),
            "primary_style": self._get_most_common([m.playing_style.value for m in matches]),
            "pressing_intensity": self._get_most_common([m.pressing_intensity.value for m in matches]),
            "defensive_block": self._get_most_common([m.defensive_block.value for m in matches]),
            "set_piece_focus": self._analyze_set_piece_focus(matches),
            "transition_style": self._analyze_transition_style(matches),
            "pressing_style": self._analyze_pressing_style(matches)
        }

        return tendencies

    def _get_most_common(self, items: List[str]) -> str:
        """Get the most common item from a list"""

        if not items:
            return "unknown"

        counts = defaultdict(int)
        for item in items:
            counts[item] += 1

        return max(counts.items(), key=lambda x: x[1])[0]

    def _analyze_set_piece_focus(self, matches: List[MatchData]) -> Dict[str, float]:
        """Analyze opponent's set-piece focus"""

        total_sp_xg_for = sum(m.set_piece_xg_for for m in matches)
        total_sp_xg_against = sum(m.set_piece_xg_against for m in matches)
        total_matches = len(matches)

        avg_sp_xg_for = total_sp_xg_for / total_matches
        avg_sp_xg_against = total_sp_xg_against / total_matches

        total_xg_for = sum(m.xg_for for m in matches)
        set_piece_percentage = (total_sp_xg_for / max(total_xg_for, 0.01)) * 100 if total_xg_for > 0 else 0

        return {
            "avg_set_piece_xg_for": round(avg_sp_xg_for, 2),
            "avg_set_piece_xg_against": round(avg_sp_xg_against, 2),
            "set_piece_xg_percentage": round(set_piece_percentage, 1)
        }

    def _analyze_transition_style(self, matches: List[MatchData]) -> str:
        """Analyze opponent's transition style"""

        avg_high_turnovers = sum(m.high_turnovers for m in matches) / len(matches)

        if avg_high_turnovers > 6:
            return "aggressive-counter-attacks"
        elif avg_high_turnovers > 3:
            return "moderate-transitions"
        else:
            return "cautious-transitions"

    def _analyze_pressing_style(self, matches: List[MatchData]) -> str:
        """Analyze opponent's pressing style"""

        avg_ppda = sum(m.ppda for m in matches) / len(matches)

        if avg_ppda < 10:
            return "high-press"
        elif avg_ppda < 14:
            return "medium-press"
        else:
            return "low-press"

    def _identify_strengths_weaknesses(
        self,
        matches: List[MatchData],
        avg_xg_for: float,
        avg_xg_against: float,
        avg_ppda: float,
        avg_high_turnovers: float
    ) -> Tuple[List[str], List[str]]:
        """Identify opponent's tactical strengths and weaknesses"""

        strengths = []
        weaknesses = []

        # Attack analysis
        if avg_xg_for > 1.3:
            strengths.append("strong-chance-creation")
        elif avg_xg_for < 0.9:
            weaknesses.append("weak-chance-creation")

        # Defense analysis
        if avg_xg_against < 0.9:
            strengths.append("solid-defensive-organization")
        elif avg_xg_against > 1.3:
            weaknesses.append("vulnerable-defense")

        # Pressing analysis
        if avg_ppda < 11:
            strengths.append("intense-pressing")
        elif avg_ppda > 15:
            weaknesses.append("passive-pressing")

        # Transition analysis
        if avg_high_turnovers > 5:
            strengths.append("effective-transitions")
        elif avg_high_turnovers < 2:
            weaknesses.append("poor-transition-play")

        # Set-piece analysis
        avg_sp_xg_for = sum(m.set_piece_xg_for for m in matches) / len(matches)
        avg_sp_xg_against = sum(m.set_piece_xg_against for m in matches) / len(matches)

        if avg_sp_xg_for > 0.15:
            strengths.append("dangerous-set-pieces")
        if avg_sp_xg_against > 0.15:
            weaknesses.append("vulnerable-set-pieces")

        return strengths, weaknesses

    def _identify_exploitation_opportunities(
        self,
        matches: List[MatchData],
        weaknesses: List[str],
        tendencies: Dict[str, any]
    ) -> List[str]:
        """Identify specific exploitation opportunities"""

        opportunities = []

        # Weakness-based opportunities
        weakness_exploits = {
            "weak-chance-creation": "low-block-patience",
            "vulnerable-defense": "direct-attacks",
            "passive-pressing": "high-press-pressuring",
            "poor-transition-play": "counter-attacking",
            "vulnerable-set-pieces": "set-piece-focus",
            "weak-chance-creation": "pressing-high"
        }

        for weakness in weaknesses:
            if weakness in weakness_exploits:
                opportunities.append(weakness_exploits[weakness])

        # Style-based opportunities
        primary_style = tendencies.get("primary_style", "")

        if primary_style == "possession":
            opportunities.append("counter-attack-exploitation")
            opportunities.append("pressing-triggers")
        elif primary_style == "counter-attack":
            opportunities.append("controlled-possession")
            opportunities.append("defensive-balance")
        elif primary_style == "direct":
            opportunities.append("low-block-organization")
            opportunities.append("aerial-dominance")

        # Pressing-based opportunities
        pressing_style = tendencies.get("pressing_style", "")

        if pressing_style == "high-press":
            opportunities.append("long-ball-bypass")
            opportunities.append("third-man-runs")
        elif pressing_style == "low-press":
            opportunities.append("patient-build-up")
            opportunities.append("final-third-creativity")

        return opportunities

    def _recommend_approach(
        self,
        tendencies: Dict[str, any],
        strengths: List[str],
        weaknesses: List[str]
    ) -> str:
        """Recommended tactical approach against this opponent"""

        primary_style = tendencies.get("primary_style", "")
        pressing_style = tendencies.get("pressing_style", "")

        approach_parts = []

        # Base recommendation on style
        if primary_style == "possession":
            approach_parts.append("Use a mid-block to force them into patient build-up")
            approach_parts.append("Counter-press aggressively in their half")
            approach_parts.append("Look for counter-attack opportunities when they overcommit")
        elif primary_style == "counter-attack":
            approach_parts.append("Maintain defensive balance at all times")
            approach_parts.append("Control possession to limit their transition opportunities")
            approach_parts.append("Exploit their numerical vulnerabilities in midfield")
        elif primary_style == "direct":
            approach_parts.append("Drop to a low block and protect the penalty area")
            approach_parts.append("Win first and second balls aerially")
            approach_parts.append("Build patiently from the back when you win possession")

        # Add pressing-specific recommendations
        if pressing_style == "high-press":
            approach_parts.append("Use third-man runs and quick combinations to bypass their press")
        elif pressing_style == "low-press":
            approach_parts.append("Be patient in build-up, look for openings in their compact block")

        # Add weakness-specific recommendations
        if "vulnerable-set-pieces" in weaknesses:
            approach_parts.append("Focus on set-piece situations for goal-scoring opportunities")

        if "weak-chance-creation" in weaknesses:
            approach_parts.append("Press high to force mistakes in their build-up")

        return ". ".join(approach_parts) + "."

    def export_to_json(self, profile: OpponentProfile, filepath: str):
        """Export opponent profile to JSON file"""

        data = {
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

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)


def load_matches_from_dict(matches_data: List[Dict]) -> List[MatchData]:
    """Load match data from dictionary"""

    matches = []

    for match_data in matches_data:
        match = MatchData(
            opponent=match_data["opponent"],
            formation=match_data["formation"],
            playing_style=PlayingStyle(match_data["playing_style"]),
            pressing_intensity=PressingIntensity(match_data.get("pressing_intensity", "medium")),
            defensive_block=DefensiveBlock(match_data.get("defensive_block", "mid")),
            xg_for=match_data["xg_for"],
            xg_against=match_data["xg_against"],
            goals_for=match_data["goals_for"],
            goals_against=match_data["goals_against"],
            shots_for=match_data.get("shots_for", 0),
            shots_against=match_data.get("shots_against", 0),
            ppda=match_data["ppda"],
            high_turnovers=match_data["high_turnovers"],
            set_piece_xg_for=match_data.get("set_piece_xg_for", 0.0),
            set_piece_xg_against=match_data.get("set_piece_xg_against", 0.0),
            result=match_data["result"]
        )

        matches.append(match)

    return matches


def main():
    """Example usage of the opponent analyzer"""

    analyzer = OpponentAnalyzer()

    # Example match data (simulating last 5 matches)
    example_matches = [
        MatchData(
            opponent="Manchester City",
            formation="4-3-3",
            playing_style=PlayingStyle.POSSESSION,
            pressing_intensity=PressingIntensity.HIGH,
            defensive_block=DefensiveBlock.HIGH,
            xg_for=1.8,
            xg_against=0.7,
            goals_for=2,
            goals_against=0,
            shots_for=15,
            shots_against=8,
            ppda=9.5,
            high_turnovers=7,
            set_piece_xg_for=0.12,
            set_piece_xg_against=0.08,
            result="W"
        ),
        MatchData(
            opponent="Liverpool",
            formation="4-3-3",
            playing_style=PlayingStyle.COUNTER_ATTACK,
            pressing_intensity=PressingIntensity.HIGH,
            defensive_block=DefensiveBlock.MID,
            xg_for=1.2,
            xg_against=1.4,
            goals_for=1,
            goals_against=2,
            shots_for=12,
            shots_against=14,
            ppda=11.2,
            high_turnovers=4,
            set_piece_xg_for=0.18,
            set_piece_xg_against=0.15,
            result="L"
        ),
        MatchData(
            opponent="Chelsea",
            formation="3-5-2",
            playing_style=PlayingStyle.BALANCED,
            pressing_intensity=PressingIntensity.MEDIUM,
            defensive_block=DefensiveBlock.MID,
            xg_for=1.0,
            xg_against=1.0,
            goals_for=1,
            goals_against=1,
            shots_for=11,
            shots_against=11,
            ppda=13.5,
            high_turnovers=3,
            set_piece_xg_for=0.10,
            set_piece_xg_against=0.12,
            result="D"
        ),
        MatchData(
            opponent="Arsenal",
            formation="4-2-3-1",
            playing_style=PlayingStyle.POSSESSION,
            pressing_intensity=PressingIntensity.HIGH,
            defensive_block=DefensiveBlock.HIGH,
            xg_for=1.5,
            xg_against=0.9,
            goals_for=2,
            goals_against=1,
            shots_for=14,
            shots_against=10,
            ppda=10.8,
            high_turnovers=5,
            set_piece_xg_for=0.15,
            set_piece_xg_against=0.10,
            result="W"
        ),
        MatchData(
            opponent="Tottenham",
            formation="4-2-3-1",
            playing_style=PlayingStyle.COUNTER_ATTACK,
            pressing_intensity=PressingIntensity.MEDIUM,
            defensive_block=DefensiveBlock.MID,
            xg_for=0.9,
            xg_against=1.1,
            goals_for=1,
            goals_against=1,
            shots_for=10,
            shots_against=12,
            ppda=14.2,
            high_turnovers=4,
            set_piece_xg_for=0.08,
            set_piece_xg_against=0.14,
            result="D"
        )
    ]

    # Analyze opponent
    profile = analyzer.analyze_opponent(example_matches, "Manchester United")

    # Print results
    print(f"Opponent Analysis: {profile.team_name}\n")
    print(f"Recent Form: {' '.join(profile.recent_form)}")
    print(f"\nAverages:")
    print(f"  xG For: {profile.avg_xg_for}")
    print(f"  xG Against: {profile.avg_xg_against}")
    print(f"  PPDA: {profile.avg_ppda}")
    print(f"  High Turnovers: {profile.avg_high_turnovers}")
    print(f"  Conversion Rate: {profile.conversion_rate}%")

    print(f"\nTactical Tendencies:")
    for key, value in profile.tactical_tendencies.items():
        print(f"  {key}: {value}")

    print(f"\nStrengths:")
    for strength in profile.strengths:
        print(f"  + {strength}")

    print(f"\nWeaknesses:")
    for weakness in profile.weaknesses:
        print(f"  - {weakness}")

    print(f"\nExploitation Opportunities:")
    for opportunity in profile.exploitation_opportunities:
        print(f"  * {opportunity}")

    print(f"\nRecommended Approach:")
    print(f"  {profile.recommended_approach}")


if __name__ == "__main__":
    main()
