
import main 
from util import *

class Graph(object): 
    
    def __init__(self, nodes0=set(), edges0=set()): 
        self.nodes = nodes0
        self.edges = edges0
        if main.DEBUG:
            for node1, node2 in edges0:
                assertion(node1 in self.nodes, 'Warning: '+str(node1)+' is in the initializing edge ('+str(node1)+', '+str(node2)+') but is not in the initializing nodes.')
                assertion(node2 in self.nodes, 'Warning: '+str(node2)+' is in the initializing edge ('+str(node1)+', '+str(node2)+') but is not in the initializing nodes.')
    
    def add_edge(self, node1, node2):
        self.edges.add((node1, node2))
    
    def add_node(node):
        self.nodes.add(node)

class Genome(object):
    
    def fill_edges(self):
        shuffled_edges = random.sample(self.graph.edges, len(self.graph.edges))
        for (node1,node2) in shuffled_edges:
            if node1 not in [e[0] for e in self.chosen_edges] and node2 not in [e[1] for e in self.chosen_edges]:
                self.chosen_edges.append((node1,node2))
        
    def __init__(self, dict_of_hosts0, dict_of_guests0, dict_of_host_spots0, dict_hosts_to_host_spots0, graph0, initial_edges=[]):
        self.dict_of_hosts=dict_of_hosts0
        self.dict_of_guests=dict_of_guests0
        self.dict_of_host_spots=dict_of_host_spots0
        self.dict_hosts_to_host_spots=dict_hosts_to_host_spots0
        self.graph=graph0 
        self.chosen_edges = list(initial_edges)
        self.fill_edges()
    
    def __repr__(self):
        ans = ''+ \
            '''Genome('''+ \
                '''dict_of_hosts0='''+self.dict_of_hosts.__repr__()+''', '''+ \
                '''dict_of_guests0='''+self.dict_of_guests.__repr__()+''', '''+ \
                '''dict_of_host_spots0='''+self.dict_of_host_spots.__repr__()+''', '''+ \
                '''graph0='''+self.graph.__repr__()+''', '''+ \
                '''initial_edges='''+self.chosen_edges.__repr__()+''', '''+ \
            ''')'''
        return ans
        
    def mutate(self):
        self.chosen_edges = random.sample(self.chosen_edges, len(self.chosen_edges)/2)
        self.fill_edges()
    
    def get_clone(self):
        return Genome(self.dict_of_hosts, self.dict_of_guests, self.dict_of_host_spots, self.graph, self.chosen_edges)
    
    def get_N_value(self):
        return len(self.chosen_edges)
    
    def get_P_value(self):
        P = 0
        dict_host_to_list_of_guest_id_nums = {}
        for host_id_num in self.dict_of_hosts.keys():
            dict_host_to_list_of_guest_id_nums[host_id_num] = []
        for host_spot_id_num, guest_id_num in self.chosen_edges:
            host_id_num = self.dict_of_host_spots[host_spot_id_num]
            dict_host_to_list_of_guest_id_nums[host_id_num].append(guest_id_num)
        for host_spot_id_num, guest_id_num in self.chosen_edges:
            host_id_num = self.dict_of_host_spots[host_spot_id_num]
            host = self.dict_of_hosts[host_id_num]
            host_name = host['first_name']+' '+host['last_name']
            host_prefers_these_housing_buddies = host["preferred_housing_buddies"]
            guest = self.dict_of_guests[guest_id_num]
            guest_name = guest['first_name']+' '+guest['last_name']
            guest_prefers_these_housing_buddies = guest["preferred_housing_buddies"]
            id_nums_of_all_guests_staying_with_host = dict_host_to_list_of_guest_id_nums[host_id_num]
            names_of_all_guests_staying_with_host = [self.dict_of_guests[g_id_num]['first_name']+' '+self.dict_of_guests[g_id_num]['last_name'] for g_id_num in id_nums_of_all_guests_staying_with_host]
            if host_name in guest_prefers_these_housing_buddies: # guest prefers host
                P += 1
            if guest_name in host_prefers_these_housing_buddies: # host prefers guest
                P += 1
            P += len(list_intersection(guest_prefers_these_housing_buddies, names_of_all_guests_staying_with_host)) # guest prefers guest
        return P
    
    def get_misc_info(self):
        ans = {}
        ans["P_value"] = self.get_P_value()
        ans["N_value"] = self.get_N_value()

        ans["host_actively_prefers_to_house_guest_of_a_different_gender"]=0
        ans["guest_actively_prefers_to_be_housed_with_host_of_a_different_gender"]=0
        ans["guest_actively_prefers_to_be_housed_with_coguest_of_a_different_gender"]=0
        ans["guest_CANNOT_get_needed_rides_from_host"]=0
        
        ans["host_guest_late_night_tendencies_match"]=0
        ans["host_guest_early_sleeper_some_late_night_mismatch"]=0
        ans["host_guest_early_sleeper_survivors_club_mismatch"]=0
        ans["host_guest_some_late_survivors_club_mismatch"]=0
        
        ans["coguest_late_night_tendencies_match"]=0
        ans["coguest_early_sleeper_some_late_night_mismatch"]=0
        ans["coguest_early_sleeper_survivors_club_mismatch"]=0
        ans["coguest_some_late_survivors_club_mismatch"]=0
        
        dict_host_to_list_of_guest_id_nums = {}
        for host_id_num in self.dict_of_hosts.keys():
            dict_host_to_list_of_guest_id_nums[host_id_num] = []
        for host_spot_id_num, guest_id_num in self.chosen_edges:
            host_id_num = self.dict_of_host_spots[host_spot_id_num]
            dict_host_to_list_of_guest_id_nums[host_id_num].append(guest_id_num)
        for host_spot_id_num, guest_id_num in self.chosen_edges:
            host_id_num = self.dict_of_host_spots[host_spot_id_num]
            host = self.dict_of_hosts[host_id_num]
            guest = self.dict_of_guests[guest_id_num]
            id_nums_of_all_guests_staying_with_host = dict_host_to_list_of_guest_id_nums[host_id_num]
            if (host["hosts_prefer_which_gender"]!=guest["gender"] and "Either"!=host["hosts_prefer_which_gender"]):
                ans["host_actively_prefers_to_house_guest_of_a_different_gender"]+=1
            if (guest["guests_prefer_which_gender"]!=host["gender"] and "Either"!=guest["guests_prefer_which_gender"]):
                ans["guest_actively_prefers_to_be_housed_with_host_of_a_different_gender"]+=1
            if not guest["has_ride"] and not host["willing_to_provide_rides"]: 
                ans["guest_CANNOT_get_needed_rides_from_host"]+=1
            # Late Night Tendencies Matching
            host_late_night_tendencies = host["late_night_tendencies"]
            guest_late_night_tendencies = guest["late_night_tendencies"]
            host_guest_late_night_tendencies_tuple = (host_late_night_tendencies, guest_late_night_tendencies)
            # guest host matching
            if host_late_night_tendencies == guest_late_night_tendencies:
                ans["host_guest_late_night_tendencies_match"]+=1
            if "early sleeper" in host_guest_late_night_tendencies_tuple:
                if "some late night" in host_guest_late_night_tendencies_tuple: 
                    ans["host_guest_early_sleeper_some_late_night_mismatch"]+=1
            if "survivors' club" in host_guest_late_night_tendencies_tuple: 
                if "early sleeper" in host_guest_late_night_tendencies_tuple:
                    ans["host_guest_early_sleeper_survivors_club_mismatch"]+=1
            if "some late night" in host_guest_late_night_tendencies_tuple:
                if "survivors' club" in host_guest_late_night_tendencies_tuple: 
                    ans["host_guest_some_late_survivors_club_mismatch"]+=1
            for g_id_num in id_nums_of_all_guests_staying_with_host:
                if g_id_num == guest_id_num:
                    continue
                # gender preferences
                coguest_gender = self.dict_of_guests[g_id_num]['gender']
                if guest["guests_prefer_which_gender"]!=coguest_gender and "Either"!=guest["guests_prefer_which_gender"]:
                    ans["guest_actively_prefers_to_be_housed_with_coguest_of_a_different_gender"]+=1
                # guest and co-guests matching
                other_guest_preference = self.dict_of_guests[g_id_num]["late_night_tendencies"]
                guest_other_guest_late_night_tendencies_tuple = (other_guest_preference, guest_late_night_tendencies)
                if other_guest_preference == guest_late_night_tendencies:
                    ans["coguest_late_night_tendencies_match"]+=1
                if "early sleeper" in guest_other_guest_late_night_tendencies_tuple:
                    if "some late night" in guest_other_guest_late_night_tendencies_tuple: 
                        ans["coguest_early_sleeper_some_late_night_mismatch"]+=1
                if "survivors' club" in guest_other_guest_late_night_tendencies_tuple: 
                    if "early sleeper" in guest_other_guest_late_night_tendencies_tuple:
                        ans["coguest_early_sleeper_survivors_club_mismatch"]+=1
                if "some late night" in guest_other_guest_late_night_tendencies_tuple:
                    if "survivors' club" in guest_other_guest_late_night_tendencies_tuple: 
                        ans["coguest_some_late_survivors_club_mismatch"]+=1
        return ans
        
def mate(parent_1, parent_2):
    child = Genome(parent_1.dict_of_hosts, parent_1.dict_of_guests, parent_1.dict_of_host_spots, parent_1.dict_hosts_to_host_spots, parent_1.graph, [])
    edges_1 = parent_1.chosen_edges
    edges_2 = parent_2.chosen_edges
    random.shuffle(edges_1)
    random.shuffle(edges_2)
    child.chosen_edges=[]
    starting_index_1=0
    starting_index_2=0
    while starting_index_1<len(edges_1)-1 or starting_index_2<len(edges_2)-1:
        for i, edge in enumerate(edges_1[starting_index_1:]):
            if edge[0] not in [e[0] for e in child.chosen_edges] and edge[1] not in [e[1] for e in child.chosen_edges]:
                child.chosen_edges.append(edge)
                print "edge from parent 1", edge
                break
        starting_index_1+=1+i
        for i, edge in enumerate(edges_2[starting_index_2:]):
            if edge[0] not in [e[0] for e in child.chosen_edges] and edge[1] not in [e[1] for e in child.chosen_edges]:
                child.chosen_edges.append(edge)
                print "edge from parent 2", edge
                break
        starting_index_2+=1+i
    child.fill_edges()
    return child

def are_compatible(host,guest):
    local_debug=False
    def local_debug_print(text):
        if local_debug:
            print text
    if not main.EVENT_WE_ARE_HOUSING_FOR in host["events_doing_housing"]:
        local_debug_print('EVENT1')
        return False
    if not main.EVENT_WE_ARE_HOUSING_FOR in guest["events_needing_housing"]:
        local_debug_print('EVENT2')
        return False
    if not guest["days_housing_is_needed"].issubset(host["days_housing_is_available"]):
        local_debug_print('DAYS')
        return False
    if host["has_cats"]:
        if not guest["can_be_around_cats"]:
            local_debug_print('CATS')
            return False
    if host["has_dogs"]:
        if not guest["can_be_around_dogs"]:
            local_debug_print('DOGS')
            return False
    if guest["smokes"]: 
        if not host["willing_to_house_smokers"]:
            local_debug_print('SMOKING')
            return False
    return True

class GeneticAlgorithm(object):
    
    def __init__(self, dict_of_hosts0, dict_of_guests0, dict_of_host_spots0, dict_hosts_to_host_spots0, population_size0, tournament_size0, elite_percent0, mate_percent0, mutation_percent0, genomes_list0=[]):
        self.dict_of_hosts = dict_of_hosts0
        self.dict_of_guests = dict_of_guests0
        self.dict_of_host_spots = dict_of_host_spots0
        self.dict_hosts_to_host_spots = dict_hosts_to_host_spots0
        self.population_size = population_size0
        self.tournament_size = tournament_size0
        self.elite_percent = elite_percent0
        self.mate_percent = mate_percent0
        self.mutation_percent = mutation_percent0
        
        self.graph = Graph(nodes0=self.dict_of_host_spots.keys()+self.dict_of_guests.keys())
        for host_spot_id_num, host_id_num in self.dict_of_host_spots.items():
            host = self.dict_of_hosts[host_id_num]
            for guest_id_num, guest in self.dict_of_guests.items():
                if are_compatible(host,guest):
                    self.graph.add_edge(host_spot_id_num,guest_id_num) # Edges are stored in (host_spot_id_num, guest_id_num) order
        
        genomes_list = [Genome(self.dict_of_hosts, self.dict_of_guests, self.dict_of_host_spots, self.dict_hosts_to_host_spots, self.graph) for _ in xrange(self.population_size-len(genomes_list0))]+genomes_list0
        self.genomes_and_scores_list = [(g, g.get_N_value(), g.get_P_value()) for g in genomes_list]
    
    def run_for_x_generations(self, num_generations=1):
        for generation_index in xrange(num_generations):
            num_new_elites = int(self.elite_percent*self.population_size)
            num_new_children = int(self.mate_percent*self.population_size)
            num_new_mutations = int(self.mutation_percent*self.population_size)
            
            new_genomes_and_scores_list = []
            for e in random.sample(self.genomes_and_scores_list, num_new_mutations):
                mutation = e[0].clone()
                mutation.mutate()
                new_genomes_and_scores_list.append((mutation,mutation.get_N_value(),mutation.get_P_value()))
            for _ in xrange(num_new_children):
                parents_and_scores = random.sample(self.genomes_and_scores_list, 2)
                parent_1 = parents_and_scores[0][0]
                parent_2 = parents_and_scores[1][0]
                child = mate(parent_1, parent_2)
                new_genomes_and_scores_list.append((child, child.get_N_value(), child.get_P_value()))
            self.genomes_and_scores_list.sort(key=lambda x:-x[0]) # now sorted from biggest to smallest N
            num_genomes_with_pareto_score=0
            current_pareto_score=0
            prev_P = -inf
            while num_genomes_with_pareto_score<len(self.genomes_and_scores_list): # Get Pareto Scores 
                for index in enumerate(self.genomes_and_scores_list):
                    # We store the pareto score in the 4th box of the tuple
                    if len(genome_and_scores)>3:
                        continue
                    genome_and_scores[index]
                    genome = genome_and_scores[0]
                    current_N = genome_and_scores[1]
                    current_P = genome_and_scores[2]
                    if current_P >= prev_P:
                        prev_P = current_P
                        self.genomes_and_scores_list[index] = (genome, current_N, current_P, current_pareto_score) 
                        num_genomes_with_pareto_score+=1
                current_pareto_score+=1
            for _ in xrange(num_new_elites):
                tournament_indices = random.sample(range(len(self.genomes_and_scores_list)), min(self.tournament_size, len(self.genomes_and_scores_list)))
                tournament_winner, tournament_winner_index = max(([self.genomes_and_scores_list[i],i) for i in tournament_indices], lambda x:x[0][3])
                new_genomes_and_scores_list.append(self.genomes_and_scores_list.pop(tournament_winner_index)[:3])
            while len(new_genomes_and_scores_list) < self.population_size: 
                # we're going to add random genomes until we meet the population size
                new_genome = new_genomes_and_scores_list[0][0].get_clone()
                new_genome.chosen_edges = []
                new_genome.fill_edges()
                new_genomes_and_scores_list.append((new_genome, new_genome.get_N_value(), new_genome.get_P_value()))
            self.genomes_and_scores_list = new_genomes_and_scores_list
        
    def __repr__(self):
        ans = ''+ \
            '''GeneticAlgorithm('''+ \
                '''dict_of_hosts0='''+self.dict_of_hosts.__repr__()+''', '''+ \
                '''dict_of_guests0='''+self.dict_of_guests.__repr__()+''', '''+ \
                '''dict_of_host_spots0='''+self.dict_of_host_spots.__repr__()+''', '''+ \
                '''population_size0='''+self.population_size.__repr__()+''', '''+ \
                '''tournament_size0='''+self.tournament_size.__repr__()+''', '''+ \
                '''elite_percent0='''+self.elite_percent.__repr__()+''', '''+ \
                '''mate_percent0='''+self.mate_percent.__repr__()+''', '''+ \
                '''mutation_percent0='''+self.mutation_percent.__repr__()+''', '''+ \
                '''graph0='''+self.graph.__repr__()+''', '''+ \
                '''genomes_list0='''+([e[0] for e in self.self.genomes_and_scores_list]).__repr__()+''', '''+ \
            ''')'''
        return ans

