import time
from pathlib import Path

import numpy as np

# which games would have been possible with this many red, green and blue cubes
maximum_balls = np.array([12, 13, 14])
test_answer = 8  # sum of the possible game ID's

color_to_vec = {
    "red": np.array([1, 0, 0]),
    "green": np.array([0, 1, 0]),
    "blue": np.array([0, 0, 1]),
}


def main():
    two_star()


def two_star():
    lines = Path("./input.txt").read_text().split("\n")
    answer = sum(map(line_to_power, lines))
    print(answer)


def line_to_power(line):
    try:
        (game, handfuls) = line.split(":")
    except ValueError:
        return 0

    handfuls = handfuls.split(";")
    return np.max(list(map(handful_to_balls, handfuls)), axis=0).prod()


def one_star():
    lines = Path("./input.txt").read_text().split("\n")
    answer = sum(map(line_to_game_id, lines))
    print(answer)


def line_to_game_id(line):
    try:
        (game, handfuls) = line.split(":")
    except ValueError:
        return 0

    game_id = int(game.split(" ")[-1])
    handfuls = handfuls.split(";")
    possible = (
        np.max(list(map(handful_to_balls, handfuls)), axis=0) <= maximum_balls
    ).all()
    return possible * game_id


def handful_to_balls(handful):
    balls = handful.split(",")
    balls = sum(map(ball_to_vec, balls))
    return balls  # in [r, g, b] array


def ball_to_vec(ball):
    n_ball, color = ball.strip().split(" ")
    return int(n_ball) * color_to_vec[color.strip().casefold()]


if __name__ == "__main__":
    start_time = time.perf_counter()
    main()
    end_time = time.perf_counter()
    print(f"It took {end_time - start_time} seconds")
