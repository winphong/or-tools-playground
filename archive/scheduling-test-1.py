from ortools.sat.python import cp_model
import random
import json


def main():
    # This program tries to find an optimal assignment of nurses to shifts
    # (3 shifts per day, for 7 days), subject to some constraints (see below).
    # Each nurse can request to be assigned to specific shifts.
    # The optimal assignment maximizes the number of fulfilled 0shift requests.
    num_nurses = 3
    num_shifts = 2
    num_days = 2
    all_nurses = range(num_nurses)
    all_shifts = range(num_shifts)
    all_days = range(num_days)
    all_conditions = range(4)

    shift_requests = [  # num of nurse = 3
        [  # num of days = 2
            [  # num of shifts = 2
                [  # for each shift
                    1,  # match shift availability
                    1,  # match day availability
                    1,  # has no clashing shift
                    1,  # has no clashing dayOff
                    15,  # num of hours for shift,
                ],
                [  # for each shift
                    1,  # match shift availability
                    1,  # match day availability
                    1,  # have no clashing shift
                    1,  # have no clashing dayOff
                    12,  # num of hours for shift,
                ],
            ],
            [  # num of shifts = 2
                [1, 1, 0, 1, 18],
                [1, 1, 1, 1, 3],
            ],
        ],
        [
            [
                [1, 1, 1, 1, 24],  # nurse 1, day 0, shift 0
                [1, 1, 1, 0, 10],  # nurse 1, day 0, shift 1
            ],
            [
                [1, 1, 1, 1, 15],  # nurse 1, day 1, shift 0
                [0, 0, 0, 0, 3],  # nurse 1, day 1, shift 1
            ]
        ],
        [
            [
                [1, 1, 1, 1, 11],  # nurse 2, day 0, shift 0
                [0, 0, 0, 0, 12]  # nurse 2, day 0, shift 1
            ],
            [
                [1, 1, 0, 1, 16],  # nurse 2, day 1, shift 0
                [1, 1, 1, 1, 3]  # nurse 2, day 1, shift 1
            ]
        ],

    ]

    model = cp_model.CpModel()

    # Creates shift variables.
    # shifts[(n, d, s, c)]: nurse 'n' works shift 's' on day 'd' under condition 'c'
    shifts = {}
    for n in all_nurses:
        for d in all_days:
            for s in all_shifts:
                for c in all_conditions:
                    shifts[n, d, s, c] = model.NewBoolVar(
                        'shift_n%id%is%ic%i' % (n, d, s, c))

    # Constraint where shift should only be assigned if all criteria are filled
    for n in all_nurses:
        for d in all_days:
            for s in all_shifts:
                model.AddBoolAnd([shifts[n, d, s, c]
                                 for c in all_conditions])

    # Each shift is assigned to exactly one nurse in .
    # [START exactly_one_nurse]
    for d in all_days:
        for s in all_shifts:
            for n in all_nurses:
                tmp.append(sum((shifts[n, d, s, c] for c in all_conditions)))

                AddMaxEquality(teacher_courses[course, subject, t],
                               temp_array)
            model.Add(sum(tmp) < 1)
    # [END exactly_one_nurse]

    # # Each nurse works at most one shift per day.
    # # [START at_most_one_shift]
    # for n in all_nurses:
    #     for d in all_days:
    #         model.Add(sum(shifts[(n, d, s)] for s in all_shifts) <= 1)
    # # [END at_most_one_shift]

    #
    # =======================================================================================
    #
    # hours = {}
    # for n in all_nurses:
    #     for d in all_days:
    #         for s in all_shifts:
    #             hours[(n, d, s)] = model.NewConstant(
    #                 shift_requests[n][d][s][4])

    # for n in all_nurses:
    #     model.Add(sum(hours[(n, d, s)]
    #                   for d in all_days for s in all_shifts) <= 44)
    #     # model.Maximize(sum(hours[(n, d, s)]
    #     #                for d in all_days for s in all_shifts))

    # averages = []
    # a = model.NewIntVar(0, sum_of_costs * scaling,
    #                     'average_cost_of_group_%i' % j)
    # averages.append(a)
    # obj = model.NewIntVar(0, sum_of_costs * scaling, 'obj')
    # model.AddMaxEquality(obj, averages)

    # for n in all_nurses:
    #     max_shift_arr = []

    #     for d in all_days:

    #         for s in all_shifts:
    #             condition_arr = []
    #             temp_arr = []

    #             for c in all_conditions:
    #                 condition_arr.append(shifts[(n, d, s, c)])
    #                 temp_arr.append(shift_requests[n][d][s][c])

    #             # ensure all condition must be met
    #             model.AddBoolAnd(condition_arr)
    #             # ensure all sadsadasdsasdsadsadsadsadsad
    #             max_shift_arr.append(all(temp_arr))

    #     model.Add(sum(max_shift_arr) < 3)
    #
    # =======================================================================================
    #

    # Constraint where each user is not assigned more than n hours in the week
    # for n in all_nurses:
    #     model.Add(sum(shift_requests[n][d][s][4]
    #                   for d in all_days for s in all_shifts
    #                   if sum(shift_requests[n][d][s][c] for c in all_conditions) == 4)
    #               <= 44)

    # hours = {}
    # for n in all_nurses:
    #     for d in all_days:
    #         for s in all_shifts:
    #             # print(shift_requests[n][d][s][4])
    #             hours[(n, d, s)] = model.NewConstant(
    #                 shift_requests[n][d][s][4])

    # for n in all_nurses:
    #     model.AddLinearConstraint(sum(hours[(
    #         n, d, s)] for d in all_days for s in all_shifts
    #     ), 0, 44)

    # # Each nurse works at most one shift per day.
    # for n in all_nurses:
    #     for d in all_days:
    #         model.Add(sum(shifts[(n, d, s, c)] for s in all_shifts) <= 1)

    # Try to distribute the shifts evenly, so that each nurse works
    # min_shifts_per_nurse shifts. If this is not possible, because the total
    # number of shifts is not divisible by the number of nurses, some nurses will
    # be assigned one more shift.
    # min_shifts_per_nurse = (num_shifts * num_days) // num_nurses
    # if num_shifts * num_days % num_nurses == 0:
    #     max_shifts_per_nurse = min_shifts_per_nurse
    # else:
    #     max_shifts_per_nurse = min_shifts_per_nurse + 1
    # for n in all_nurses:
    #     num_shifts_worked = 0
    #     for d in all_days:
    #         for s in all_shifts:
    #             num_shifts_worked += shifts[(n, d, s)]
    #     model.Add(min_shifts_per_nurse <= num_shifts_worked)
    #     model.Add(num_shifts_worked <= max_shifts_per_nurse)

    # pylint: disable = g-complex-comprehension
    # model.Maximize(
    #     sum(
    #         shift_requests[n][d][s][c] * shifts[(n, d, s, c)]
    #         for n in all_nurses
    #         for d in all_days
    #         for s in all_shifts
    #         for c in all_conditions
    #     )
    # )

    # Creates the solver and solve.
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 10
    status = solver.Solve(model)

    if (status == cp_model.INFEASIBLE):
        print("INFEASIBLE")

    for n in all_nurses:
        for d in all_days:
            for s in all_shifts:
                if all(solver.BooleanValue(shifts[(n, d, s, c)]) for c in all_conditions):
                    if sum(shift_requests[n][d][s][c] for c in all_conditions) == 4:
                        print('Nurse', n, 'works shift', s, 'on day', d)
                    else:
                        print('Not working')
        print()

    # Statistics.
    print()
    print('Statistics')
    # print('  - Number of shift requests met = %i' % solver.ObjectiveValue(),
    #       '(out of', num_nurses * min_shifts_per_nurse, ')')
    # print('  - wall time       : %f s' % solver.WallTime())
    print(solver.ResponseStats())


if __name__ == '__main__':
    main()
