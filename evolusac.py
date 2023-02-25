import random
from dataclasses import dataclass
from typing import TypeVar

POD_SIZE: int = 4
MAX_HOUSES: int = 100
DEADLY_OCCURRENCE_CHANCE: float = 0.9
INITIAL_ALTRUISTIC_PERCENT: float = 0.3
NUM_DAYS: int = 35


# utils
T = TypeVar("T")
def flatten(arg: list[list[T]]) -> list[T]:
    flatlist = []
    for sublist in arg:
        flatlist.extend(sublist)
    return flatlist


@dataclass
class Critter:
    altruistic: bool


# typing
Pod = list[Critter]


def make_random_critter(p: float):  # p = percent altruistic
    if random.random() < p:
        return Critter(True)
    else:
        return Critter(False)


def get_child(parent1: Critter, parent2: Critter):
    child_altruism = random.choice([parent1, parent2]).altruistic
    return Critter(child_altruism)


"""
Pods go on an adventure!
At least one of them probably dies.
"""


def adventure(pod: Pod) -> None:
    if random.random() > DEADLY_OCCURRENCE_CHANCE:
        return
    if len(pod) == 0:
        return

    watcher = pod[0]
    if watcher.altruistic:
        del pod[0]
    else:
        for _ in range(len(pod) - 1):
            del pod[1]


def get_initial_population() -> list[Pod]:
    pods = []
    for _ in range(MAX_HOUSES):
        pod = [make_random_critter(INITIAL_ALTRUISTIC_PERCENT) for _ in range(POD_SIZE)]
        pods.append(pod)
    return pods


def run_day(population: list[Pod]) -> list[Pod]:
    for pod in population:
        adventure(pod)

    survivers = flatten(population)
    random.shuffle(survivers)
    num_houses = min(MAX_HOUSES, (len(survivers) // 2))
    survivers = survivers[0 : 2 * num_houses]

    newborns: list[Pod] = []
    for i in range(num_houses):
        c1 = survivers[2 * i]
        c2 = survivers[2 * i + 1]

        newpod = []
        for _ in range(POD_SIZE):
            newpod.append(get_child(c1, c2))
        newborns.append(newpod)
    return newborns


def get_world_string(num_cowardly: int, num_altruistic: int) -> str:
    total = MAX_HOUSES * POD_SIZE

    # clean up a bit
    output_length = 40
    ret = ""
    for i in range(output_length):
        if i / output_length < num_cowardly / total:
            ret += "#"  # cowardly
        elif i / output_length < (num_cowardly + num_altruistic) / total:
            ret += "&"  # altruistic
        else:
            ret += "-"  # dead
    return ret


# -> (num, num_cowardly, num_altruistic)
def get_stats(population: list[Pod]) -> tuple[int, int, int]:
    num_altruistic = 0
    num_cowardly = 0
    num = 0
    for pod in population:
        for critter in pod:
            num += 1
            if critter.altruistic:
                num_altruistic += 1
            else:
                num_cowardly += 1
    return num, num_cowardly, num_altruistic


if __name__ == "__main__":
    population: list[Pod]
    population = get_initial_population()

    num, num_cowardly, num_altruistic = get_stats(population)
    print(
        f"Starting! Initial population {num}, split into {num_cowardly} cowards and {num_altruistic} altruists."
    )
    for i in range(NUM_DAYS):
        population = run_day(population)

        num, num_cowardly, num_altruistic = get_stats(population)
        print(f"Round {(i+1):02}: {get_world_string(num_cowardly, num_altruistic)}")

    num, num_cowardly, num_altruistic = get_stats(population)
    print(
        f"Finished! Final talley {num} living, split into split into {num_cowardly} cowards and {num_altruistic} altruists"
    )
