from ortools.sat.python import cp_model

days = {
    0: [0, 1],
    1: [2, 3],
    2: [4, 5, 6],
    3: [7],
    4: [8, 9],
    5: [10, 11, 12, 13, 14, 15],
    6: [16, 17, 18, 19, 20],
}

shiftSlots = {
    0: {'shiftSlotId': 0, 'start': 8, 'end': 20, 'hours': 12},
    1: {'shiftSlotId': 1, 'start': 8, 'end': 16, 'hours': 8},
    2: {'shiftSlotId': 2, 'start': 3, 'end': 23, 'hours': 20},
    3: {'shiftSlotId': 3, 'start': 0, 'end': 18, 'hours': 18},
    4: {'shiftSlotId': 4, 'start': 8, 'end': 15, 'hours': 7},
    5: {'shiftSlotId': 5, 'start': 5, 'end': 20, 'hours': 15},
    6: {'shiftSlotId': 6, 'start': 8, 'end': 14, 'hours': 6},
    7: {'shiftSlotId': 7, 'start': 8, 'end': 20, 'hours': 12},
    8: {'shiftSlotId': 8, 'start': 8, 'end': 16, 'hours': 8},
    9: {'shiftSlotId': 9, 'start': 2, 'end': 22, 'hours': 20},
    10: {'shiftSlotId': 10, 'start': 12, 'end': 14, 'hours': 2},
    11: {'shiftSlotId': 11, 'start': 6, 'end': 10, 'hours': 4},
    12: {'shiftSlotId': 12, 'start': 2, 'end': 4, 'hours': 2},
    13: {'shiftSlotId': 13, 'start': 15, 'end': 18, 'hours': 3},
    14: {'shiftSlotId': 14, 'start': 6, 'end': 10, 'hours': 4},
    15: {'shiftSlotId': 15, 'start': 2, 'end': 8, 'hours': 6},
    16: {'shiftSlotId': 16, 'start': 10, 'end': 18, 'hours': 8},
    17: {'shiftSlotId': 17, 'start': 20, 'end': 22, 'hours': 2},
    18: {'shiftSlotId': 18, 'start': 13, 'end': 16, 'hours': 3},
    19: {'shiftSlotId': 19, 'start': 2, 'end': 3, 'hours': 1},
    20: {'shiftSlotId': 20, 'start': 1, 'end': 5, 'hours': 4},
}

# assuming ordered by absentism rate in descending order (worst to best)
staff_dict = {
    # to convert to minutes
    0: {'userId': 'marcus', 'daily_ot_limit': 8, 'weekly_ot_limit': 46},
    1: {'userId': 'cherry', 'daily_ot_limit': 8, 'weekly_ot_limit': 44},
    2: {'userId': 'daniel', 'daily_ot_limit': 8, 'weekly_ot_limit': 46},
    3: {'userId': 'elijah', 'daily_ot_limit': 8, 'weekly_ot_limit': 46},
    4: {'userId': 'phillip', 'daily_ot_limit': 8, 'weekly_ot_limit': 44},
    5: {'userId': 'marcel', 'daily_ot_limit': 8, 'weekly_ot_limit': 46},
    6: {'userId': 'winston', 'daily_ot_limit': 8, 'weekly_ot_limit': 46},
    7: {'userId': 'arial', 'daily_ot_limit': 8, 'weekly_ot_limit': 44},
    8: {'userId': 'tina', 'daily_ot_limit': 8, 'weekly_ot_limit': 46},
    9: {'userId': 'marcus_1', 'daily_ot_limit': 8, 'weekly_ot_limit': 46},
    10: {'userId': 'cherry_1', 'daily_ot_limit': 8, 'weekly_ot_limit': 44},
    11: {'userId': 'daniel_1', 'daily_ot_limit': 8, 'weekly_ot_limit': 46},
    12: {'userId': 'elijah_1', 'daily_ot_limit': 8, 'weekly_ot_limit': 46},
    13: {'userId': 'phillip_1', 'daily_ot_limit': 8, 'weekly_ot_limit': 44},
    14: {'userId': 'marcel_1', 'daily_ot_limit': 8, 'weekly_ot_limit': 46},
    15: {'userId': 'winston_1', 'daily_ot_limit': 8, 'weekly_ot_limit': 46},
    16: {'userId': 'arial_1', 'daily_ot_limit': 8, 'weekly_ot_limit': 44},
    17: {'userId': 'tina_1', 'daily_ot_limit': 8, 'weekly_ot_limit': 46},
}

shifts_data = []
for staff in range(len(staff_dict)):
    shifts_data.append([])
    for day in range(len(days)):
        shifts_data[staff].append([])
        for shift in range(len(shiftSlots)):
            if (shift in days[day]):
                shifts_data[staff][day].append(
                    [
                        1,
                        shiftSlots[shift]['hours']
                    ])
            else:
                shifts_data[staff][day].append([0, 0])

# for staff in range(len(staff_dict)):
#     shifts_data.append([])
#     for day in range(len(days)):
#         shifts_data[staff].append([])
#         for shift in range(len(shiftSlots)):
#             shifts_data[staff][day].append(
#                 [
#                     # eligibility for the shiftslot (filtered by availability and roles)
#                     1,
#                     shiftSlots[shift]['hours'],
#                 ])


def main():
    # This program tries to find an optimal assignment of all_staff to shifts
    # Each staff can request to be assigned to specific shifts.
    all_staff = range(len(staff_dict))
    all_shifts = range(len(shiftSlots))
    all_days = range(len(days))

    model = cp_model.CpModel()

    # Creates shift variables.
    # shifts[(n, d, s, c)]: staff 'n' works shift 's' on day 'd'
    shifts = {}
    for n in all_staff:
        for d in all_days:
            for s in all_shifts:
                shifts[n, d, s] = model.NewBoolVar(
                    'shift_n%id%is%i' % (n, d, s))

    # Each staff works at most one shift per day.
    # [START at_most_one_shift]
    for n in all_staff:
        for d in all_days:
            model.Add(sum(shifts[(n, d, s)] for s in all_shifts) <= 1)
    # [END at_most_one_shift]
    #
    # =======================================================================================
    #
    # Each staff works at most n hour per week according to weekly OT limit.
    # [START at_most_x_hours]
    for n in all_staff:
        model.Add(sum(shifts[(n, d, s)] * shifts_data[n][d][s][1]
                  for d in all_days for s in all_shifts) <= staff_dict[n]['weekly_ot_limit'])
    # [END at_most_x_hours]
    #
    # =======================================================================================
    #
    # Each staff works at most n hour per day according to daily OT limit.
    # [START at_most_n_hours]
    # for n in all_staff:
    #     for d in all_days:
    #         model.Add(sum(shifts[(n, d, s)] * shifts_data[n][d][s][1]
    #                       for s in all_shifts) <= staff_dict[n]['daily_ot_limit'])
    # [END at_most_n_hours]
    #
    # =======================================================================================
    #
    # Each shiftslot is assigned to at most one staff in the schedule period.
    # [START at_most_one_staff]
    for d in all_days:
        for s in all_shifts:
            model.Add(sum(shifts[(n, d, s)] for n in all_staff) <= 1)
    # [END at_most_one_staff]
    #
    # ==========================================================
    #
    # pylint: disable = g-complex-comprehension
    # Maximize assignment to user that has the highest priority (in terms of absenteeism)
    # [START maximize_assignment_to_user_wrt_priority]
    # model.Maximize(
    #     sum(
    #         shifts[n, d, s] * shifts_data[n][d][s][0] * n
    #         for n in all_staff
    #         for d in all_days
    #         for s in all_shifts
    #     )
    # )
    # [END maximize_assignment_to_user_wrt_priority]
    #
    # Output:
    # Day 0
    # Staff 16 works shift 0 - 12 hours
    # Staff 17 works shift 1 - 8 hours

    # Day 1
    # Staff 15 works shift 2 - 20 hours
    # Staff 16 works shift 3 - 18 hours

    # Day 2
    # Staff 15 works shift 5 - 15 hours
    # Staff 16 works shift 6 - 6 hours
    # Staff 17 works shift 4 - 7 hours

    # Day 3
    # Staff 17 works shift 7 - 12 hours

    # Day 4
    # Staff 14 works shift 9 - 20 hours
    # Staff 17 works shift 8 - 8 hours

    # Day 5
    # Staff 12 works shift 14 - 4 hours
    # Staff 13 works shift 15 - 6 hours
    # Staff 14 works shift 13 - 3 hours
    # Staff 15 works shift 11 - 4 hours
    # Staff 16 works shift 12 - 2 hours
    # Staff 17 works shift 10 - 2 hours

    # Day 6
    # Staff 13 works shift 20 - 4 hours
    # Staff 14 works shift 16 - 8 hours
    # Staff 15 works shift 18 - 3 hours
    # Staff 16 works shift 17 - 2 hours
    # Staff 17 works shift 19 - 1 hours
    # ==========================================================
    #
    # Maximize hours assigned across the week
    # [START maximize_hours_assigned]
    model.Maximize(
        sum(
            shifts[n, d, s] * shifts_data[n][d][s][1]
            for n in all_staff
            for d in all_days
            for s in all_shifts
        )
    )
    # [END maximize_hours_assigned]
    #
    # Output:
    # Day 0
    # Staff 0 works shift 0 - 12 hours
    # Staff 2 works shift 1 - 8 hours

    # Day 1
    # Staff 3 works shift 2 - 20 hours
    # Staff 5 works shift 3 - 18 hours

    # Day 2
    # Staff 1 works shift 6 - 6 hours
    # Staff 2 works shift 4 - 7 hours
    # Staff 16 works shift 5 - 15 hours

    # Day 3
    # Staff 15 works shift 7 - 12 hours

    # Day 4
    # Staff 0 works shift 9 - 20 hours
    # Staff 2 works shift 8 - 8 hours

    # Day 5
    # Staff 0 works shift 10 - 2 hours
    # Staff 1 works shift 14 - 4 hours
    # Staff 2 works shift 15 - 6 hours
    # Staff 3 works shift 13 - 3 hours
    # Staff 4 works shift 12 - 2 hours
    # Staff 15 works shift 11 - 4 hours

    # Day 6
    # Staff 0 works shift 16 - 8 hours
    # Staff 1 works shift 18 - 3 hours
    # Staff 6 works shift 19 - 1 hours
    # Staff 15 works shift 17 - 2 hours
    # Staff 16 works shift 20 - 4 hours
    # ==========================================================

    # Creates the solver and solve.
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 5
    status = solver.Solve(model)

    if (status == cp_model.INFEASIBLE):
        print("\nNot feasible\n")
        print(solver.ResponseStats())
        return print()

    for d in all_days:
        print('Day', d)
        for n in all_staff:
            for s in all_shifts:
                if solver.Value(shifts[(n, d, s)]) == 1:
                    if shifts_data[n][d][s][0] == 1:
                        print('Staff', n, 'works shift',
                              s, '-', shifts_data[n][d][s][1], 'hours')
        print()

    # Statistics.
    print()
    print('Statistics')
    print(solver.ResponseStats())


if __name__ == '__main__':
    main()
