import numpy as np


class ParticleFilter:

    def __init__(self, states, initial_sample, transition_sample, observation_prob, n=1000):
        self.n = n
        self.states = states
        self.initial_sample = initial_sample  # P(x_0)
        self.transition_sample = transition_sample  # P(x_t+1|x_t, u_t)
        self.observation_prob = observation_prob  # P(z_t|x_t)
        self.init_particles()

    def init_particles(self):
        self.particles = np.empty((self.n, self.states))
        for i in range(self.states):
            self.particles[:, i] = self.initial_sample()
        self.weights = np.ones(self.n) / self.n

    def predict(self, action):
        for i in range(len(self.particles)):
            self.particles[i, :] = self.transition_sample(self.particles[i, :], action)

    def update(self, observation):
        for i in range(len(self.particles)):
            self.weights[i] *= self.observation_prob(observation, self.particles[i])  # Sample from distribution
        self.weights = self.weights/self.weights.sum()  # Normalize to sum to 1

    def resample(self):
        n_eff = 1 / np.sum(self.weights**2)
        if n_eff < self.n:
            cdf = np.cumsum(self.w)
            cdf[-1] = 1. # avoid round-off error
            indexes = np.searchsorted(cdf, np.random.uniform(self.n))
            self.particles[:] = self.particles[indexes] # resample according to indexes
            self.weights.fill(1.0 / self.n)


pf = ParticleFilter(
    states=1,
    initial_sample = lambda: np.array([np.random.normal(0, 1, 1)]),
    transition_sample = lambda x, u: np.random.normal(x + u, 1, 1),
    observation_prob = lambda z, x: np.random.normal(x, 1, z),
    n = 2
)

for i in range(2):
    pf.predict(1)
    pf.update(1)
    print(pf.particles)

