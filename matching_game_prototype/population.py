import numpy as np
import random, math

class Population():
  def __init__(self,P, nbagents_per_player=10,r=0.05,f1 = 0.3,f2=0.2,base_seed=0):
    #self.T = T
    self.base_seed = base_seed
    self.P = P # number of players
    self.t = 0
    self.I = P * nbagents_per_player
    self.p_i = np.kron( np.arange(P),np.ones(nbagents_per_player))
    self.f1= f1
    self.f2 = f2
    np.random.seed(base_seed)
    self.x_i = np.random.uniform(size = self.I)
    self.W_i = np.zeros(self.I)
    self.w_i = np.zeros(self.I)
    self.r = r
    self.matched = set()
    self.unmatched=set(range(self.I))
    # self.bid_functions = {p: (lambda x,phi: 0) for p in range (P)}
    self.bid_functions = dict.fromkeys(range(P), 0)

    # add a line (it needs a seed before running update function)
    self.seed = self.base_seed

  def bid(self,player, x, surplus):
    return self.bid_functions[player](x,surplus)


  def match(self, verbose = True):
    np.random.seed(self.seed )
    N = min(2 * max(1, int(np.floor(self.f2 * self.I / 2))),len(self.unmatched))  # ensure at least 1
    tomeet = random.sample(list(self.unmatched), N)
    if verbose:
      print("introduced ",tomeet)
    tomatch = []
    for n in range( math.ceil(N / 2) ):
      i,j = tomeet[2 * n], tomeet[2 * n + 1]
      phi = self.x_i[i]* self.x_i[j]
      ur = self.bid(self.p_i[i], self.x_i[i],phi)
      vr = self.bid(self.p_i[j], self.x_i[j],phi)
      # here, if u+v < phi then match i and j and split the surplus
      if ur + vr < phi:
        tomatch.append((i,j))
        self.matched.add((i,j))
        self.unmatched.remove(i)
        self.unmatched.remove(j)
        self.w_i[i] = (phi - ur - vr) / 2
        self.w_i[j] = (phi - ur - vr) / 2
    if verbose:
      print("matched ",tomatch)

  def unmatch(self, verbose=True):
    np.random.seed(self.seed )
    N = min(int(np.floor(self.f2 * len(self.matched))),len(self.matched))
    to_unmatch = random.sample(list(self.matched), N )
    if verbose:
      print("unmatched ",to_unmatch)
    for (i,j) in to_unmatch:
      self.matched.remove((i,j))
      self.unmatched.add(i)
      self.unmatched.add(j)
      self.w_i[i] = 0
      self.w_i[j] = 0

  def update(self):
    self.W_i += self.r * self.W_i + self.w_i
    self.t += 1
    self.seed = self.t + self.base_seed
    self.match()
    self.unmatch()