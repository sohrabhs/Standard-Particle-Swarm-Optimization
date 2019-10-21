class SPSO_FeatureSelection_WrapperMethod_continuous_BySelectionSize(StandardParticleSwarmOptimization):
    def __init__(self, X_train, y_train, X_test, y_test, subsetSize, wrapperModel, iteration, populationSize,
                 w, c1, c2, silent=True):

        self.iteration = iteration
        self.popSize = populationSize
        self.subsetSize = subsetSize
        self.silent = silent
        self.wrapperModel = wrapperModel
        features = [i + 1 for i in range(0, X_train.shape[1])]
        self.features = features
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test
        self.featureSize = len(features)
        self.selected_features = None
        self.max_accuracy = None
        super().__init__(it=iteration, popSize=populationSize, w=w, c1=c1, c2=c2, minimization=False, silent=silent)

    def optimize(self):
        super().optimize()
        permutation = np.array(sorted(range(len(self.bestSolution)), key=lambda k: self.bestSolution[k])) + 1
        self.selected_features = sorted(permutation[:self.subsetSize].tolist())
        self.max_accuracy = self.bestObj

    def initial_solution(self):
        pop = [0] * self.popSize
        for i in range(len(pop)):
            pop[i] = np.random.rand(self.featureSize)
        return pop

    def objective_function(self, pop):
        obj = [0] * len(pop)
        for i in range(len(pop)):
            chrome = pop[i]
            permutation = np.array(sorted(range(len(chrome)), key=lambda k: chrome[k])) + 1
            selected_features = permutation[:self.subsetSize]
            X_train, y_train, X_test, y_test = self.feature_selected(self.X_train, self.y_train, self.X_test, self.y_test, selected_features)
            obj[i] = self.accuracy_calc(X_train, y_train, X_test, y_test, self.wrapperModel)
        return obj

    def update_position(self, velocity, pop):
        new_pop = [0] * self.popSize
        for i in range(self.popSize):
            new_pop[i] = pop[i] + velocity[i]
        return new_pop

    def update_velocity(self, velocity, pop, personal_best_position, global_best_position, c1, c2, w):
        np.random.seed(0)
        R1 = np.random.rand(self.popSize, len(pop[0]))
        np.random.seed(1)
        R2 = np.random.rand(self.popSize, len(pop[0]))
        if velocity != None:
            for i in range(self.popSize):
                velocity[i] = w * velocity[i] + c1 * (R1[i] * (personal_best_position[i] - pop[i])) + c2 * (
                    R2[i] * (global_best_position - pop[i]))
        else:
            velocity = [0] * self.popSize
            for i in range(self.popSize):
                velocity[i] = c1 * (R1[i] * (personal_best_position[i] - pop[i])) + c2 * (
                    R2[i] * (global_best_position - pop[i]))
        return velocity

    def feature_selected(self, X_train, y_train, X_test, y_test, selected):
	features = [i + 1 for i in range(0, X_train.shape[1])]
	mask = [i - 1 for i in features if i in selected]
	X_train = X_train[:, mask]
	y_train = y_train
	X_test = X_test[:, mask]
	y_test = y_test
	return X_train, y_train, X_test, y_test

