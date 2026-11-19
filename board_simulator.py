import random
from card_data import chance_cards, community_chest_cards

def passed_go(p_initial, p_final):
    return p_final < p_initial

def simulate_monopoly(num_turns=100000):

    position = 0 
    times_passed_go = 0
    landing_counts = [0] * 40
    jail_visits = 0
    in_jail = False
    jail_turns = 0
    consecutive_doubles = 0
    triple_doubles_jail = 0
    escaped_jail = False
    total_rolls = 0
    chance_spaces = [7, 22, 36]
    community_chest_spaces = [2, 17, 33]




    for turn in range(num_turns):
        consecutive_doubles = 0

        while True:
            die1 = random.randint(1, 6)
            die2 = random.randint(1, 6)
            total_rolls += 1

            roll = die1 + die2
            is_double = die1 == die2
            escaped_jail = False

            # Step 1: Handle jail
            if in_jail:
                jail_turns += 1

                if is_double:
                    in_jail = False
                    jail_turns = 0
                    escaped_jail = True

                elif jail_turns == 3:
                    in_jail = False
                    jail_turns = 0
                    escaped_jail = True

                else:
                    break

            # Step 2: Track doubles during normal play
            if not escaped_jail:
                if is_double:
                    consecutive_doubles += 1
                else:
                    consecutive_doubles = 0

            # Step 3: Three doubles sends player to jail
            if consecutive_doubles == 3:
                triple_doubles_jail += 1
                jail_visits += 1

                position = 10
                in_jail = True
                jail_turns = 0

                landing_counts[10] += 1
                break

            # Step 4: Move around the board
            if position + roll >= 40:
                times_passed_go += 1

            position = (position + roll) % 40

            # Step 5: Go To Jail
            if position == 30:
                position = 10
                in_jail = True
                jail_turns = 0
                jail_visits += 1

                landing_counts[10] += 1
                break
            
            # Chance Cards
            if position in chance_spaces:
                card = random.choice(chance_cards)
                if card == "Advance to GO":
                    position = 0
                    times_passed_go += 1

                elif card == "Go to Jail":
                    position = 10
                    in_jail = True
                    jail_turns = 0
                    jail_visits += 1
                    landing_counts[10] += 1
                    break

                elif card == "Advance to Illinois Avenue":
                    if passed_go(position, 24):
                        times_passed_go += 1
                    position = 24

                elif card == "Advance to Boardwalk":
                    position = 39

                elif card == "Advance to St. Charles Place":
                    if passed_go(position, 11):
                        times_passed_go += 1
                    position = 11

                elif card == "Advance to Reading Railroad":
                    if passed_go(position, 5):
                        times_passed_go += 1
                    position = 5

                elif card == "Advance to Nearest Railroad":
                    railroads = [5, 15, 25, 35]
                    destination = next(
                        (r for r in railroads if r > position),
                        railroads[0]
                    )

                    if passed_go(position, destination):
                        times_passed_go += 1
                    position = destination

                elif card == "Advance to Nearest Utility":
                    utilities = [12, 28]
                    destination = next(
                        (u for u in utilities if u > position),
                        utilities[0]
                    )

                    if passed_go(position, destination):
                        times_passed_go += 1
                    position = destination

                elif card == "Go Back 3 Spaces":
                    position = (position - 3) % 40

                    
                # "No Movement" cards leave position unchanged

            #Community Chest Cards
            
            if position in community_chest_spaces:
                card = random.choice(community_chest_cards)

                if card == "Advance to GO":
                    position = 0
                    times_passed_go += 1

                elif card == "Go to Jail":
                    position = 10
                    in_jail = True
                    jail_turns = 0
                    jail_visits += 1
                    landing_counts[10] += 1
                    break

        
            landing_counts[position] += 1

            # Step 6: Decide whether the turn ends
            if escaped_jail or not is_double:
                break

    return {
    "landing_counts": landing_counts,
    "times_passed_go": times_passed_go,
    "jail_visits": jail_visits,
    "triple_doubles_jail": triple_doubles_jail,
    "total_rolls": total_rolls,
    "num_turns": num_turns
    }
            

if __name__ == "__main__":
    random.seed(422)
    results = simulate_monopoly(100000)
    print("Total turns:", results["num_turns"])
    print("Total rolls:", results["total_rolls"])
    print("Jail visits:", results["jail_visits"])
    print("Recorded landings:", sum(results["landing_counts"]))