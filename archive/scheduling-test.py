from ortools.sat.python import cp_model
import random
import json

data = [
    {'userId': '96d3a616-db1f-11eb-8d19-0242ac130003'},
    {'schedules': ['']}

]

# id correspond to day of the week
days = {
    0: [1, 2, 3],
    1: [],
    2: [],
    3: [],
    4: [],
    5: [],
    6: [],
    7: [4, 5, 6, 7]
}

# id does not need to follow index
shifts = {
    1: {'id': 1, 'timeStart': 2, 'timeEnd': 4, 'role': 'staff', },
    2: {'id': 2, 'timeStart': 7, 'timeEnd': 9, 'role': 'staff'},
    3: {'id': 3, 'timeStart': 9, 'timeEnd': 16, 'role': 'staff'},
    4: {'id': 4, 'timeStart': 11, 'timeEnd': 20, 'role': 'staff'},
    5: {'id': 5, 'timeStart': 2, 'timeEnd': 21, 'role': 'staff'},
    6: {'id': 6, 'timeStart': 13, 'timeEnd': 14, 'role': 'staff'},
    7: {'id': 7, 'timeStart': 13, 'timeEnd': 14, 'role': 'staff'},
}

nurses = {
    'cherry': {'name': 'cherry', 'role': ['staff', 'cook']},
    'daniel': {'name': 'daniel', 'role': ['staff', 'cook']},
    'elijah': {'name': 'elijah', 'role': ['staff', 'cook']},
}

arr = []
for nurse_key, nurse_value in nurses.items():
    arr.append([])
    for day_key, day_value in days.items():
        arr.append([])
        for shift_key, shift_value in shifts.items():
            print('idk')


def main():
    # This program tries to find an optimal assignment of nurses to shifts
    # (3 shifts per day, for 7 days), subject to some constraints (see below).
    # Each nurse can request to be assigned to specific shifts.
    # The optimal assignment maximizes the number of fulfilled 0shift requests.
    num_nurses = 5
    num_shifts = 3
    num_days = 7
    all_nurses = range(num_nurses)
    all_shifts = range(num_shifts)
    all_days = range(num_days)

    # shift_requests = [ # num of nurse = 5
    #                     [ # num of days = 7
    #                         # num of shifts = 3
    #                         [1, 0, 0], [1, 1, 1], [0, 0, 0], [0, 0, 0], [0, 0, 1], [1, 1, 0], [0, 0, 1]
    #                     ],
    #                     [
    #                         [1, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 0], [1, 0, 0], [0,1, 0], [1, 0, 1]
    #                     ],
    #                     [
    #                         [0, 1, 0], [0, 1, 1], [0, 0, 0], [1, 1, 0], [0, 0, 0], [0, 1, 0], [0, 0, 0]
    #                     ],
    #                     [
    #                         [0, 0, 1], [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 1, 0], [1, 0, 0], [0, 0, 0]
    #                     ],
    #                     [
    #                         [0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 0, 0], [1, 1, 0], [0, 1, 0], [0, 0, 0]
    #                     ]
    #                 ]

    shift_requests = []
    shift_requests = [  # num of nurse = 5
        [  # num of days = 7
            [  # num of shifts = 3
                [  # for each shift
                    1,  # match shift availability
                    1,  # match day availability
                    1,  # has no clashing shift
                    1,  # has no  clashing dayOff
                    8,  # num of hours for shift,
                ],
                [  # for each shift
                    1,  # match shift availability
                    1,  # match day availability
                    1,  # have no clashing shift
                    1,  # have no clashing dayOff
                    8,  # num of hours for shift,
                ],
            ],
        ],
        [
            [  # for each shift
                1, 1, 1, 1, 8
            ],
            [  # for each shift
                1, 1, 0, 0, 8
            ],
        ],
        [
            [  # for each shift
                1, 1, 1, 1, 8
            ],
            [  # for each shift
                1, 1, 0, 0, 8
            ],
        ],

    ]

    # for i in range(num_nurses):
    #     shift_requests.append([])
    #     for j in range(num_days):
    #         shift_requests[i].append([])
    #         for k in range(num_shifts):
    #             shift_requests[i][j].append(random.randint(0, 1))

    model = cp_model.CpModel()

    # Creates shift variables.
    # shifts[(n, d, s, 2)]: nurse 'n' works shift 's' on day 'd'.
    shifts = {}
    for n in all_nurses:
        for d in all_days:
            for s in all_shifts:
                shifts[(n, d, s, 2)] = model.NewBoolVar(
                    'shift_n%id%is%i' % (n, d, s))

    # for n in all_nurses:
    #     print(shifts[(n, d, s, 2)])

    print(sum(shifts[(n, d, s, 2)] for n in all_nurses) == 1)

    # Each shift is assigned to exactly one nurse in .
    for d in all_days:
        for s in all_shifts:
            model.Add(sum(shifts[(n, d, s, 2)] for n in all_nurses) == 1)

    # Each nurse works at most one shift per day.
    for n in all_nurses:
        for d in all_days:
            model.Add(sum(shifts[(n, d, s, 2)] for s in all_shifts) <= 1)

    #  for n in all_nurses:
    #     for d in all_days:
    #         model.Add(sum(shifts[(n, d, s, 2, c)] for s in all_shifts) >= 1)

    # # Try to distribute the shifts evenly, so that each nurse works
    # # min_shifts_per_nurse shifts. If this is not possible, because the total
    # # number of shifts is not divisible by the number of nurses, some nurses will
    # # be assigned one more shift.
    # min_shifts_per_nurse = (num_shifts * num_days) // num_nurses
    # if num_shifts * num_days % num_nurses == 0:
    #     max_shifts_per_nurse = min_shifts_per_nurse
    # else:
    #     max_shifts_per_nurse = min_shifts_per_nurse + 1
    # for n in all_nurses:
    #     num_shifts_worked = 0
    #     for d in all_days:
    #         for s in all_shifts:
    #             num_shifts_worked += shifts[(n, d, s, 2)]
    #     model.Add(min_shifts_per_nurse <= num_shifts_worked)
    #     model.Add(num_shifts_worked <= max_shifts_per_nurse)

    # pylint: disable=g-complex-comprehension
    model.Maximize(
        sum(
            shift_requests[n][d][s] * shifts[(n, d, s, 2)]
            for n in all_nurses
            for d in all_days
            for s in all_shifts))
    # Creates the solver and solve.
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 10
    solver.Solve(model)
    for d in all_days:
        print('Day', d)
        for n in all_nurses:
            for s in all_shifts:
                if solver.Value(shifts[(n, d, s, 2)]) == 1:
                    if shift_requests[n][d][s] == 1:
                        print('Nurse', n, 'works shift', s, '(requested).')
                    else:
                        print('Nurse', n, 'works shift', s, '(not requested).')
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
