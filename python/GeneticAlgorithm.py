
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
        random.shuffle(self.chosen_edges)
        self.chosen_edges = self.chosen_edges[:len(self.chosen_edges)/2]
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
            genders_of_all_guests_staying_with_host = [self.dict_of_guests[g_id_num]['gender'] for g_id_num in id_nums_of_all_guests_staying_with_host]
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
        ans["host_actively_prefers_gender_of_guest"]=0
        ans["guest_actively_prefers_gender_of_coguests"]=0
        ans["guest_can_get_needed_rides_from_host"]=0
        
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
            genders_of_all_guests_staying_with_host = [self.dict_of_guests[g_id_num]['gender'] for g_id_num in id_nums_of_all_guests_staying_with_host]
            # If a person prefers either, then the person doesn't ACTIVELY prefer any gender
            if (host["hosts_prefer_which_gender"]==guest["gender"]):
                ans["host_actively_prefers_gender_of_guest"]+=1
            for coguest_gender in genders_of_all_guests_staying_with_host:
                if guest["guests_prefer_which_gender"]==coguest_gender:
                    ans["guest_actively_prefers_gender_of_coguests"]+=1
            if host["willing_to_provide_rides"] and not guest["has_ride"]: 
                # True only if the guest ACTIVELY NEEDS a ride and host can provide rides
                ans["guest_can_get_needed_rides_from_host"]+=1
            # Late Night Tendencies Matching
            host_late_night_tendencies = host["late_night_tendencies"]
            guest_late_night_tendencies = guest["late_night_tendencies"]
            if host_late_night_tendencies == guest_late_night_tendencies:
                ans["host_guest_late_night_tendencies_match"]+=1
            if "early sleeper" in (host_late_night_tendencies, guest_late_night_tendencies):
                if "some late night" in (host_late_night_tendencies, guest_late_night_tendencies): 
                    ans["host_guest_early_sleeper_some_late_night_mismatch"]+=1
            if "survivors' club" in (host_late_night_tendencies, guest_late_night_tendencies): 
                if "early sleeper" in (host_late_night_tendencies, guest_late_night_tendencies):
                    ans["host_guest_early_sleeper_survivors_club_mismatch"]+=1
            if "some late night" in (host_late_night_tendencies, guest_late_night_tendencies):
                if "survivors' club" in (host_late_night_tendencies, guest_late_night_tendencies): 
                    ans["host_guest_some_late_survivors_club_mismatch"]+=1
            for g_id_num in id_nums_of_all_guests_staying_with_host:
                other_guest_preference = self.dict_of_guests[g_id_num]["late_night_tendencies"]
                if other_guest_preference == guest_late_night_tendencies:
                    ans["coguest_late_night_tendencies_match"]+=1
                if "early sleeper" in (other_guest_preference, guest_late_night_tendencies):
                    if "some late night" in (other_guest_preference, guest_late_night_tendencies): 
                        ans["coguest_early_sleeper_some_late_night_mismatch"]+=1
                if "survivors' club" in (other_guest_preference, guest_late_night_tendencies): 
                    if "early sleeper" in (other_guest_preference, guest_late_night_tendencies):
                        ans["coguest_early_sleeper_survivors_club_mismatch"]+=1
                if "some late night" in (other_guest_preference, guest_late_night_tendencies):
                    if "survivors' club" in (other_guest_preference, guest_late_night_tendencies): 
                        ans["coguest_some_late_survivors_club_mismatch"]+=1
        return ans
        
def mate(parent_1, parent_2):
    child = Genome()
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
                break
        starting_index_1+=1+i
        for i, edge in enumerate(edges_2[starting_index_2:]):
            if edge[0] not in [e[0] for e in child.chosen_edges] and edge[1] not in [e[1] for e in child.chosen_edges]:
                child.chosen_edges.append(edge)
                break
        starting_index_2+=1+i
    child.fill_edges()
    return child

#def ga(population_size=POPULATION_SIZE_DEFAULT_VALUE, generations=GENERATIONS_DEFAULT_VALUE, tournament_size=TOURNAMENT_SIZE_DEFAULT_VALUE, elite_percent=ELITE_PERCENT_DFAULT_VALUE, mate_percent=MATE_PERCENT_DEFAULT_VALUE, mutation_percent=MUTATION_PERCENT_DEFAULT_VALUE,starting_generation_descriptor_dir=STARTING_GENERATION_DESCRIPTOR_DIR_DEFAULT_VALUE,output_dir=OUTPUT_DIR_DEFAULT_VALUE): 
#    
#    global SAVE_VISUALIZATIONS
#    
#    global_pareto_frontier = [] # Dummy initial object so that we don't have to check if it's empty every time we attempt to add something to it. 
#    
#    # Genetic algorithm
#    starter_genomes_and_scores=[] # Get genomes from descriptor files
#    for potential_genome_list_descriptor_files in filter(lambda x:'.py'==x[-3:], list_dir_abs(starting_generation_descriptor_dir)):
#        lines=open(potential_genome_list_descriptor_files,'r').readlines()
#        for line in lines:
#            if 'genomes=[Genome([(' == line[:18]: # Not very secure :/ 
#                d = dict()
#                exec line in globals(), d
#                starter_genomes_and_scores += [(genome, 1/(genome.get_N_value()+1), 1/(genome.get_P_value()+1)) for genome in d['genomes']]
#    starter_genomes_and_scores = sorted(starter_genomes_and_scores, key=lambda x:(x[0],-x[1])) 
#    genomes = []
#    prev_inverse_P=inf # We're only starting with the pareto frontier of all the starter genomes bc there are usually too many starter genomes
#    for (genome, inverse_N, inverse_P) in starter_genomes_and_scores:
#        if inverse_P<=prev_inverse_P:
#            genomes.append(genome)
#            prev_P = P
#    while len(genomes)<population_size:
#        genomes.append(Genome())
#    
#    num_elites = int(round(elite_percent*population_size))
#    num_offspring = int(round(mate_percent*population_size))
#    num_mutated = int(round(mutation_percent*population_size))
#    
#    if SAVE_VISUALIZATIONS:
#        makedirs(join_paths([output_dir,'all_generations_point_cloud_graph_graph']))
#        makedirs(join_paths([output_dir,'point_cloud_graph']))
#        makedirs(join_paths([output_dir,'pareto_curve_graph']))
#        makedirs(join_paths([output_dir,'global_pareto_curve_graph']))
#        makedirs(join_paths([output_dir,'global_pareto_frontier_scores_csv']))
#        makedirs(join_paths([output_dir,'all_scores_per_generation_csv']))
#        makedirs(join_paths([output_dir,'pareto_frontier_scores_per_generation_csv']))
#        makedirs(join_paths([output_dir,'population_data']))
#        fig_all_points, subplot_all_points = get_subplots()
#        fig_global_pareto_curve_graph, subplot_global_pareto_curve_graph = get_subplots()
#    for generation in xrange(generations):
#        SAVE_VISUALIZATIONS=(generation%NUM_GENERATIONS_BEFORE_SAVING_VISUALIZATIONS==0)
#        print "%-30s Elapsed Time: %015f" % ("Working on generation "+str(generation)+'.',time.time()-START_TIME)
#        
#        # Save the population
#        with open(join_paths([os.path.abspath(output_dir),'population_data','generation_%03d.py'%generation]),'w') as f:
#            f.write('genomes='+genomes.__repr__())
#        
#        # Evaluate each population member
#        inverse_N_P_scores = sorted([(index, 1.0/(1+genome.get_N_value()), 1.0/(1+genome.get_P_value())) for index,genome in enumerate(genomes)], key=lambda x:x[1]) # sorted from lowest to highest 1/N values
#        xy = sorted(list(set([e[1:3] for e in inverse_N_P_scores])),key=lambda e:(e[0],-e[1]))
#        x = [1.0/e[0]-1 for e in xy] # N values
#        y = [1.0/e[1]-1 for e in xy] # P values
#        with open(join_paths([os.path.abspath(output_dir),'all_scores_per_generation_csv','generation_%03d.csv'%generation]),'w') as f:
#            f.write('N, P\n')
#            for n,p in zip(x,y):
#                f.write(str(int(n))+', '+str(int(p))+'\n')
#        if SAVE_VISUALIZATIONS:
#            #Save point clouds over all generations visualization
#            subplot_all_points.set_title('Generation '+str(generation))
#            subplot_all_points.scatter(x, y, zorder=10, c='c', alpha=0.10)
#            fig_all_points.savefig(join_paths([output_dir,'all_generations_point_cloud_graph_graph','generation_%03d.png'%generation]))
#            # Save only this generation point cloud visualization
#            fig, subplot = get_subplots()
#            subplot.scatter(x, y, zorder=10, c='r', alpha=1.0)
#            fig.savefig(join_paths([output_dir,'point_cloud_graph','generation_%03d.png'%generation]))
#            matplotlib.pyplot.close(fig)
#        # Get pareto ranking by N and P values
#        pareto_ranking = [] 
#        if SAVE_VISUALIZATIONS:
#            fig_pareto_curve_graph, subplot_pareto_curve_graph = get_subplots()
#        for pareto_rank_score in xrange(len(inverse_N_P_scores)): # the number of pareto rank values is upper bounded by the number of points as they all may fall on different pareto curves (imagine if they all lied on the f(x)=x line). 
#            indices_to_pop=[]
#            prev_inverse_P_score = inf
#            for i,(index_of_genome, inverse_N_score, inverse_P_score) in enumerate(sorted(inverse_N_P_scores, key=lambda e:e[1])):
#                if inverse_P_score<=prev_inverse_P_score:
#                    prev_inverse_P_score=inverse_P_score
#                    indices_to_pop.append(i)
#                    pareto_ranking.append((index_of_genome, pareto_rank_score, inverse_N_score, inverse_P_score))
#            # Update global_pareto_frontier
#            if pareto_rank_score==0:
#                if SAVE_VISUALIZATIONS:
#                    n_of_max_N=int(1.0/pareto_ranking[0][-2]-1)
#                    p_of_max_N=int(1.0/pareto_ranking[0][-1]-1)
#                    n_of_max_P=int(1.0/pareto_ranking[-1][-2]-1)
#                    p_of_max_P=int(1.0/pareto_ranking[-1][-1]-1)
#                    add_upper_left_text_box(subplot_pareto_curve_graph, "Max N: (N:"+str(n_of_max_N)+",P:"+str(p_of_max_N)+")\nMax P: (N:"+str(n_of_max_P)+",P:"+str(p_of_max_P)+")")
#                new_global_pareto_frontier=sorted(pareto_ranking+global_pareto_frontier, key=lambda x:(x[-2],-x[-1]))
#                indices_to_avoid=[]
#                prev_inverse_P = inf
#                for i, elem in enumerate(new_global_pareto_frontier):
#                    inverse_P_score=elem[-1]
#                    if inverse_P_score <= prev_inverse_P:
#                        prev_inverse_P = inverse_P_score
#                        continue
#                    indices_to_avoid.append(i)
#                for i in indices_to_avoid[::-1]:
#                    new_global_pareto_frontier.pop(i)
#                global_pareto_frontier=[]
#                for i, elem in enumerate(new_global_pareto_frontier):
#                    inverse_N_score=elem[-2]
#                    inverse_P_score=elem[-1]
#                    genome = genomes[elem[0]] if type(elem[0])==int else elem[0]
#                    assertion(isinstance(genome,Genome),"genome is not an instance of the class Genome.")
#                    global_pareto_frontier.append((genome,inverse_N_score,inverse_P_score))
#                with open(join_paths([os.path.abspath(output_dir),'pareto_frontier_scores_per_generation_csv','pareto_frontier_at_generation_%03d.csv'%generation]),'w') as f:
#                    f.write('N, P\n')
#                    for (_, _, inverse_N_score, inverse_P_score) in pareto_ranking:
#                        n = 1.0/inverse_N_score-1
#                        p = 1.0/inverse_P_score-1
#                        f.write(str(int(n))+', '+str(int(p))+'\n')
#            if SAVE_VISUALIZATIONS:
#                subplot_global_pareto_curve_graph.set_title('Generation '+str(generation))
#                xy = sorted(list(set([(inverse_N_score,inverse_P_score) for (genome,inverse_N_score,inverse_P_score) in global_pareto_frontier])), key=lambda e:(e[0],-e[1]))
#                x = [int(1.0/e[0]-1) for e in xy] # N values
#                y = [int(1.0/e[1]-1) for e in xy] # P values
#                color=numpy.random.rand(3,1)
#                subplot_global_pareto_curve_graph.plot(x, y, zorder=10, c=color, alpha=1.0)
#                subplot_global_pareto_curve_graph.scatter(x, y, zorder=10, c=color, alpha=1.0)
#                add_upper_left_text_box(subplot_global_pareto_curve_graph, "Max N: (N:"+str(x[0])+",P:"+str(y[0])+")\nMax P: (N:"+str(x[-1])+",P:"+str(y[-1])+")")
#                fig_global_pareto_curve_graph.savefig(join_paths([output_dir,'global_pareto_curve_graph','generation_%03d.png'%generation]))
#                subplot_pareto_curve_graph.set_title('Generation '+str(generation))
#                xy = sorted(list(set([inverse_N_P_scores[i][1:3] for i in indices_to_pop])), key=lambda e:(e[0],-e[1]))
#                x = [1.0/e[0]-1 for e in xy] # N values
#                y = [1.0/e[1]-1 for e in xy] # P values
#                color=numpy.random.rand(3,1)
#                subplot_pareto_curve_graph.plot(x, y, zorder=10, c=color, alpha=1.0)
#                subplot_pareto_curve_graph.scatter(x, y, zorder=10, c=color, alpha=1.0) # points may overlap, and thus some differen colored points may appear on multiple lines, which gives the illusion that the coloring of the points and lines are different.
#            for i in indices_to_pop[::-1]:
#                inverse_N_P_scores.pop(i)
#            if len(inverse_N_P_scores)==0:
#                break
#        if SAVE_VISUALIZATIONS:
#            fig_pareto_curve_graph.savefig(join_paths([output_dir,'pareto_curve_graph','generation_%03d.png'%generation]))
#            matplotlib.pyplot.close(fig_pareto_curve_graph)
#        assertion(len(inverse_N_P_scores)==0, "inverse_N_P_scores is not empty after pareto rank determination (all values should've been popped out of it.")
#        # Tournament selection for the elites
#        elites_scores = []
#        tournament_group_start_index=inf
#        while len(elites_scores)<num_elites:
#            if tournament_group_start_index>len(genomes)-1:
#                random.shuffle(pareto_ranking) # tournament groups are selected randomly
#                tournament_group_start_index=0
#            tournament_group_end_index = min(len(genomes), tournament_group_start_index+tournament_size)
#            tournament_group = pareto_ranking[tournament_group_start_index:tournament_group_end_index]
#            for genome_pareto_score_set in sorted(tournament_group, key=lambda x:x[1]):
#                if genome_pareto_score_set not in elites_scores:
#                    elites_scores.append(genome_pareto_score_set)
#                    break
#            tournament_group_start_index += tournament_size
#        elites = [genomes[index_of_genome] for (index_of_genome, pareto_rank_score, inverse_N_score, inverse_P_score) in elites_scores]
#        # Random mating 
#        offspring=[mate(random.choice(genomes),random.choice(genomes)) for i in xrange(num_offspring)]
#        # Random mutation
#        mutation=[]
#        for genome in random.sample(genomes,num_mutated):
#            mutation.append(genome.get_clone())
#            mutation[-1].mutate()
#        # Create the new generation
#        genomes=elites+offspring+mutation
#        genomes=genomes[:population_size]
#        assertion(len(genomes)==population_size,"len(genomes) is not equal to population_size.")
#        # Save global_pareto_frontier
#        with open(join_paths([os.path.abspath(output_dir),'global_pareto_frontier.py']),'w') as f:
#            # We want to save this on every generation in case the running stops for any reason ebfore we've reached our final generation.
#            f.write('genomes='+([e[0] for e in global_pareto_frontier]).__repr__())
#        with open(join_paths([os.path.abspath(output_dir),'global_pareto_frontier_scores_csv','global_pareto_frontier_at_generation_%03d.csv'%generation]),'w') as f:
#            f.write('N, P\n')
#            for (_,inverse_n,inverse_p) in global_pareto_frontier:
#                f.write(str(int(1.0/inverse_n-1))+', '+str(int(1.0/inverse_p-1))+'\n')
#    
#    if SAVE_VISUALIZATIONS:
#        matplotlib.pyplot.close(fig_all_points)
#        matplotlib.pyplot.close(fig_global_pareto_curve_graph)

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
    
    def __init__(self, dict_of_hosts0, dict_of_guests0, dict_of_host_spots0, dict_hosts_to_host_spots0, population_size0, tournament_size0, elite_percent0, mate_percent0, mutation_percent0):
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
            # [are_compatible(self.dict_of_hosts[host_id_num],guest) for guest_id_num, guest in self.dict_of_guests.items()]
            host = self.dict_of_hosts[host_id_num]
            for guest_id_num, guest in self.dict_of_guests.items():
                if are_compatible(host,guest):
                    self.graph.add_edge(host_spot_id_num,guest_id_num) # Edges are stored in (host_spot_id_num, guest_id_num) order
        
        self.genomes_list = [Genome(self.dict_of_hosts, self.dict_of_guests, self.dict_of_host_spots, self.dict_hosts_to_host_spots, self.graph) for _ in xrange(self.population_size)]
        
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
                '''genomes_list0='''+self.genomes_list.__repr__()+''', '''+ \
            ''')'''
        return ans

