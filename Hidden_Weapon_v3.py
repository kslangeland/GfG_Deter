import gambit
import csv
import pandas as pd
import numpy as np

solver = gambit.nash.ExternalEnumPureSolver()
results = []

with open("hidden_weapon_input.csv") as csvfile:
	reader = csv.reader(csvfile)
	i = 1
	for row in reader:
		if i != 1:
			chance_high = int(row[0])
			chance_high_denom = int(row[1])
			blue_start = int(row[2])
			red_start = int(row[3])
			blue_change_weapon = int(row[4])
			blue_change_noweapon = int(row[5])
			red_dev_cost = int(row[6])
			blue_signal_cost = int(row[7])
			blue_chance_weapon = int(row[8])
			blue_chance_weapon_denom = int(row[9])
			blue_chance_noweapon = int(row[10])
			blue_chance_noweapon_denom = int(row[11])
			conflict_cost = int(row[12])
			win_value = int(row[13])

			game = gambit.Game.new_tree()
			game.title = "Hidden Weapon"

			Blue = game.players.add("Blue")
			Red = game.players.add("Red")

			weapon_signal_accept = game.outcomes.add("Weapon Signal Accept")
			weapon_signal_accept[0] = blue_start + blue_change_weapon - blue_signal_cost - red_start
			weapon_signal_accept[1] = red_start - blue_start - blue_change_weapon

			weapon_nosignal_accept = game.outcomes.add("Weapon No Signal Accept")
			weapon_nosignal_accept[0] = blue_start + blue_change_weapon - red_start
			weapon_nosignal_accept[1] = red_start - blue_start - blue_change_weapon

			noweapon_signal_accept = game.outcomes.add("No Weapon Signal Accept")
			noweapon_signal_accept[0] = blue_start - (blue_signal_cost / 2) - red_start + blue_change_noweapon
			noweapon_signal_accept[1] = red_start - blue_start

			noweapon_nosignal_accept = game.outcomes.add("No Weapon No Signal Accept")
			noweapon_nosignal_accept[0] = blue_start - red_start + blue_change_noweapon
			noweapon_nosignal_accept[1] = red_start - blue_start

			blue_wins_weapon_signal = game.outcomes.add("Blue Wins Weapon Signal")
			blue_wins_weapon_signal[0] = win_value - blue_signal_cost - conflict_cost
			blue_wins_weapon_signal[1] = 0 - conflict_cost

			blue_wins_weapon_nosignal = game.outcomes.add("Blue Wins Weapon No Signal")
			blue_wins_weapon_nosignal[0] = win_value - conflict_cost
			blue_wins_weapon_nosignal[1] = 0 - conflict_cost

			blue_wins_noweapon_signal = game.outcomes.add("Blue Wins No Weapon Signal")
			blue_wins_noweapon_signal[0] = win_value - blue_signal_cost / 2 - conflict_cost
			blue_wins_noweapon_signal[1] = 0 - conflict_cost

			blue_wins_noweapon_nosignal = game.outcomes.add("Blue Wins No Weapon No Signal")
			blue_wins_noweapon_nosignal[0] = win_value - conflict_cost
			blue_wins_noweapon_nosignal[1] = 0 - conflict_cost

			red_wins_weapon_signal = game.outcomes.add("Red Wins Weapon Signal")
			red_wins_weapon_signal[0] = 0 - conflict_cost - blue_signal_cost
			red_wins_weapon_signal[1] = win_value - conflict_cost

			red_wins_weapon_nosignal = game.outcomes.add("Red Wins Weapon No Signal")
			red_wins_weapon_nosignal[0] = 0 - conflict_cost
			red_wins_weapon_nosignal[1] = win_value - conflict_cost

			red_wins_noweapon_signal = game.outcomes.add("Red Wins No Weapon Signal")
			red_wins_noweapon_signal[0] = 0 - conflict_cost - blue_signal_cost / 2
			red_wins_noweapon_signal[1] = win_value - conflict_cost

			red_wins_noweapon_nosignal = game.outcomes.add("Red Wins No Weapon No Signal")
			red_wins_noweapon_nosignal[0] = 0 - conflict_cost
			red_wins_noweapon_nosignal[1] = win_value - conflict_cost

			move = game.root.append_move(game.players.chance, 2)
			move.actions[0].label = "weapon"
			move.actions[0].prob = gambit.Rational(chance_high, chance_high_denom)
			move.actions[1].label = "no weapon"
			move.actions[1].prob = gambit.Rational(chance_high_denom - chance_high, chance_high_denom)

			#weapon branch
			wmove = game.root.children[0].append_move(Blue, 2)
			wmove.label = "send signal?"
			wmove.actions[0].label = "signal"
			wmove.actions[1].label = "no signal"

			#no weapon branch
			nmove = game.root.children[1].append_move(Blue, 2)
			nmove.label = "send signal?"
			nmove.actions[0].label = "signl"
			nmove.actions[1].label = "no signal"

			#sees signal
			move = game.root.children[0].children[0].append_move(Red, 2)
			move.actions[0].label = "accept"
			move.actions[1].label = "aggresive posture"
			game.root.children[1].children[0].append_move(move)

			#doesn't see signal
			move = game.root.children[0].children[1].append_move(Red, 2)
			move.actions[0].label = "accept"
			move.actions[1].label = "aggressive posture"
			game.root.children[1].children[1].append_move(move)

			#signal and weapon
			move = game.root.children[0].children[0].children[1].append_move(game.players.chance, 2)
			move.actions[0].label = "blue wins"
			move.actions[0].prob = gambit.Rational(blue_chance_weapon, blue_chance_weapon_denom)
			move.actions[0].label = "red wins"
			move.actions[0].prob = gambit.Rational(blue_chance_weapon_denom - blue_chance_weapon, blue_chance_weapon_denom)

			#no signal and weapon
			move = game.root.children[0].children[1].children[1].append_move(game.players.chance, 2)
			move.actions[0].label = "blue wins"
			move.actions[0].prob = gambit.Rational(blue_chance_weapon, blue_chance_weapon_denom)
			move.actions[0].label = "red wins"
			move.actions[0].prob = gambit.Rational(blue_chance_weapon_denom - blue_chance_weapon, blue_chance_weapon_denom)

			#signal and no weapon
			move = game.root.children[1].children[0].children[1].append_move(game.players.chance, 2)
			move.actions[0].label = "blue wins"
			move.actions[0].prob = gambit.Rational(blue_chance_noweapon, blue_chance_noweapon_denom)
			move.actions[0].label = "red wins"
			move.actions[0].prob = gambit.Rational(blue_chance_noweapon_denom - blue_chance_noweapon, blue_chance_noweapon_denom)

			#no signal and no weapon
			move = game.root.children[1].children[1].children[1].append_move(game.players.chance, 2)
			move.actions[0].label = "blue wins"
			move.actions[0].prob = gambit.Rational(blue_chance_noweapon, blue_chance_noweapon_denom)
			move.actions[0].label = "red wins"
			move.actions[0].prob = gambit.Rational(blue_chance_noweapon_denom - blue_chance_noweapon, blue_chance_noweapon_denom)


			game.root.children[0].children[0].children[0].outcome = weapon_signal_accept
			game.root.children[0].children[1].children[0].outcome = weapon_nosignal_accept
			game.root.children[1].children[0].children[0].outcome = noweapon_signal_accept
			game.root.children[1].children[1].children[0].outcome = noweapon_nosignal_accept
			game.root.children[0].children[0].children[1].children[0].outcome = blue_wins_weapon_signal
			game.root.children[0].children[0].children[1].children[1].outcome = red_wins_weapon_signal
			game.root.children[0].children[1].children[1].children[0].outcome = blue_wins_weapon_nosignal
			game.root.children[0].children[1].children[1].children[1].outcome = red_wins_weapon_nosignal
			game.root.children[1].children[0].children[1].children[0].outcome = blue_wins_noweapon_signal
			game.root.children[1].children[0].children[1].children[1].outcome = red_wins_noweapon_signal
			game.root.children[1].children[1].children[1].children[0].outcome = blue_wins_noweapon_nosignal
			game.root.children[1].children[1].children[1].children[1].outcome = red_wins_noweapon_nosignal
			

			print(game.write())
			#solver = gambit.nash.ExternalEnumMixedSolver()
			#solution = solver.solve(game)
			solution = gambit.nash.lcp_solve(game)
			#print(len(solution))
			print(blue_change_weapon)
			print(blue_signal_cost)
			for el in solution:
				found = False
				if not found and el[game.players["Blue"].infosets[0].actions[0]] != el[game.players["Blue"].infosets[1].actions[0]]:
					print(el)
					print(el[game.players["Red"]])
					print(el.payoff(game.players["Red"]))
					print(el[game.players["Blue"]])
					print(el.payoff(game.players["Blue"]))
					results.append({"Signal Cost":blue_signal_cost,
						"Weapon Value":blue_change_weapon,
						"Prob Red Develops":float(el[game.players["Red"].infosets[0].actions[1]])# + el[game.players["Red"].infosets[1].actions[0]] 
						})
					found = True
				elif found:
					print("multiple semi-pooling equilibrium ignored")
				else:
					print("pass")
					#results.append({"Signal Cost":blue_signal_cost,
					#	"Weapon Value":blue_change_weapon,
					#	"Prob Red Develops":0
					#	})
			print("-------------------------------------------------\n")
		i = i + 1

df = pd.DataFrame(results)
print(df)
df.to_csv("results.csv")