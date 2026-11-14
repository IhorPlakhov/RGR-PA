graph = {
    1: {12, 14},
    2: {3, 4},
    3: {2, 4, 6, 10},
    4: {2, 3, 5, 6},
    5: {4, 7, 8},
    6: {3, 4, 7},
    7: {5, 6, 8},
    8: {5, 7, 9},
    9: {8, 11, 12},
    10: {3, 11, 13},
    11: {9, 10, 12},
    12: {1, 9, 11, 13, 14},
    13: {10, 12, 14},
    14: {1, 12, 13},
}


def backtracking(
    adjacency_dictionary: dict[int : set[int]],
    heuristic_fn,
    num_colors: int,
) -> tuple[dict[int:int], int, int]:

    states_count = 0
    backtracks_count = 0

    colors_dict = {node: None for node in adjacency_dictionary}

    palette = set(range(1, num_colors + 1))

    def backtracking_step(current_node: int | None) -> dict[int, int | None] | None:
        # nonlocal allows us to modify the variables not only get their values
        nonlocal states_count, backtracks_count
        states_count += 1

        if current_node is None:
            return colors_dict

        for color in get_valid_colors(
            current_node, palette, adjacency_dictionary, colors_dict
        ):
            colors_dict[current_node] = color
            next_node = heuristic_fn(adjacency_dictionary, colors_dict)
            result = backtracking_step(next_node)
            if result is not None:
                return result

            colors_dict[current_node] = None

        backtracks_count += 1
        return None

    first_node = heuristic_fn(adjacency_dictionary, colors_dict)
    return backtracking_step(first_node), states_count, backtracks_count


def get_valid_colors(
    node: int,
    palette: set[int],
    adj_dictionary: dict[int, set[int]],
    colors_dict: dict[int, int | None],
) -> set[int]:
    neighbor_colors = {
        colors_dict[nb] for nb in adj_dictionary[node] if colors_dict[nb] is not None
    }
    return palette - neighbor_colors


def degree_heuristic(
    adj_dictionary: dict[int : set[int]], colors_dict: dict[int, int | None]
):
    nodes_list = [
        i for i in adj_dictionary if i not in colors_dict or colors_dict[i] is None
    ]
    if not nodes_list:
        return None

    return max(nodes_list, key=lambda node: len(adj_dictionary[node]))


def without_heuristic(
    adj_dictionary: dict[int : set[int]], colors_dict: dict[int, int | None]
):
    nodes_list = [
        i for i in adj_dictionary if i not in colors_dict or colors_dict[i] is None
    ]
    if not nodes_list:
        return None

    return nodes_list[0]


if __name__ == "__main__":
    results = backtracking(graph, degree_heuristic, 3)
    print(results[0])
    print(f"States visited: {results[1]}")
    print(f"Backtracks: {results[2]}")
    results = backtracking(graph, without_heuristic, 3)
    print(results[0])
    print(f"States visited: {results[1]}")
    print(f"Backtracks: {results[2]}")
