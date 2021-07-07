from ortools.sat.python import cp_model
import random

days = {
    0: [0, 1],
    1: [2, 3],
    2: [4, 5, 6],
    3: [7],
    4: [8, 9, 10],
    5: [11, 12],
    6: [13],

    # 0: [0],
    # 1: [2],
    # 2: [3],
    # 3: [4],
    # 4: [5],
    # 5: [],
    # 6: [1],
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
}

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
    # 9: {'userId': 'marcus_1', 'daily_ot_limit': 8,'weekly_ot_limit': 46},
    # 10: {'userId': 'cherry_1', 'daily_ot_limit': 8,'weekly_ot_limit': 44},
    # 11: {'userId': 'daniel_1', 'daily_ot_limit': 8,'weekly_ot_limit': 46},
    # 12: {'userId': 'elijah_1', 'daily_ot_limit': 8,'weekly_ot_limit': 46},
    # 13: {'userId': 'phillip_1', 'daily_ot_limit': 8,'weekly_ot_limit': 44},
    # 14: {'userId': 'marcel_1', 'daily_ot_limit': 8,'weekly_ot_limit': 46},
    # 15: {'userId': 'winston_1', 'daily_ot_limit': 8,'weekly_ot_limit': 46},
    # 16: {'userId': 'arial_1', 'daily_ot_limit': 8,'weekly_ot_limit': 44},
    # 17: {'userId': 'tina_1', 'daily_ot_limit': 8,'weekly_ot_limit': 46},
}

arr = []
# for staff in range(len(staff_dict)):
#     arr.append([])
#     for day in range(len(days)):
#         arr[staff].append([])
#         for shift in range(len(shiftSlots)):
#             if (shift in days[day]):
#                 arr[staff][day].append(
#                     [
#                         # random.randint(0, 1),
#                         1 if staff % 2 == 0 else 0,
#                         shiftSlots[shift]['hours']
#                     ])
#             else:
#                 arr[staff][day].append([0, 0])

for staff in range(len(staff_dict)):
    arr.append([])
    for day in range(len(days)):
        arr[staff].append([])
        for shift in range(len(shiftSlots)):
            arr[staff][day].append(
                [
                    # random.randint(0, 1),
                    # 1 if staff % 2 == 0 else 0,
                    # eligibility for the shiftslot (filtered by availability and roles)
                    1,
                    shiftSlots[shift]['hours'],
                    random.randint(0, 100),  # ranking
                ])


def main():
    # This program tries to find an optimal assignment of all_staff to shifts
    # (3 shifts per day, for 7 days), subject to some constraints (see below).
    # Each staff can request to be assigned to specific shifts.
    # The optimal assignment maximizes the number of fulfilled shift requests.
    all_staff = range(len(staff_dict))
    all_shifts = range(len(shiftSlots))
    all_days = range(len(days))

    shift_requests = arr
    shift_requests_2 = [  # num of staff = 3
        [  # num of days = 2
            [  # num of shifts = 2
                [1, 55],
                [1, 55],
            ],
            [  # num of shifts = 2
                [1, 30],
                [1, 3],
            ],
            [
                [1, 50],
                [1, 60],
            ],
            [
                [1, 50],
                [1, 60],
            ],
            [
                [1, 50],
                [1, 60],
            ],

        ],
        [
            [
                [1, 24],  # staff 1, day 0, shift 0
                [0, 10],  # staff 1, day 0, shift 1
            ],
            [
                [1, 15],  # staff 1, day 1, shift 0
                [1, 24],  # staff 1, day 1, shift 1
            ],
            [
                [1, 8],
                [1, 3],
            ],
            [
                [1, 8],
                [1, 3],
            ],
            [
                [1, 8],
                [1, 3],
            ],
        ],
        [
            [
                [1, 15],  # staff 2, day 0, shift 0
                [1, 24],  # staff 2, day 0, shift 1
            ],
            [
                [1, 16],  # staff 2, day 1, shift 0
                [1, 3],  # staff 2, day 1, shift 1
            ],
            [
                [1, 8],
                [1, 3],
            ],
            [
                [1, 8],
                [1, 3],
            ],
            [
                [1, 8],
                [1, 3],
            ],
        ],

    ]

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
    # for n in all_staff:
    #     for d in all_days:
    #         model.Add(sum(shifts[(n, d, s)] for s in all_shifts) <= 1)
    # # [END at_most_one_shift]
    #
    # =======================================================================================
    #
    # Each staff works at most n hour per week according to weekly OT limit.
    # [START at_most_n_hours]
    for n in all_staff:
        model.Add(sum(shifts[(n, d, s)] * shift_requests[n][d][s][1]
                  for d in all_days for s in all_shifts) <= staff_dict[n]['weekly_ot_limit'])
    # [END at_most_n_hours]
    #
    # =======================================================================================
    #
    # TODO: Precedence for staff priority (dk how)
    # [START precedence]

    # [END precedence]
    #
    # =======================================================================================
    #
    # Each staff works at most n hour per day according to daily OT limit.
    # [START at_most_n_hours]
    for n in all_staff:
        for d in all_days:
            model.Add(sum(shifts[(n, d, s)] * shift_requests[n][d][s][1]
                          for s in all_shifts) <= staff_dict[n]['daily_ot_limit'])
    # [END at_most_n_hours]
    #
    # =======================================================================================
    #
    # Each shift in a day for a single user should not have overlapping hour.
    # [START no_overlapping_hours_in_day]
    for n in all_staff:
        for d in all_days:
            nooverlap_arr = []

            for s in all_shifts:
                suffix = 'd%is%i' % (s, d)

                start_var = model.NewIntVar(
                    0, shiftSlots[s]['start'], 'start' + suffix)
                end_var = model.NewIntVar(
                    0, shiftSlots[s]['end'] + shiftSlots[s]['start'], 'end' + suffix)

                interval_var = model.NewIntervalVar(start_var, shiftSlots[s]['end'] - shiftSlots[s]['start'],
                                                    end_var, 'interval' + suffix)

                # For precedence, not used
                # all_tasks[job_id, task_id] = task_type(start=start_var,
                #                                        end=end_var,
                #                                        interval=interval_var)
                nooverlap_arr.append(interval_var)

            model.AddNoOverlap(nooverlap_arr)

    # [END no_overlapping_hours_in_day]
    #
    # =======================================================================================
    #

    # Try to distribute the shifts evenly, so that each staff works
    # min_shifts_per_staff shifts. If this is not possible, because the total
    # number of shifts is not divisible by the number of all_staff, some all_staff will
    # be assigned one more shift.
    # min_shifts_per_staff = (len(shiftSlots) * len(days)) // len(all_staff)
    # if len(shiftSlots) * len(days) % len(all_staff) == 0:
    #     max_shifts_per_staff = min_shifts_per_staff
    # else:
    #     max_shifts_per_staff = min_shifts_per_staff + 1
    # for n in all_staff:
    #     num_shifts_worked = 0
    #     for d in all_days:
    #         for s in all_shifts:
    #             num_shifts_worked += shifts[(n, d, s)]
    #     model.Add(min_shifts_per_staff <= num_shifts_worked)
    #     model.Add(num_shifts_worked <= max_shifts_per_staff)

    # ==========================================================
    # Each shiftslot is assigned to at most one staff in the schedule period.
    # [START at_most_one_staff]
    for d in all_days:
        for s in all_shifts:
            model.Add(sum(shifts[(n, d, s)] for n in all_staff) <= 1)
    # [END at_most_one_staff]

    # pylint: disable = g-complex-comprehension
    # Maximize the hours of the entire schedule
    model.Maximize(
        sum(
            shift_requests[n][d][s][1]
            * shift_requests[n][d][s][0]
            * shifts[n, d, s]
            for n in all_staff
            for d in all_days
            for s in all_shifts
        )
    )
    # ==========================================================

    # ==========================================================
    # Each shiftslot is assigned to at most one staff in the schedule period.
    # [START at_most_one_staff]
    # for d in all_days:
    #     for s in all_shifts:
    #         model.Add(sum(shifts[(n, d, s)] for n in all_staff) == 1)
    # # [END at_most_one_staff]

    # # Assign slot to user that has most available slot
    # model.Maximize(
    #     sum(
    #         shifts[n, d, s] * shift_requests[n][d][s][0]
    #         for n in all_staff
    #         for d in all_days
    #         for s in all_shifts
    #     )
    # )
    # ==========================================================

    # Creates the solver and solve.
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 5
    # solver.parameters.cp_model_presolve = False
    status = solver.Solve(model)

    if (status == cp_model.INFEASIBLE):
        print("\nNot feasible")
        print(solver.ResponseStats())
        return print()

    for d in all_days:
        print('Day', d)
        for n in all_staff:
            for s in all_shifts:
                if solver.Value(shifts[n, d, s]) == 1:
                    if shift_requests[n][d][s][0] == 1:
                        print('Staff', n, 'works shift',
                              s, '(with availability).', shift_requests[n][d][s][1])
        print()

    # Statistics.
    print()
    print('Statistics')
    print(solver.ResponseStats())


if __name__ == '__main__':
    main()
