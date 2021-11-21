import re

def open_file():
    try:
        return open("lab3.txt")
    except FileNotFoundError:
        print("Oops! File not exist...")
        exit()


def borda(data, benefits):
    result = {"sum": {}, "note": {}}
    for benefit in benefits:
        result["sum"][benefit] = 0
        result["note"][benefit] = ""

    for benefit in benefits:
        for line in data:
            votes = line[0]
            position = line[1].index(benefit)
            line_length = len(line[1])
            result["note"][benefit] += votes + "*" + str(line_length - position) + "+"
            result["sum"][benefit] += (line_length - position) * int(votes)
        result["note"][benefit] = result["note"][benefit][:-1]

    places = []
    for count in sorted(result["sum"], key=result["sum"].get, reverse=True):
        places.append(count)

    return {'places': places, 'sum': result['sum'], 'note': result['note']}


def condorcet(data, benefits):
    votes = {}

    for benefit in benefits:
        for line in data:
            electorate = line[0]
            for candidate in line[1]:
                if candidate == benefit: continue
                if line[1].index(candidate) > line[1].index(benefit): continue

                key = candidate + '>' + benefit
                votes[key] = int(electorate) if key not in votes else votes[key] + int(electorate)

    print("Comparison of votes:", votes)

    final_eloctorates = {}
    benefits_first_place = {}
    for benefit in benefits:
        benefits_first_place[benefit] = 0

    for result in votes:
        candidates = re.split('>', result)
        largest_candidate = candidates if votes[result] > votes[candidates[1] + '>' + candidates[0]] else [candidates[1], candidates[0]]
        key = largest_candidate[0] + '>' + largest_candidate[1]
        final_eloctorates[key] = votes[key]
    print("The following decisions remain:", final_eloctorates)

    for e in final_eloctorates.keys():
        candidates = re.split('>', e)
        if candidates[0] not in benefits_first_place: continue

        benefits_first_place[candidates[0]] += 1

    places = []
    for count in sorted (benefits_first_place, key = benefits_first_place.get, reverse=True):
        places.append(count)

    return { 'places': places, 'final_eloctorates': final_eloctorates }


file = open_file()
lines = []
benefits = []

for line in file:
    if (not (line and not line.isspace())): continue
    row = re.split(';', re.sub('\n', '', line))
    new_benefits = re.split(',', row[1])
    for benefit in new_benefits:
        if benefit not in benefits: benefits.append(benefit)

    lines.append([row[0], new_benefits])

print("Data:")
for line in lines: print(line)

print("\nCondorcet method:")
condorcet_result = condorcet(lines, benefits)
print("So:", ">".join(condorcet_result["places"]))

print("\nBorda method:")
borda_result = borda(lines, benefits)
print("Calculations:")
for note in borda_result['note'].keys():
    print(note, ": ", borda_result["note"][note], " = ", borda_result["sum"][note])
print("So:", ">".join(condorcet_result["places"]))