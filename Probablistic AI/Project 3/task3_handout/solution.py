import numpy as np
from scipy.optimize import fmin_l_bfgs_b

from scipy.stats import norm
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel, Matern

domain = np.array([[0, 5]])
SAFETY_THRESHOLD = 1.2
SEED = 0

""" Solution """


class BO_algo():

    def __init__(self):
        """Initializes the algorithm with a parameter configuration. """

        # TODO: enter your code here
        # pass

        self.evaluated_points = []
        f_kernel = ConstantKernel(constant_value=0.5) * Matern(length_scale=0.5, length_scale_bounds='fixed', nu=2.5)
        v_kernel = ConstantKernel(constant_value=np.sqrt(2)) * Matern(length_scale=0.5, length_scale_bounds='fixed', nu=2.5) +  ConstantKernel(constant_value=1.5)
        self.f_model = GaussianProcessRegressor(kernel=f_kernel, alpha=0.15**2)  
        self.v_model = GaussianProcessRegressor(kernel=v_kernel, alpha=0.0001**2)  


    def next_recommendation(self):
        """
        Recommend the next input to sample.

        Returns
        -------
        recommendation: np.ndarray
            1 x domain.shape[0] array containing the next point to evaluate
        """

        # TODO: enter your code here
        # In implementing this function, you may use optimize_acquisition_function() defined below.
        # raise NotImplementedError

        return self.optimize_acquisition_function()


    def optimize_acquisition_function(self):
        """
        Optimizes the acquisition function.

        Returns
        -------
        x_opt: np.ndarray
            1 x domain.shape[0] array containing the point that maximize the acquisition function.
        """

        def objective(x):
            return -self.acquisition_function(x)

        f_values = []
        x_values = []

        # Restarts the optimization 20 times and pick best solution
        for _ in range(20):
            x0 = domain[:, 0] + (domain[:, 1] - domain[:, 0]) * \
                 np.random.rand(domain.shape[0])
            result = fmin_l_bfgs_b(objective, x0=x0, bounds=domain,
                                   approx_grad=True)
            x_values.append(np.clip(result[0], *domain[0]))
            f_values.append(-result[1])

        ind = np.argmax(f_values)
        return np.atleast_2d(x_values[ind]) #return array([[xnew]])

    def acquisition_function(self, x):
        """
        Compute the acquisition function.

        Parameters
        ----------
        x: np.ndarray
            x in domain of f

        Returns
        ------
        af_value: float
            Value of the acquisition function at x
        """

        # TODO: enter your code here
        # raise NotImplementedError


        x = np.atleast_2d(x)
        f_mu, f_sigma = self.f_model.predict(x, return_std=True)
        evaluated_points = np.array(self.evaluated_points)

        valid_index = np.where(evaluated_points[:, 2] > SAFETY_THRESHOLD)[0]
        if len(valid_index) == 0:
            EI = 1
        else:
            t = np.max(evaluated_points[valid_index, 1])
            z = (f_mu - t) / f_sigma
            EI = (f_mu - t) * norm.cdf(z) + f_sigma*norm.pdf(z)

        v_mu, v_sigma = self.v_model.predict(x, return_std=True)
        Pr = 1 - norm.cdf(SAFETY_THRESHOLD, loc=v_mu, scale=v_sigma)

        return EI * Pr


    def add_data_point(self, x, f, v):
        """
        Add data points to the model.

        Parameters
        ----------
        x: np.ndarray
            Hyperparameters
        f: np.ndarray
            Model accuracy
        v: np.ndarray
            Model training speed
        """

        # TODO: enter your code here
        # raise NotImplementedError
        """For Gaussian process, add point x and y = c(v,f)"""
        # self.evaluated_points.append([float(x), -float(f), float(v)])
        self.evaluated_points.append([float(x), float(f), float(v)])
        evaluated_points = np.array(self.evaluated_points)
        self.f_model.fit(evaluated_points[:, 0].reshape(-1,1), evaluated_points[:, 1])
        self.v_model.fit(evaluated_points[:, 0].reshape(-1,1), evaluated_points[:, 2])

    def get_solution(self):
        """
        Return x_opt that is believed to be the maximizer of f.

        Returns
        -------
        solution: np.ndarray
            1 x domain.shape[0] array containing the optimal solution of the problem
        """

        # TODO: enter your code here
        # raise NotImplementedError
        evaluated_points = np.array(self.evaluated_points)
        valid_index = np.where(evaluated_points[:, 2] > 1.2)[0]
        opt_index = np.argmax(evaluated_points[valid_index, 1])
        return evaluated_points[valid_index[opt_index], 0]


""" Toy problem to check code works as expected """

def check_in_domain(x):
    """Validate input"""
    x = np.atleast_2d(x)
    return np.all(x >= domain[None, :, 0]) and np.all(x <= domain[None, :, 1])


def f(x):
    """Dummy objective"""
    mid_point = domain[:, 0] + 0.5 * (domain[:, 1] - domain[:, 0])
    return - np.linalg.norm(x - mid_point, 2)  # -(x - 2.5)^2


def v(x):
    """Dummy speed"""
    return 2.0

def get_initial_safe_point():
    """Return initial safe point"""
    x_domain = np.linspace(*domain[0], 4000)[:, None]
    c_val = np.vectorize(v)(x_domain)
    x_valid = x_domain[c_val > SAFETY_THRESHOLD]
    np.random.seed(SEED)
    np.random.shuffle(x_valid)
    x_init = x_valid[0]
    return x_init



def main():
    # Init problem
    agent = BO_algo()

    # Add initial safe point
    x_init = get_initial_safe_point()
    obj_val = f(x_init)
    cost_val = v(x_init)
    agent.add_data_point(x_init, obj_val, cost_val)


    # Loop until budget is exhausted
    for j in range(20):
        # Get next recommendation
        x = agent.next_recommendation()

        # Check for valid shape
        assert x.shape == (1, domain.shape[0]), \
            f"The function next recommendation must return a numpy array of " \
            f"shape (1, {domain.shape[0]})"

        # Obtain objective and constraint observation
        obj_val = f(x)
        cost_val = v(x)
        agent.add_data_point(x, obj_val, cost_val)

    # Validate solution
    solution = np.atleast_2d(agent.get_solution())
    assert solution.shape == (1, domain.shape[0]), \
        f"The function get solution must return a numpy array of shape (" \
        f"1, {domain.shape[0]})"
    assert check_in_domain(solution), \
        f'The function get solution must return a point within the ' \
        f'domain, {solution} returned instead'

    # Compute regret
    if v(solution) < 1.2:
        regret = 1
    else:
        regret = (0 - f(solution))

    print(f'Optimal value: 0\nProposed solution {solution}\nSolution value '
          f'{f(solution)}\nRegret{regret}')


if __name__ == "__main__":
    main()