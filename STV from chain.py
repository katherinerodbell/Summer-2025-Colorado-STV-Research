from votekit.elections import STV
from votekit.cleaning import remove_and_condense
from votekit.ballot import Ballot
from votekit.pref_profile import PreferenceProfile
from votekit.pref_profile import profile_df_head
import votekit.ballot_generator as bg
from votekit import PreferenceInterval
import random

#start check
print("starting…")

#reads csv

dem_read = open('dem_results.csv','r')
new_dem_list = dem_read.readlines()

rep_read = open('rep_results.csv','r')
new_rep_list = rep_read.readlines()

#splits and cleans csv

new_dem_list = str(new_dem_list)
split_dem_list = new_dem_list.split(',')
clean_split_dem_list = []
for i in split_dem_list:
    clean_i = i.replace("[","").replace("]","").replace("'","").replace(" ","").replace("Dempop:","")
    clean_split_dem_list.append(clean_i)
    
new_rep_list = str(new_rep_list)
split_rep_list = new_rep_list.split(',')
clean_split_rep_list = []
for i in split_rep_list:
    clean_i = i.replace("[","").replace("]","").replace("'","").replace(" ","").replace("Reppop:","")
    clean_split_rep_list.append(clean_i)

#creates dictionary from csv

democrat_dict = {}

for i in range(0,10000): #change based on number of steps
    district_dict = {8:0,9:0,11:0,12:0,2:0,5:0,4:0,10:0,6:0,7:0,1:0,3:0,13:0}
    democrat_dict[i] = district_dict
    democrat_dict[i][8] = clean_split_dem_list[2][2:]
    democrat_dict[i][9] = clean_split_dem_list[3][2:]
    democrat_dict[i][11] = clean_split_dem_list[4][3:]
    democrat_dict[i][12] = clean_split_dem_list[5][3:]
    democrat_dict[i][2] = clean_split_dem_list[6][2:]
    democrat_dict[i][5] = clean_split_dem_list[7][2:]
    democrat_dict[i][4] = clean_split_dem_list[8][2:]
    democrat_dict[i][10] = clean_split_dem_list[9][3:]
    democrat_dict[i][6] = clean_split_dem_list[10][2:]
    democrat_dict[i][7] = clean_split_dem_list[11][2:]
    democrat_dict[i][1] = clean_split_dem_list[12][2:]
    democrat_dict[i][3] = clean_split_dem_list[13][2:]
    democrat_dict[i][13] = clean_split_dem_list[14][3:]
    del clean_split_dem_list[0:15]
    
republican_dict = {}

for i in range(0,10000): #change based on number of steps
    district_dict = {8:0,9:0,11:0,12:0,2:0,5:0,4:0,10:0,6:0,7:0,1:0,3:0,13:0}
    republican_dict[i] = district_dict
    republican_dict[i][8] = clean_split_rep_list[2][2:]
    republican_dict[i][9] = clean_split_rep_list[3][2:]
    republican_dict[i][11] = clean_split_rep_list[4][3:]
    republican_dict[i][12] = clean_split_rep_list[5][3:]
    republican_dict[i][2] = clean_split_rep_list[6][2:]
    republican_dict[i][5] = clean_split_rep_list[7][2:]
    republican_dict[i][4] = clean_split_rep_list[8][2:]
    republican_dict[i][10] = clean_split_rep_list[9][3:]
    republican_dict[i][6] = clean_split_rep_list[10][2:]
    republican_dict[i][7] = clean_split_rep_list[11][2:]
    republican_dict[i][1] = clean_split_rep_list[12][2:]
    republican_dict[i][3] = clean_split_rep_list[13][2:]
    republican_dict[i][13] = clean_split_rep_list[14][3:]
    del clean_split_rep_list[0:15]

results_dict = {}

#creates outer loop that runs through steps
for key in range(0,1): #change to steps you want to run
    results_dict[key] = {"D": 0, "R": 0}
    winner_dict = {"D": 0, "R": 0}
    dem_multi_dict = {'8': int(democrat_dict[key][8]), '9': int(democrat_dict[key][9]), '11': int(democrat_dict[key][11]), '12': int(democrat_dict[key][12]), '2': int(democrat_dict[key][2]), '5': int(democrat_dict[key][5]), '4': int(democrat_dict[key][4]), '10': int(democrat_dict[key][10]), '6': int(democrat_dict[key][6]), '7': int(democrat_dict[key][7]), '1': int(democrat_dict[key][1]), '3': int(democrat_dict[key][3]), '13':int(democrat_dict[key][13])}
    rep_multi_dict = {'8': int(republican_dict[key][8]), '9': int(republican_dict[key][9]), '11': int(republican_dict[key][11]), '12': int(republican_dict[key][12]), '2': int(republican_dict[key][2]), '5': int(republican_dict[key][5]), '4': int(republican_dict[key][4]), '10': int(republican_dict[key][10]), '6': int(republican_dict[key][6]), '7': int(republican_dict[key][7]), '1': int(republican_dict[key][1]), '3': int(republican_dict[key][3]), '13':int(republican_dict[key][13])}
#creates inner loop that runs through districts   
    for i in range(1,14):
        winner_list = []
        num_dem_votes = dem_multi_dict[str(i)]
        num_rep_votes = rep_multi_dict[str(i)]
        total_votes = num_dem_votes + num_rep_votes
        prop_dem_votes = num_dem_votes/total_votes 
        prop_rep_votes = num_rep_votes/total_votes
        prop_dem_seats = round(5*(prop_dem_votes))
        prop_rep_seats = round(5*(prop_rep_votes))
        num_dem_can = prop_dem_seats+2
        num_rep_can = prop_rep_seats+2
        dem_can_list = []
        rep_can_list = []
        for x in range(0, num_dem_can):
            dem_can_list.append('D'+str(x))
        for y in range(0, num_rep_can):
            rep_can_list.append('R'+str(y))

        #Set parameters:
        slate_to_candidates = {"Dems": dem_can_list, "Reps": rep_can_list}

        alphas = {"Dems": {"Dems": 1, "Reps": 1}, "Reps": {"Dems": 1, "Reps": 1}}

        bloc_voter_prop = {"Dems": prop_dem_votes, "Reps": prop_rep_votes }

        cohesion_parameters = {"Dems": {"Dems":0.93, "Reps":0.07}, "Reps": {"Reps":0.88, "Dems":0.12},}

        number_of_ballots = total_votes

        #Create ballots:
        pl = bg.slate_PlackettLuce.from_params(
            slate_to_candidates=slate_to_candidates,
            bloc_voter_prop=bloc_voter_prop,
            cohesion_parameters=cohesion_parameters,
            alphas=alphas,
        )

        profile_dict, agg_profile = pl.generate_profile(number_of_ballots=number_of_ballots, by_bloc=True)

        orig_profile = agg_profile

        #Truncate Ballots (ADD YOUR PATH TO DESKTOP AND STEP NUMBERS)
        write_file = open(‘DESKTOP\\PATH\\HERE\\pref_prof_STEP_NUMBER.csv', 'w')
        write_file.write(orig_profile.df.to_string())

        read_file = open(‘DESKTOP\\PATH\\HERE\\pref_prof_STEP_NUMBER.csv', 'r')
        pref_prof_list = read_file.readlines()
       
        no_spaces = []
        for item in pref_prof_list:
            no_n = item.strip()
            no_spaces_item = no_n.replace(" ", "")
            no_spaces.append(no_spaces_item)

        del no_spaces[0:2]


        ballots_before = []
        for item in no_spaces:
            #clean it to be just candidates
            beg_specific_char = "("
            new_index = item.find(beg_specific_char)
            if new_index != -1:  
                beg_result_string = item[new_index +1 :] 
            end_specific_char = "{"
            end_index = beg_result_string.find(end_specific_char)
            if end_index != -1:  
                end_result_string = beg_result_string[:end_index-1] 
            
            #make ballot a list
            ballot = [f'({j})' for j in end_result_string.strip().split(')(')]
            cleaned_ballot = [item.strip('()') for item in ballot]

            #define weight
            weight = item.split('}')[-1]  
            int_weight = int(float(weight))

            #make list of ballots
            for z in range(0, int_weight):
                ballots_before.append(cleaned_ballot)
      

        truncated_ballots_list = []
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        probabilities = [.10, .08, .19, .16, .24, .07, .03, .02, .11] 

        for item in ballots_before:
            ballot_length = random.choices(values, weights=probabilities, k=1)[0]
            truncated_ballot = item[:ballot_length]
            truncated_ballots_list.append(truncated_ballot)
       
        ballots = []
        for item in truncated_ballots_list:
            ranking = [{candidate} for candidate in item]
            ballot = Ballot(ranking=ranking)
            ballots.append(ballot)

        profile = PreferenceProfile(ballots=ballots)

        #Run STV:
        print('Running election...')
        election = STV(profile=profile, m=5)
        
        #Display results better
        district_winner_dict = {"D": 0, "R": 0}

        winner_list = []
        winner_list.extend(election.get_elected(-1))
        winner_string = str(winner_list)

        candidate_list = []
        candidate_list.extend(dem_can_list)
        candidate_list.extend(rep_can_list)
        
        clean_winner_list = []
        for candidate in candidate_list:
            if candidate in winner_string:
                clean_winner_list.append(candidate)

        for winner in clean_winner_list:
            if winner[0] == 'D':
                district_winner_dict["D"] += 1
            if winner[0] == 'R':
                district_winner_dict["R"] += 1


        winner_dict["D"]+=district_winner_dict["D"]
        winner_dict["R"]+=district_winner_dict["R"]
        
        results_dict[key]["D"] = winner_dict["D"]
        results_dict[key]["R"] = winner_dict["R"]
        
        print("Step",key,":")
        print("District", i,":")
        print("Winners from district:", district_winner_dict)
        print("Winners from map:", winner_dict)
        print()
        print(election)
        print()
        
    print(results_dict)