"""A script for determining perfect MapleStory node combinations."""

import csv


def find_combinations(index, combo, count):
    if count == len(targets):
        combinations.append(combo)
        counts.append(dict(targets))
    elif index < len(nodes) and len(combo) < MAX_NODES:
        curr = nodes[index]

        # Don't use curr
        find_combinations(index + 1, combo, count)

        # Use curr if its leader hasn't been used already
        if curr[0] not in leaders:
            leaders.add(curr[0])
            for skill in curr:
                if skill in targets:
                    targets[skill] += 1
                    if targets[skill] == 2:
                        count += 1

            find_combinations(index + 1, combo + [curr], count)

            leaders.remove(curr[0])
            for skill in curr:
                if skill in targets:
                    targets[skill] -= 1


targets = {}
nodes = set()
with open('data.csv', newline='') as file:
    csv_reader = csv.reader(file)
    for i, row in enumerate(csv_reader):
        temp = []       # Clean up skill names
        for s in row:
            cleaned = s.lower().strip()
            if cleaned:
                temp.append(cleaned)
        row = temp

        if i == 0:              # Read target skills from first line
            targets = {s: 0 for s in row}
        elif len(row) == 3:     # Read node
            t1 = tuple(row)
            t2 = (row[0], row[2], row[1])
            if t1 not in nodes and t2 not in nodes:
                nodes.add(t1)
        elif len(row) != 0:
            print(f' !  Invalid number of skills on line {i+1}.')

MAX_NODES = (len(targets) * 2 + 2) // 3
nodes = list(nodes)
leaders = set()
combinations = []
counts = []

print(f"[~] Looking to satisfy: {', '.join(targets.keys())}")
find_combinations(0, [], 0)

print(f"[~] Found {len(combinations)} combination(s):")
for i in range(len(combinations)):
    info = ', '.join([f'{k}: {v}' for k, v in counts[i].items()])
    print(f' ~  Combination {i+1}:    {{{info}}}')
    for n in combinations[i]:
        print(f"     -  {', '.join(n)}")
    if i != len(combinations) - 1:
        print()
