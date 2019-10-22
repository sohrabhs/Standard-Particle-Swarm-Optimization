import numpy as np

class StandardParticleSwarmOptimization:
    def __init__(self, it=20, popSize=10, w=0.9, c1=1, c2=1, minimization=True, silent=True):
        self.minimization = minimization
        self.silent = silent
        self.it = it
        self.popSize = popSize
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.bestSolution = None
        self.bestObj = None

    def sortedFirstBySecond(self, first, second, reverse=False):
        index = np.array(sorted(range(len(second)), key=lambda k: second[k], reverse=reverse))
        second = np.array(sorted(second, reverse=reverse))
        first = np.array(first)
        first = first[index]
        first = first.tolist()
        second = second.tolist()
        return first, second

    def optimize(self):
        # Generate first swarm
        pop = self.initial_solution()

        # Evaluate the fitness of all particles
        obj = self.objective_function(pop)

        # Record personal best fitness of all particles
        personal_best_obj = obj
        personal_best_position = pop

        # Find global best particle
        if self.minimization:
            p_best_position, p_best_obj = self.sortedFirstBySecond(personal_best_position,
                                                                      personal_best_obj,
                                                                      reverse=False)
        else:
            p_best_position, p_best_obj = self.sortedFirstBySecond(personal_best_position,
                                                                      personal_best_obj,
                                                                      reverse=True)
        global_best_obj = p_best_obj[0]
        global_best_position = p_best_position[0]

        # update the velocity of particles
        velocity = self.update_velocity(None, pop, personal_best_position, global_best_position, self.c1, self.c2, self.w)

        # update the position of particles
        pop = self.update_position(velocity, pop)

        # ---------------------------------------------------------------------------------------------
        # -----------------------------------     main loop     ---------------------------------------
        # ---------------------------------------------------------------------------------------------
        for p in range(0, self.it):
            # Evaluate the fitness of all particles
            obj = self.objective_function(pop)

            # Record personal best fitness of all particles
            if self.minimization:
                for i in range(len(personal_best_obj)):
                    if obj[i] < personal_best_obj[i]:
                        personal_best_obj[i] = obj[i]
                        personal_best_position[i] = pop[i]
            else:
                for i in range(len(personal_best_obj)):
                    if obj[i] > personal_best_obj[i]:
                        personal_best_obj[i] = obj[i]
                        personal_best_position[i] = pop[i]

            # Find global best particle
            if self.minimization:
                p_best_position, per_best_obj = self.sortedFirstBySecond(personal_best_position,
                                                                            personal_best_obj,
                                                                            reverse=False)
            else:
                p_best_position, per_best_obj = self.sortedFirstBySecond(personal_best_position,
                                                                            personal_best_obj,
                                                                            reverse=True)
            if self.minimization:
                if per_best_obj[0] < global_best_obj:
                    global_best_obj = per_best_obj[0]
                    global_best_position = p_best_position[0]
            else:
                if per_best_obj[0] > global_best_obj:
                    global_best_obj = per_best_obj[0]
                    global_best_position = p_best_position[0]

            # update the velocity of particles
            velocity = self.update_velocity(velocity, pop, personal_best_position, global_best_position, self.c1, self.c2, self.w)

            # update the position of particles
            pop = self.update_position(velocity, pop)

            if not self.silent:
                print("it", p + 1, "obj", global_best_obj)
                # print("it", p + 1, "obj", obj)
        self.bestSolution = global_best_position
        self.bestObj = global_best_obj

    def initial_solution(self):
        pass

    def objective_function(self, pop):
        pass

    def update_position(self, velocity, pop):
        pass

    def update_velocity(self, velocity, pop, personal_best_position, global_best_position, c1, c2, w):
        pass







