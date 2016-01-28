# lindy_hop_housing

Automated Housing Assigment Generator for Lindy Hop Events. 

=======================================================================================================================================

TODO:
    Very Important
        Add gender to teh host and guest classes
        add a person_id for each host to make telling if the hosts are teh same faster as well as making it easier to determine who else is staying with the host
        update the tips and hacks to explain the P and N concepts
        change it so that the hosts and guests are no longer lists but dictionaries where the key is the person's id_num
        
        Change the code so that it takes place in several stages
            step 1: preprocessing the data
                we will always need to go through the initial data anyway to read Misc. Comments. 
                our code will go through and tell if there are any problems with any entries, the user will have to fix them. 
                    problems can be bad data types, mispelled preferred co-guest names, etc. 
                during this initial phase, it should be noted that the user must add in manually if any two people can't stay together for specific reasons
            step 2: we run our GA
            Step 3: we print out our results for each solution we have
                we will state what things we could not obey when determing P, e.g. preferred guests they couldn't stay with, different late night tendencies, etc. It should be easily read by our user
        
        we need to change teh way we evaluate P
            P will be determined by many values, not just preferred guests. some ideas include
                how early a guest registered (what to do if this person is in a carpool with someone who registered last minute)
                prefered co-guests
                required co-guests (bc car pools)
                being housed with people from the same scene? Maybe? Ignore that for this iteration. 
                late night tendencies. Does this matter? 
                preferences with which gender they'd like to be housed? This can be ignored. 
            can we ask that people list no more than 4 carpool buddies?
            can we have it so that by the time housing registration closes, people must list their car pools?
                make registration work in such a way that they can edit who their car pool buddies are until the very last minute?
                    either that or make it some grunt work to be done by the housing coordinator before they use our algorithm.
                    we can have it so that when people list who they MUST stay with, they list a reason. 
                        Carpools and girlfriend/boyfriend are good reasons.
                        bc we're friends or want to hang out a lot is not.
            I think we should rearrange the algorithm so that people definitely already have carpools organized. 
                if they bitch about it, we can just say that they changed their plans after housing has been assigned. 
                we have to make them agree to it before they finish updating their registration, e.g. "You know that we will assign housing with carpools the way they are right now, and that we will not take into account carpool changes after housing closes."
                    We can make it so that there is a separate account for housing
                        make the housing coordinator nag the shit out of people the week before housing closes to fill out their housing.
                        send them an email saying "URGENT: We don't have your housing info. FILL IT OUT NOW." 
                So, we have some hard restrictions and some soft restrictions
                    Hard restrictions
                        cats, dogs, smoking, rides
                        required co-guests must stay together so taht we can assign housing based on groups
                    Soft restrictions
                        how early the guest registered
                        preferred co-guests
                        being housed with ppl from teh same scene
                        late night tendencies
                        gender housing tendencies (if they would have needed to stay with people of the same gender, we would have seen that in teh misc. info.)
        
        Would it be a good idea to have the GA take into account splitting carpools to get a higher N?
            what I mean is that we have our set of fixed groups of people who need to be togther
                this could be large groups like a whole scene or smaller groups of friends (about 8 or so) or small carpool groups of 4
            We could split them so that we might need to split a carpool group of 4 into two groups of two so that all four of them can get housed instead of not housing the 4 of them bc they won't fit somewhere. 
        
        change P to be a linear combination of all the soft values
        have diminishing returns for people staying together
            different methods
                per person, 1/(something) for each edge, something can be n**2, 2**n, etc.
                per group, 1/n of the graph. 
        We're going to assume that preferred co-guests and required co-guests are the same 
        
    Less Important
        implement feature where guests cannot be housed with smokers if they don't want to be housed with smokers
        Take into account gender preferences when it comes to calculating P
        Add gender preferences to Host and Guest classes
        Get script working to run island_ga.py on https://cloud.sagemath.com/ 
        Add parsing of actual data to add real hosts and guests instead of using the dummy func
            See how this works with real data
        Refactor each section of the main GA code into functions
        Take into account late night tendencies when it comes to calculating P

=======================================================================================================================================

Tips and Hacks for Usage:
    
    It might be a good idea to tweak the parameters for population size according to your computer's available processing resources.
    
    It's a good idea to check the visualizations during the running to make sure everything is running as it should. 
    
    It's good to have the number of generations unreasonably high to a point where it won't be complete in the time you need it. This way, you can stop it from running and have the results the algorithm generated up to that point. This avoids having idle time that the algorithm isn't using to find better results. 
        The results only get better as more generations pass since we save a global pareto frontier of the best results we've found so far over all the generations. 
        If you want to continue running the algorithm from a certain point, just take all the ".py" files in the output folder and use that folder to seed the starting generation of a new genetic algorithm run using the "-starting_generation_descriptor_dir" option.
    
    It might be a good idea to seed the starting generation with a maximum matching. You can use "Genome(networkx.maximal_matching(housing_graph))" to generate a genome that uses a maximum matching. Put it in a list called "genomes" and put that into a '.py' file, and the file can be used to seed the starting generation of a new genetic algorithm run via the "-starting_generation_descriptor_dir" option. 
    
    Keep in mind that we want to balance exploration and exploitation to get good performance. 
        If we seek exploration and high diversity, we will explore many of options, but these options may not necessarily be good. This will help us avoid local extrema in our search space but may take a lot of time.
        If we seek exploitation and high quality, we will explore only the options that perform best. This, however, may lead us to get stuck in local extrema. 
    
    Ways we can balance exploration and exploitation for good performance include playing with:
        Population Sizes: Larger population sizes will lead to more diversity, but processing each generation will also take more time.  Progress of the genetic search is saved after each generation is processed, so it might be a good idea to have each generation not take a long time as all time spent processing a generation is wasted if that generation has not completed processing. Smaller population sizes will have lower diversity. 
        Tournament Sizes: Smaller tournament sizes increase diversity. Larger tournament sizes lead to greedier searches. 
        Elite Percent: Having a higher percent of elites can decrease diversity and vice-versa (though to what extent this happens also depends on the tournament size). If there are more elites, it is more likely that they will be chosen for crossover and mutation (the selection for both of these is random selection) and vice-versa. Keep in mind that the impact that the percent of elites has on diversity is affected by the tournament size. 
        Mate Percent: Having a higher mate percent can increase diversity as the parents chosen for the mating is random. However, how diverse the new children will be depends on the number of elites in the population, which is dependent on the elite percent and the tournament size, as a larger percent of elites will lead to a larger probability that they will be chosen as parents to create offspring. However, we should keep in mind that these offspring may not necessarily be as elite as the parents. 
        Mutation Percent: Having a higher mutation percent can increase diversity as the genomes chosen for mutation is random. However, how diverse the mutated genomes will be depends on the number of elites in the population, which is dependent on the elite percent and the tournament size, as a larger percent of elites will lead to a larger probability that they will be chosen to be mutated. However, we should keep in mind that these mutated genomes may not necessarily be as elite as the original unmutated elite genome.
        Island GA: Having many different independently growing populations can lead to diversity as each population will go start in and go in different places in the search space. More independent populations will lead to more diverse results. Having these populations crossover with each other can increase exploitation. This can be done wither probabilistically or deterministically. This is worth considering to increase diversity. The interpopulation crossover on performance is hard to determine, but it does necessarily increase exploitation, which can be helpful to balance out the diversity induced by having independent populations.
        Keep in mind that genetic algorithms are randomized algorithms and that there is a lot of noise in the performance. The amount of noise is impacted by the nature of the problem as well as the parameters of our GA. Thus, a lot of the noise in our results is out of our hands, so it's hard to know what decisions are best without getting a strong understanding of the noise, which we can only gain through studying the results of our genetic algorithm with different inputs and parameter selections run a sufficient number of times (a sufficient number of times is also hard to determine). 
        Keep in mind that exploitation and exploration is not something that is easily measured and that it's hard to measure the impact that they have on the results. Two separate parameters may impact diversity, but those may affect the results in different ways. Simply knowing that diversity is impacted does not say anything about the new population members that are being looked at. Thus, it says nothing about how it impacts the results. We'll have to clearly study the results to really know how the impact of the parameters as we do not get a significant amount of insight about our results simply through knowing how the parameters impact exploration and exploitation. 
    
    The starting generation has a noteable impact on the performance of our genetic algorithm. Whichever direction we go in our search space depends on our starting population/starting point. Different starting generations will be different distances from the global extrema of our search space. Starting closer to global extrema is obviously better, but it is hard to determine where in the search space a starting generation is, where the global extrema are, and how far any pair of points are in the search space or even what metric is best to determine distance. We can really know nothing about how well our starting generation performs as we know very little about our search space (which is why we study it and use genetic algorithms to explore it rather than a more elegant method), but we do know that it has an impact. 
        We can manipulate our starting generation using the "-starting_generation_descriptor_dir" command line option. 

