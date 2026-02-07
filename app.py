import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


DATA_PATH = Path(__file__).parent / "data" / "teams.csv"
HOME_ADVANTAGE = 55  # Elo points
DRAW_BASE = 0.24
DRAW_SCALER = 0.0025


@dataclass(frozen=True)
class Team:
    league: str
    division: int
    name: str
    elo: int


def load_teams(path: Path = DATA_PATH) -> List[Team]:
    if not path.exists():
        raise FileNotFoundError(f"No se encontró el archivo de datos: {path}")

    teams: List[Team] = []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            teams.append(
                Team(
                    league=row["league"].strip(),
                    division=int(row["division"]),
                    name=row["team"].strip(),
                    elo=int(row["elo"]),
                )
            )
    return teams


def group_by_league(teams: Iterable[Team]) -> Dict[str, List[Team]]:
    grouped: Dict[str, List[Team]] = {}
    for team in teams:
        grouped.setdefault(team.league, []).append(team)
    return grouped


def find_team(teams: Iterable[Team], league: str, name: str) -> Team:
    for team in teams:
        if team.league.lower() == league.lower() and team.name.lower() == name.lower():
            return team
    raise ValueError(f"Equipo no encontrado en {league}: {name}")


def expected_score(elo_a: int, elo_b: int) -> float:
    return 1 / (1 + 10 ** ((elo_b - elo_a) / 400))


def draw_probability(elo_gap: int) -> float:
    raw = DRAW_BASE - (abs(elo_gap) * DRAW_SCALER / 100)
    return max(0.12, min(0.30, raw))


def predict_match(home: Team, away: Team) -> Tuple[float, float, float]:
    adjusted_home = home.elo + HOME_ADVANTAGE
    win_prob = expected_score(adjusted_home, away.elo)
    draw_prob = draw_probability(adjusted_home - away.elo)
    home_win = win_prob * (1 - draw_prob)
    away_win = (1 - win_prob) * (1 - draw_prob)
    return home_win, draw_prob, away_win


def format_prediction(home: Team, away: Team) -> str:
    home_win, draw, away_win = predict_match(home, away)
    return (
        f"Pronóstico {home.name} vs {away.name}:\n"
        f"- Victoria local: {home_win:.1%}\n"
        f"- Empate: {draw:.1%}\n"
        f"- Victoria visitante: {away_win:.1%}"
    )


def list_leagues(teams: Iterable[Team]) -> List[str]:
    leagues = sorted({team.league for team in teams})
    return leagues


def list_teams_for_league(teams: Iterable[Team], league: str) -> List[str]:
    return sorted(
        [team.name for team in teams if team.league.lower() == league.lower()]
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Pronosticador de resultados europeos")
    parser.add_argument("--league", help="Nombre de la liga")
    parser.add_argument("--home", help="Equipo local")
    parser.add_argument("--away", help="Equipo visitante")
    parser.add_argument("--list-leagues", action="store_true", help="Listar ligas")
    parser.add_argument(
        "--list-teams", action="store_true", help="Listar equipos de una liga"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    teams = load_teams()

    if args.list_leagues:
        print("Ligas disponibles:")
        for league in list_leagues(teams):
            print(f"- {league}")
        return

    if args.list_teams:
        if not args.league:
            raise SystemExit("Debes indicar --league para listar equipos")
        print(f"Equipos en {args.league}:")
        for team in list_teams_for_league(teams, args.league):
            print(f"- {team}")
        return

    if not (args.league and args.home and args.away):
        raise SystemExit("Debes indicar --league, --home y --away")

    home = find_team(teams, args.league, args.home)
    away = find_team(teams, args.league, args.away)

    print(format_prediction(home, away))


if __name__ == "__main__":
    main()
