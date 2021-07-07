"""Simple solve."""

from ortools.sat.python import cp_model


def SimpleSatProgram():
  """Minimal CP-SAT example to showcase calling the solver."""
  # Creates the model.
  model = cp_model.CpModel()

  # Creates the variables.
  num_vals = 3
  x = model.NewIntVar(2, num_vals - 1, 'a')
  y = model.NewIntVar(2, num_vals * 2 - 1, 'g')
  z = model.NewIntVar(2, num_vals * 3 - 1, 'd')

  # Creates the constraints.
  model.Add(x != y)
  model.Add(x != z)
  model.Add(y != z)

  # Creates a solver and solves the model.
  solver = cp_model.CpSolver()
  status = solver.Solve(model)

  if status == cp_model.OPTIMAL:
    print('x = %i' % solver.Value(x))
    print('y = %i' % solver.Value(y))
    print('z = %i' % solver.Value(z))

  print(status)


SimpleSatProgram()