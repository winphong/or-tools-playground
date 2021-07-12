# NOTE: Not working
from ortools.sat.python import cp_model
import json

days = {
    0: [0, 1],
    1: [2],
    2: [],
    3: [],
    4: [],
    5: [],
    6: [],
    # 0: [0, 1],
    # 1: [2, 3],
    # 2: [4, 5, 6],
    # 3: [7],
    # 4: [8, 9],
    # 5: [10, 11, 12, 13, 14, 15],
    # 6: [16, 17, 18, 19, 20],
}

shiftSlots = {
    0: {'shiftSlotId': 0, 'start': 18, 'end': 20, 'hours': 2},
    1: {'shiftSlotId': 1, 'start': 8, 'end': 16, 'hours': 8},
    2: {'shiftSlotId': 2, 'start': 3, 'end': 5, 'hours': 2},
    # 3: {'shiftSlotId': 3, 'start': 0, 'end': 18, 'hours': 18},
    # 4: {'shiftSlotId': 4, 'start': 8, 'end': 15, 'hours': 7},
    # 5: {'shiftSlotId': 5, 'start': 5, 'end': 20, 'hours': 15},
    # 6: {'shiftSlotId': 6, 'start': 8, 'end': 14, 'hours': 6},
    # 7: {'shiftSlotId': 7, 'start': 8, 'end': 20, 'hours': 12},
    # 8: {'shiftSlotId': 8, 'start': 8, 'end': 16, 'hours': 8},
    # 9: {'shiftSlotId': 9, 'start': 2, 'end': 22, 'hours': 20},
    # 10: {'shiftSlotId': 10, 'start': 12, 'end': 14, 'hours': 2},
    # 11: {'shiftSlotId': 11, 'start': 6, 'end': 10, 'hours': 4},
    # 12: {'shiftSlotId': 12, 'start': 2, 'end': 4, 'hours': 2},
    # 13: {'shiftSlotId': 13, 'start': 15, 'end': 18, 'hours': 3},
    # 14: {'shiftSlotId': 14, 'start': 6, 'end': 10, 'hours': 4},
    # 15: {'shiftSlotId': 15, 'start': 2, 'end': 8, 'hours': 6},
    # 16: {'shiftSlotId': 16, 'start': 10, 'end': 18, 'hours': 8},
    # 17: {'shiftSlotId': 17, 'start': 20, 'end': 22, 'hours': 2},
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

hourBreakdown = {
    #   0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19 20 21 22 23
    1: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    2: [0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    3: [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    4: [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
}


shifts_data = []
for staff in range(len(staff_dict)):
    shifts_data.append([])
    for day in range(len(days)):
        shifts_data[staff].append([])
        for shift in range(len(shiftSlots)):
            if (shift in days[day]):

                other_shiftSlots_in_day = []
                for x in days[day]:
                    if (x != shift):
                        other_shiftSlots_in_day.append(x)

                other_shiftSlots_as_tuple = []
                for t in other_shiftSlots_in_day:
                    other_shiftSlots_as_tuple.append(
                        (shiftSlots[t]['start'], shiftSlots[t]['end']))

                shifts_data[staff][day].append(
                    [
                        1,
                        (shiftSlots[shift]['start'], shiftSlots[shift]['end']),
                        other_shiftSlots_as_tuple
                    ])
            else:
                shifts_data[staff][day].append(
                    [0, (0, 0), []])

# for staff in range(len(staff_dict)):
#     shifts_data.append([])
#     for day in range(len(days)):
#         shifts_data[staff].append([])
#         for shift in range(len(shiftSlots)):
#             shifts_data[staff][day].append(
#                 [1, (2, 5), [(3, 10), (9, 12), (15, 19)]])

print(json.dumps(shifts_data[0]))


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

    # shifts_w_hours[(n, d, s, h)]: staff 'n' works shift 's' on day 'd' on hour 'h'
    # shifts_w_hours = {}
    # for n in all_staff:
    #     for d in all_days:
    #         for s in all_shifts:
    #             for h in all_hours:
    #                 shifts_w_hours[n, d, s, h] = model.NewBoolVar(
    #                     'shift_with_hours_n%id%is%ih%i' % (n, d, s, h))

    # Each staff works at most one shift per day.
    # [START at_most_one_shift]
    for n in all_staff:
        for d in all_days:
            model.Add(sum(shifts[(n, d, s)] for s in all_shifts) <= 1)
    # [END at_most_one_shift]
    #
    # =======================================================================================
     # Each staff works at most one shift per day.
    # [START at_most_one_shift]
    for n in all_staff:
        for d in all_days:
            for s in all_shifts:
                actual = shifts_data[n][d][s][1]
                no_clash = True
                for i in range(len(shifts_data[n][d][s][2])):
                    no_clash = no_clash and actual[1] <= shifts_data[n][d][
                        s][2][i][0] and actual[0] >= shifts_data[n][d][s][2][i][1]

                if (shifts_data[n][d][s][0] == 0):
                    no_clash: False

                model.Add(shifts[(n, d, s)] * no_clash == 1)

    # [END at_most_one_shift]
    #
    # =======================================================================================

    # Creates the solver and solve.
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 5
    status = solver.Solve(model)

    if (status == cp_model.INFEASIBLE):
        print("\nNot feasible\n")
        print(solver.ResponseStats())
        return print()

    # for d in all_days:
    #     print('Day', d)
    #     for n in all_staff:
    #         for s in all_shifts:
    #             if solver.Value(shifts[(n, d, s)]) == 1:
    #                 if shifts_data[n][d][s][0] == 1:
    #                     print('Staff', n, 'works shift',
    #                           s, '-', shifts_data[n][d][s][1], 'hours')

    #                 else:
    #                     print("WF")
    #     print()

    # Statistics.
    print()
    print('Statistics')
    print(solver.ResponseStats())


if __name__ == '__main__':
    main()
