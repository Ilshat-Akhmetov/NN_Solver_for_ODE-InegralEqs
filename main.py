from utilities import nth_derivative
from EquationAndDomain import OnePointInitialCondition, OneDimensionalMainEquation
from TrainerForNNEquationSolver import TrainerForNNEquationSolver
from ReportMaker import ReportMaker
import torch

if __name__ == "__main__":
    left_bound = 0
    right_bound = 1
    main_eq_residual = (
        lambda x, nn_model_value: nth_derivative(nn_model_value, x, 2)
        + 0.2 * nth_derivative(nn_model_value, x, 1)
        + nn_model_value
        + 0.2 * torch.exp(-x / 5) * torch.cos(x)
    )
    n_points = 100
    main_eq = OneDimensionalMainEquation(
        left_bound, right_bound, n_points, main_eq_residual
    )

    first_init_cond_res = lambda x, nn_model_value: nn_model_value - 0
    first_init_cond = OnePointInitialCondition(left_bound, first_init_cond_res)

    second_init_cond_res = lambda x, nn_model_value: nn_model_value - torch.sin(
        torch.Tensor([1])
    ) * torch.exp(torch.Tensor([-0.2]))
    second_init_cond = OnePointInitialCondition(right_bound, second_init_cond_res)

    boundary_conditions = [first_init_cond, second_init_cond]

    true_solution = lambda x: torch.exp(-x / 5) * torch.sin(x)
    nn_ode_solver = TrainerForNNEquationSolver(main_eq, boundary_conditions)
    loss_train, loss_valid, nn_model = nn_ode_solver.fit()
    report = ReportMaker(true_solution, nn_model, main_eq, loss_train, loss_valid)
    report.make_report()
