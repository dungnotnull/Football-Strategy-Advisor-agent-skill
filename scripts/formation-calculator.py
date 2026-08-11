#!/usr/bin/env python3
"""
Formation Calculator — Optimize formation based on squad profile

This script analyzes a squad's personnel and recommends the optimal formation
and player positioning based on player attributes and tactical requirements.
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import json


class Position(Enum):
    """Standard football positions"""
    GK = "GK"
    RB = "RB"
    RCB = "RCB"
    CB = "CB"
    LCB = "LCB"
    LB = "LB"
    RWB = "RWB"
    LWB = "LWB"
    CDM = "CDM"
    RDM = "RDM"
    LDM = "LDM"
    CM = "CM"
    RCM = "RCM"
    LCM = "LCM"
    RM = "RM"
    LM = "LM"
    CAM = "CAM"
    RAM = "RAM"
    LAM = "LAM"
    RW = "RW"
    LW = "LW"
    RF = "RF"
    LF = "LF"
    ST = "ST"
    CF = "CF"


class Formation(Enum):
    """Common football formations"""
    F4_3_3 = "4-3-3"
    F4_2_3_1 = "4-2-3-1"
    F4_4_2 = "4-4-2"
    F3_5_2 = "3-5-2"
    F5_3_2 = "5-3-2"
    F3_4_3 = "3-4-3"
    F4_1_4_1 = "4-1-4-1"
    F4_3_2_1 = "4-3-2-1"


class PlayingStyle(Enum):
    """Tactical playing styles"""
    POSSESSION = "possession"
    COUNTER_ATTACK = "counter-attack"
    DIRECT = "direct"
    BALANCED = "balanced"


@dataclass
class Player:
    """Player data model"""
    name: str
    position: Position
    rating: int
    secondary_position: Optional[Position] = None
    pace: Optional[int] = None
    passing: Optional[int] = None
    dribbling: Optional[int] = None
    defending: Optional[int] = None
    physical: Optional[int] = None
    aerial: Optional[int] = None
    fitness: Optional[int] = None

    def get_average_attribute(self) -> float:
        """Calculate average of available attributes"""
        attrs = [
            self.pace, self.passing, self.dribbling,
            self.defending, self.physical, self.aerial
        ]
        valid_attrs = [a for a in attrs if a is not None]
        if not valid_attrs:
            return float(self.rating)
        return sum(valid_attrs) / len(valid_attrs)


@dataclass
class FormationScore:
    """Score for a formation recommendation"""
    formation: Formation
    score: float
    reasoning: List[str]
    positioning: Dict[str, str]
    strengths: List[str]
    weaknesses: List[str]


class FormationCalculator:
    """Calculate optimal formation based on squad profile"""

    def __init__(self):
        self.formation_templates = self._load_formation_templates()

    def _load_formation_templates(self) -> Dict[Formation, List[Position]]:
        """Load standard formation templates"""
        return {
            Formation.F4_3_3: [
                Position.GK, Position.RB, Position.RCB, Position.LCB, Position.LB,
                Position.RCM, Position.CM, Position.LCM,
                Position.RW, Position.ST, Position.LW
            ],
            Formation.F4_2_3_1: [
                Position.GK, Position.RB, Position.RCB, Position.LCB, Position.LB,
                Position.CDM, Position.CDM,
                Position.RW, Position.CAM, Position.LW,
                Position.ST
            ],
            Formation.F4_4_2: [
                Position.GK, Position.RB, Position.RCB, Position.LCB, Position.LB,
                Position.RM, Position.CM, Position.CM, Position.LM,
                Position.ST, Position.ST
            ],
            Formation.F3_5_2: [
                Position.GK, Position.RCB, Position.CB, Position.LCB,
                Position.RWB, Position.RCM, Position.CM, Position.LCM, Position.LWB,
                Position.ST, Position.CAM
            ],
            Formation.F5_3_2: [
                Position.GK, Position.RWB, Position.RCB, Position.CB, Position.LCB, Position.LWB,
                Position.CM, Position.CM, Position.CM,
                Position.ST, Position.ST
            ],
            Formation.F3_4_3: [
                Position.GK, Position.RCB, Position.CB, Position.LCB,
                Position.RM, Position.CM, Position.CM, Position.LM,
                Position.RW, Position.ST, Position.LW
            ],
            Formation.F4_1_4_1: [
                Position.GK, Position.RB, Position.RCB, Position.LCB, Position.LB,
                Position.CDM,
                Position.RM, Position.CM, Position.CM, Position.LM,
                Position.ST
            ],
            Formation.F4_3_2_1: [
                Position.GK, Position.RB, Position.RCB, Position.LCB, Position.LB,
                Position.CDM, Position.CM, Position.CM,
                Position.CAM, Position.CAM,
                Position.ST
            ]
        }

    def calculate_best_formation(
        self,
        players: List[Player],
        playing_style: PlayingStyle = PlayingStyle.BALANCED,
        preferred_formation: Optional[Formation] = None
    ) -> List[FormationScore]:
        """Calculate best formations ranked by score"""

        if len(players) < 11:
            raise ValueError("Need at least 11 players")

        # Sort players by rating (descending)
        sorted_players = sorted(players, key=lambda p: p.rating, reverse=True)
        top_11 = sorted_players[:11]

        scores = []

        for formation in Formation:
            # Score each formation
            formation_score = self._score_formation(
                formation,
                top_11,
                playing_style
            )
            scores.append(formation_score)

        # Sort by score (descending)
        scores.sort(key=lambda x: x.score, reverse=True)

        # If preferred formation specified, boost its score
        if preferred_formation:
            for score in scores:
                if score.formation == preferred_formation:
                    score.score += 10
                    score.reasoning.insert(0, f"Preferred formation {preferred_formation.value}")

            # Re-sort after adjustment
            scores.sort(key=lambda x: x.score, reverse=True)

        return scores

    def _score_formation(
        self,
        formation: Formation,
        players: List[Player],
        playing_style: PlayingStyle
    ) -> FormationScore:
        """Score a single formation against the squad"""

        template = self.formation_templates[formation]
        positioning = {}
        reasoning = []
        strengths = []
        weaknesses = []
        score = 0.0

        # Assign players to positions
        position_assignments = self._assign_players_to_positions(
            template,
            players
        )

        # Calculate position fit scores
        total_fit_score = 0
        positions_filled = 0

        for pos_name, player in position_assignments.items():
            if player:
                positions_filled += 1
                fit_score = self._calculate_position_fit(pos_name, player)
                total_fit_score += fit_score

                positioning[pos_name] = player.name

        # Base score: Average fit per position
        if positions_filled > 0:
            base_score = (total_fit_score / positions_filled) * 10
            score += base_score

            reasoning.append(f"Average position fit: {total_fit_score / positions_filled:.2f}/1.0")

        # Style bonus
        style_bonus = self._calculate_style_bonus(formation, playing_style, position_assignments)
        score += style_bonus

        if style_bonus > 0:
            reasoning.append(f"Good fit for {playing_style.value} style (+{style_bonus:.1f})")
        elif style_bonus < 0:
            reasoning.append(f"Poor fit for {playing_style.value} style ({style_bonus:.1f})")

        # Check for tactical strengths
        tactical_analysis = self._analyze_tactical_balance(
            formation,
            position_assignments
        )

        strengths.extend(tactical_analysis["strengths"])
        weaknesses.extend(tactical_analysis["weaknesses"])

        score += tactical_analysis["bonus"]

        return FormationScore(
            formation=formation,
            score=round(score, 1),
            reasoning=reasoning,
            positioning=positioning,
            strengths=strengths,
            weaknesses=weaknesses
        )

    def _assign_players_to_positions(
        self,
        template: List[Position],
        players: List[Player]
    ) -> Dict[str, Optional[Player]]:
        """Assign players to formation positions using best fit algorithm"""

        assignment = {}
        available_players = players.copy()

        for position in template:
            best_player = None
            best_fit_score = -1

            for player in available_players:
                fit_score = self._calculate_position_fit(position, player)

                if fit_score > best_fit_score:
                    best_fit_score = fit_score
                    best_player = player

            if best_player:
                assignment[position.value] = best_player
                available_players.remove(best_player)
            else:
                assignment[position.value] = None

        return assignment

    def _calculate_position_fit(self, position: Position, player: Player) -> float:
        """Calculate how well a player fits a position (0.0 to 1.0)"""

        # Perfect match
        if player.position == position:
            return 1.0

        # Secondary position match
        if player.secondary_position == position:
            return 0.9

        # Position compatibility matrix
        compatibility = self._get_position_compatibility(position, player.position)

        return compatibility

    def _get_position_compatibility(self, target: Position, current: Position) -> float:
        """Get compatibility score between two positions"""

        # Define position families
        defenders = {Position.GK, Position.RB, Position.RCB, Position.CB, Position.LCB, Position.LB, Position.RWB, Position.LWB}
        midfielders = {Position.CDM, Position.RDM, Position.LDM, Position.CM, Position.RCM, Position.LCM, Position.RM, Position.LM, Position.CAM, Position.RAM, Position.LAM}
        forwards = {Position.RW, Position.LW, Position.RF, Position.LF, Position.ST, Position.CF}

        # Same family = moderate compatibility
        if (target in defenders and current in defenders) or \
           (target in midfielders and current in midfielders) or \
           (target in forwards and current in forwards):
            return 0.6

        # Specific position relationships
        relationships = {
            # Fullback relationships
            (Position.RB, Position.RWB): 0.9,
            (Position.RWB, Position.RB): 0.9,
            (Position.LB, Position.LWB): 0.9,
            (Position.LWB, Position.LB): 0.9,

            # Center back relationships
            (Position.RCB, Position.CB): 0.9,
            (Position.CB, Position.RCB): 0.9,
            (Position.LCB, Position.CB): 0.9,
            (Position.CB, Position.LCB): 0.9,

            # Midfield relationships
            (Position.RCM, Position.CM): 0.9,
            (Position.CM, Position.RCM): 0.9,
            (Position.LCM, Position.CM): 0.9,
            (Position.CM, Position.LCM): 0.9,
            (Position.CDM, Position.CM): 0.8,
            (Position.CM, Position.CDM): 0.8,

            # Wide midfielder relationships
            (Position.RM, Position.RW): 0.8,
            (Position.RW, Position.RM): 0.8,
            (Position.LM, Position.LW): 0.8,
            (Position.LW, Position.LM): 0.8,

            # Attacking midfield relationships
            (Position.CAM, Position.ST): 0.7,
            (Position.ST, Position.CAM): 0.7,
        }

        return relationships.get((target, current), 0.3)

    def _calculate_style_bonus(
        self,
        formation: Formation,
        playing_style: PlayingStyle,
        position_assignments: Dict[str, Optional[Player]]
    ) -> float:
        """Calculate bonus/penalty for playing style fit"""

        style_formation_fit = {
            PlayingStyle.POSSESSION: {
                Formation.F4_3_3: 5.0,
                Formation.F4_2_3_1: 4.0,
                Formation.F3_5_2: 3.0,
                Formation.F4_1_4_1: 4.5,
                Formation.F4_3_2_1: 3.5,
            },
            PlayingStyle.COUNTER_ATTACK: {
                Formation.F4_4_2: 5.0,
                Formation.F3_5_2: 4.5,
                Formation.F5_3_2: 4.0,
                Formation.F4_3_3: 3.0,
            },
            PlayingStyle.DIRECT: {
                Formation.F4_4_2: 4.0,
                Formation.F4_3_3: 3.5,
                Formation.F3_4_3: 4.5,
            },
            PlayingStyle.BALANCED: {
                Formation.F4_2_3_1: 4.0,
                Formation.F4_3_3: 4.0,
                Formation.F4_4_2: 4.0,
            }
        }

        return style_formation_fit.get(playing_style, {}).get(formation, 0.0)

    def _analyze_tactical_balance(
        self,
        formation: Formation,
        position_assignments: Dict[str, Optional[Player]]
    ) -> Dict[str, any]:
        """Analyze tactical balance of the formation"""

        analysis = {
            "strengths": [],
            "weaknesses": [],
            "bonus": 0.0
        }

        # Analyze defensive solidity
        defenders = [
            position_assignments.get(p.value)
            for p in [Position.RB, Position.RCB, Position.LCB, Position.LB]
            if p.value in position_assignments
        ]
        defenders = [d for d in defenders if d]

        if len(defenders) >= 3:
            avg_defending = sum(d.defending or d.rating for d in defenders) / len(defenders)
            if avg_defending >= 75:
                analysis["strengths"].append("Strong defensive core")
                analysis["bonus"] += 2.0
            elif avg_defending < 60:
                analysis["weaknesses"].append("Weak defensive core")
                analysis["bonus"] -= 2.0

        # Analyze midfield presence
        midfielders = [
            position_assignments.get(p.value)
            for p in [Position.CDM, Position.CM, Position.RCM, Position.LCM, Position.CAM]
            if p.value in position_assignments
        ]
        midfielders = [m for m in midfielders if m]

        if len(midfielders) >= 3:
            avg_physical = sum(m.physical or m.rating for m in midfielders) / len(midfielders)
            if avg_physical >= 70:
                analysis["strengths"].append("Strong midfield presence")
                analysis["bonus"] += 1.5

        # Analyze attacking threat
        forwards = [
            position_assignments.get(p.value)
            for p in [Position.ST, Position.RW, Position.LW, Position.CAM]
            if p.value in position_assignments
        ]
        forwards = [f for f in forwards if f]

        if len(forwards) >= 2:
            avg_pace = sum(f.pace or f.rating for f in forwards) / len(forwards)
            if avg_pace >= 75:
                analysis["strengths"].append("Pace in attacking positions")
                analysis["bonus"] += 1.0

        return analysis


def load_players_from_dict(players_data: List[Dict]) -> List[Player]:
    """Load players from dictionary data"""

    players = []
    for player_data in players_data:
        player = Player(
            name=player_data["name"],
            position=Position(player_data["position"]),
            rating=player_data["rating"],
            secondary_position=Position(player_data["secondary_position"]) if player_data.get("secondary_position") else None,
            pace=player_data.get("attributes", {}).get("pace"),
            passing=player_data.get("attributes", {}).get("passing"),
            dribbling=player_data.get("attributes", {}).get("dribbling"),
            defending=player_data.get("attributes", {}).get("defending"),
            physical=player_data.get("attributes", {}).get("physical"),
            aerial=player_data.get("attributes", {}).get("aerial"),
            fitness=player_data.get("fitness")
        )
        players.append(player)

    return players


def main():
    """Example usage of the formation calculator"""

    calculator = FormationCalculator()

    # Example squad (can be loaded from JSON)
    example_players = [
        Player("Alisson", Position.GK, 85),
        Player("Alexander-Arnold", Position.RB, 84, passing=88),
        Player("Matip", Position.RCB, 82, aerial=80, defending=82),
        Player("Van Dijk", Position.CB, 89, aerial=88, defending=89),
        Player("Robertson", Position.LB, 84, passing=82, stamina=85),
        Player("Fabinho", Position.CDM, 86, defending=87, physical=84),
        Player("Henderson", Position.RCM, 82, passing=83, physical=81),
        Player("Wijnaldum", Position.LCM, 82, physical=84, stamina=85),
        Player("Salah", Position.RW, 89, pace=90, dribbling=88, shooting=87),
        Player("Firmino", Position.ST, 85, pressing=84, movement=85),
        Player("Mane", Position.LW, 88, pace=89, shooting=86)
    ]

    # Calculate best formations
    scores = calculator.calculate_best_formation(
        players=example_players,
        playing_style=PlayingStyle.POSSESSION
    )

    # Print results
    print("Formation Recommendations:\n")
    for i, score in enumerate(scores[:3], 1):
        print(f"{i}. {score.formation.value} (Score: {score.score})")
        print(f"\nPositioning:")
        for pos, player in score.positioning.items():
            print(f"  {pos}: {player}")

        print(f"\nReasoning:")
        for reason in score.reasoning:
            print(f"  - {reason}")

        print(f"\nStrengths:")
        for strength in score.strengths:
            print(f"  + {strength}")

        print(f"\nWeaknesses:")
        for weakness in score.weaknesses:
            print(f"  - {weakness}")

        print("\n" + "-"*50 + "\n")


if __name__ == "__main__":
    main()
