from ortools.sat.python import cp_model
import json

days = {
    # 0: [0, 1],
    # 1: [2],
    # 2: [3],
    # 3: [4, 5, 6],
    # 4: [],
    # 5: [],
    # 6: [],
    0: [0, 1],
    1: [2, 3],
    2: [4, 5, 6],
    3: [7],
    4: [8, 9],
    5: [10, 11, 12, 13, 14, 15],
    6: [16, 17],
}

shiftSlots = {
    0: {'shiftSlotId': 0, 'start': 12, 'end': 20, 'hours': 8},
    1: {'shiftSlotId': 1, 'start': 8, 'end': 16, 'hours': 8},
    2: {'shiftSlotId': 2, 'start': 3, 'end': 5, 'hours': 2},
    3: {'shiftSlotId': 3, 'start': 0, 'end': 18, 'hours': 18},
    4: {'shiftSlotId': 4, 'start': 8, 'end': 15, 'hours': 7},
    5: {'shiftSlotId': 5, 'start': 5, 'end': 20, 'hours': 15},
    6: {'shiftSlotId': 6, 'start': 8, 'end': 14, 'hours': 6},
    7: {'shiftSlotId': 7, 'start': 8, 'end': 16, 'hours': 8},
    8: {'shiftSlotId': 8, 'start': 8, 'end': 16, 'hours': 8},
    9: {'shiftSlotId': 9, 'start': 2, 'end': 22, 'hours': 20},
    10: {'shiftSlotId': 10, 'start': 10, 'end': 18, 'hours': 8},
    11: {'shiftSlotId': 11, 'start': 12, 'end': 20, 'hours': 8},
    12: {'shiftSlotId': 12, 'start': 14, 'end': 22, 'hours': 8},
    13: {'shiftSlotId': 13, 'start': 15, 'end': 18, 'hours': 3},
    14: {'shiftSlotId': 14, 'start': 6, 'end': 10, 'hours': 4},
    15: {'shiftSlotId': 15, 'start': 2, 'end': 8, 'hours': 6},
    16: {'shiftSlotId': 16, 'start': 10, 'end': 18, 'hours': 8},
    17: {'shiftSlotId': 17, 'start': 20, 'end': 22, 'hours': 2},
    # 18: {'shiftSlotId': 18, 'start': 13, 'end': 16, 'hours': 3},
    # 19: {'shiftSlotId': 19, 'start': 2, 'end': 3, 'hours': 1},
    # 20: {'shiftSlotId': 20, 'start': 1, 'end': 5, 'hours': 4},
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
                clashing_shiftSlots = []
                for i in days[day]:
                    if (i == shift):
                        continue
                    # if clashing
                    if (not (shiftSlots[shift]['end'] <= shiftSlots[i][
                            'start'] and shiftSlots[shift]['start'] >= shiftSlots[i]['end'])):
                        clashing_shiftSlots.append(shiftSlots[i])

                shifts_data[staff][day].append(
                    [
                        1,
                        (shiftSlots[shift]['start'], shiftSlots[shift]['end']),
                        clashing_shiftSlots,
                        shiftSlots[shift]['hours']
                    ])
            else:
                shifts_data[staff][day].append(
                    [0, (0, 0), [], 0])

# print(json.dumps(shifts_data[0]))


def main():
    # This program tries to find an optimal assignment of all_staff to shifts
    # Each staff can request to be assigned to specific shifts.
    all_staff = range(len(staff_dict))
    all_shifts = range(len(shiftSlots))
    all_days = range(len(days))

    model = cp_model.CpModel()

    # Creates shift variables.
    # shifts[(n, d, s)]: staff 'n' works shift 's' on day 'd' on hour 'h'
    shifts = {}
    for n in all_staff:
        for d in all_days:
            for s in all_shifts:
                shifts[n, d, s] = model.NewBoolVar(
                    'shift_n%id%is%i' % (n, d, s))

    # =======================================================================================
    #
    # No clashing
    # [START no_clash]
    # for n in all_staff:
    #     for d in all_days:
    #         for s in all_shifts:
    #             model.Add((shifts[n, d, s] *
    #                       len(shifts_data[n][d][s][2])) >= 0)
    # [END no_clash]
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
    # =======================================================================================
    #
    # Each staff works at most n hour per week according to weekly OT limit.
    # [START at_most_x_hours]
    for n in all_staff:
        model.Add(sum(shifts[(n, d, s)] * shifts_data[n][d][s][3]
                  for d in all_days for s in all_shifts) <= staff_dict[n]['weekly_ot_limit'])
    # [END at_most_x_hours]
    #

    for n in all_staff:
        for d in all_days:
            model.Add(sum(shifts[(n, d, s)] * shifts_data[n][d][s][3]
                          for s in all_shifts) <= staff_dict[n]['daily_ot_limit'])

    # =======================================================================================
    #
    # There should not be any clashing shiftSlot within a day
    # [START no_clashing_shiftSlots_within_a_day]
    for n in all_staff:
        for d in all_days:
            for s in days[d]:
                for s1 in days[d]:
                    if (s == s1):
                        continue
                    clash = not (shiftSlots[s]['end'] <= shiftSlots[s1][
                        'start'] or shiftSlots[s]['start'] >= shiftSlots[s1]['end'])

                    if (clash):
                        model.Add(
                            (shifts[n, d, s] + shifts[n, d, s1]) * clash != 2)
    # [END no_clashing_shiftSlots_within_a_day]
    #
    # ======================================================================================
    #
    # Each staff works at most one shift per day.
    # [START at_most_one_shift]
    # NOTE: Work 1 shift per day
    # for n in all_staff:
    #     for d in all_days:
    #         model.Add(sum(shifts[(n, d, s)] for s in days[day]) <= 1)
    # [END at_most_one_shift]
    #

    model.Maximize(
        sum(
            shifts[n, d, s] * shifts_data[n][d][s][0] * n
            for n in all_staff
            for d in all_days
            for s in all_shifts
        )
    )

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
                if solver.Value(shifts[n, d, s]) == 1:
                    if shifts_data[n][d][s][0] == 1:
                        print('Staff', n, 'works shift',
                              s, '-', shifts_data[n][d][s][1], 'hours')

                    else:
                        print("WF")
        print()

    # Statistics.
    print()
    print('Statistics')
    print(solver.ResponseStats())


if __name__ == '__main__':
    main()
