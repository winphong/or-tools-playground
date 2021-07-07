# importing google or tools and declaring model template
from ortools.sat.python import cp_model
model = cp_model.CpModel()
# declare empty list that will be used for storing indices for worker-shift-day combination
shiftoptions = {}

# set number of workers, days and schedules as well as max schedules per day,
# as well as max shift amount difference per worker
workers = 5
shifts = 3
days = 7
maxshiftsperday = 1
maxdifference = 1

# create a tuple as a shift option list index, for each combination of worker, shift and day
# use google or tools to create a boolean variable indicating if given worker works on that day, in that shift
for x in range(workers):
    for y in range(days):
        for z in range(shifts):
            shiftoptions[(x, y, z)] = model.NewBoolVar(
                "shift with id" + str(x) + " " + str(y) + " " + str(z))

# now we add the constraint of shift only being assigned to one worker
for y in range(days):
    for z in range(shifts):
        model.Add(sum(shiftoptions[(x, y, z)] for x in range(workers)) == 1)
# now we add the constraint of a worker only working one shift per day
for x in range(workers):
    for y in range(days):
        model.Add(sum(shiftoptions[(x, y, z)] for z in range(shifts)) <= 1)
# now we add the constraint of all workers having the same amount of shifts, with some deviations allowed for with a maximum allowed difference
minshiftsperworker = (shifts * days) // workers
print(minshiftsperworker)
maxshiftsperworker = minshiftsperworker + maxdifference
for x in range(workers):
    shiftsassigned = 0
    for y in range(days):
        for z in range(shifts):
            shiftsassigned += shiftoptions[(x, y, z)]
    model.Add(minshiftsperworker <= shiftsassigned)
    model.Add(shiftsassigned <= maxshiftsperworker)

# before solving the problem I add a solution printer (this code is taken directly from Google's documentation)


class SolutionPrinterClass(cp_model.CpSolverSolutionCallback):
    def __init__(self, shiftoptions, workers, days, shifts, sols):
        val = cp_model.CpSolverSolutionCallback.__init__(self)
        self._shiftoptions = shiftoptions
        self._workers = workers
        self._days = days
        self._shifts = shifts
        self._solutions = set(sols)
        self._solution_count = 0

    def on_solution_callback(self):
        if self._solution_count in self._solutions:
            print("solution " + str(self._solution_count))
            for y in range(self._days):
                print("day " + str(y))
                for x in range(self._workers):
                    is_working = False
                    for z in range(self._shifts):
                        if self.Value(self._shiftoptions[(x, y, z)]):
                            is_working = True
                            print("worker " + str(x) + " works day " +
                                  str(y) + " shift " + str(z))
                    if not is_working:
                        print('  Worker {} does not work'.format(x))
            print()
        self._solution_count += 1

    def solution_count(self):
        return self._solution_count


# solve the model
solver = cp_model.CpSolver()
solver.parameters.linearization_level = 0
# solve it and check if solution was feasible
# we want to display 1 feasible results (the first one in the feasible set)
solutionrange = range(1)
solution_printer = SolutionPrinterClass(shiftoptions, workers,
                                        days, shifts, solutionrange)
solver.SearchForAllSolutions(model, solution_printer)
