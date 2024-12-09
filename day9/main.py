from pathlib import Path

FILE_DIR = Path(__file__).parent.absolute()


def get_input() -> str:
    with open(FILE_DIR / "input.txt", "r") as f:
        data = f.read().strip()
    return data


def part1(disk_map: str) -> int:
    blocks = []
    dot_idxs = []
    for idx, val in enumerate(disk_map):
        if idx % 2:
            dot_idxs += list(range(len(blocks), len(blocks) + int(val)))
            blocks += f"." * int(val)
        else:
            blocks += [int(idx / 2) for _ in range(int(val))]
    dot_idx = 0
    for i in reversed(range(len(blocks))):
        if blocks[i] != "." and dot_idxs[dot_idx] < i:
            blocks[dot_idxs[dot_idx]], blocks[i] = blocks[i], "."
            dot_idx += 1
    return sum([int(x) * int(y) for x, y in enumerate(blocks) if y != "."])


def part2(disk_map: str) -> int:
    blocks = []
    block_idxs = []  # (start_idx, space)
    dot_idxs = []  # (start_idx, space)
    for idx, val in enumerate(disk_map):
        if idx % 2:
            dot_idxs.append((len(blocks), int(val)))
            blocks += f"." * int(val)
        else:
            block_idxs.append((len(blocks), int(val)))
            blocks += [int(idx / 2) for _ in range(int(val))]
    for i in reversed(range(len(block_idxs))):
        for j in range(len(dot_idxs)):
            if dot_idxs[j][1] >= block_idxs[i][1] and dot_idxs[j][0] < block_idxs[i][0]:
                for k in range(block_idxs[i][1]):
                    blocks[dot_idxs[j][0] + k], blocks[block_idxs[i][0] + k] = (
                        blocks[block_idxs[i][0] + k],
                        blocks[dot_idxs[j][0] + k],
                    )
                dot_idxs[j] = (dot_idxs[j][0] + block_idxs[i][1], dot_idxs[j][1] - block_idxs[i][1])
                break
    return sum([int(x) * int(y) for x, y in enumerate(blocks) if y != "."])


if __name__ == "__main__":
    input_str = get_input()
    print(part1(input_str))
    print(part2(input_str))
