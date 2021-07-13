# This example is based on the simplified shift structure of QA Employment
from ortools.sat.python import cp_model

num_shiftSlots_per_day = 9  # NOTE: n should be a multiple of 3
days = {
    0: range(0, num_shiftSlots_per_day),
    1: range(num_shiftSlots_per_day, num_shiftSlots_per_day*2),
    2: range(num_shiftSlots_per_day*2, num_shiftSlots_per_day*3),
    3: range(num_shiftSlots_per_day*3, num_shiftSlots_per_day*4),
    4: range(num_shiftSlots_per_day*4, num_shiftSlots_per_day*5),
    5: range(num_shiftSlots_per_day*5, num_shiftSlots_per_day*6),
    6: range(num_shiftSlots_per_day*6, num_shiftSlots_per_day*7),
}

shiftSlots = {}
# Create num_shiftSlots_per_day number of shift slot which consist of
# 1/3 of 0700-1500, 1/3 of 1300-2100 and 1/3 of 2100+0700(+1)
for day in range(len(days)):
    for shiftSlotId in days[day]:
        if (shiftSlotId % num_shiftSlots_per_day < num_shiftSlots_per_day / 3):
            # TODO: convert start/end/hours to minutes to handle 12:15 / 12:30 shift
            shiftSlots[shiftSlotId] = {
                'shiftSlotId': shiftSlotId,
                'start': 7,
                'end': 15,
                'hours': 8
            }
            continue

        if (shiftSlotId % num_shiftSlots_per_day < num_shiftSlots_per_day / 3 * 2):
            shiftSlots[shiftSlotId] = {
                'shiftSlotId': shiftSlotId,
                'start': 13,
                'end': 21,
                'hours': 8
            }
            continue

        shiftSlots[shiftSlotId] = {
            'shiftSlotId': shiftSlotId,
            'start': 21,
            'end': 7,
            'hours': 10
        }

# score can be a weighted score of multiple metrics combined (x out of 100)
staff_dict = {
    # TODO: convert daily_ot_limit/weekly_ot_limit to minutes
    0: {'userId': 'marcus', 'daily_ot_limit': 8, 'weekly_ot_limit': 46, 'score': 1, 'fulltime': 1},
    1: {'userId': 'cherry', 'daily_ot_limit': 8, 'weekly_ot_limit': 44, 'score': 2, 'fulltime': 1},
    2: {'userId': 'daniel', 'daily_ot_limit': 8, 'weekly_ot_limit': 46, 'score': 3, 'fulltime': 1},
    3: {'userId': 'elijah', 'daily_ot_limit': 10, 'weekly_ot_limit': 46, 'score': 4, 'fulltime': 1},
    4: {'userId': 'phillip', 'daily_ot_limit': 8, 'weekly_ot_limit': 44, 'score': 5, 'fulltime': 1},
    5: {'userId': 'marcel', 'daily_ot_limit': 8, 'weekly_ot_limit': 46, 'score': 6, 'fulltime': 1},
    6: {'userId': 'winston', 'daily_ot_limit': 10, 'weekly_ot_limit': 46, 'score': 7, 'fulltime': 1},
    7: {'userId': 'arial', 'daily_ot_limit': 8, 'weekly_ot_limit': 44, 'score': 8, 'fulltime': 1},
    8: {'userId': 'tina', 'daily_ot_limit': 10, 'weekly_ot_limit': 46, 'score': 9, 'fulltime': 1},
    9: {'userId': 'marcus_1', 'daily_ot_limit': 8, 'weekly_ot_limit': 46, 'score': 10, 'fulltime': 0},
    10: {'userId': 'cherry_1', 'daily_ot_limit': 8, 'weekly_ot_limit': 44, 'score': 11, 'fulltime': 0},
    11: {'userId': 'daniel_1', 'daily_ot_limit': 10, 'weekly_ot_limit': 46, 'score': 12, 'fulltime': 0},
    12: {'userId': 'elijah_1', 'daily_ot_limit': 8, 'weekly_ot_limit': 46, 'score': 13, 'fulltime': 0},
    13: {'userId': 'phillip_1', 'daily_ot_limit': 8, 'weekly_ot_limit': 44, 'score': 14, 'fulltime': 0},
    14: {'userId': 'marcel_1', 'daily_ot_limit': 8, 'weekly_ot_limit': 46, 'score': 15, 'fulltime': 0},
    15: {'userId': 'winston_1', 'daily_ot_limit': 10, 'weekly_ot_limit': 46, 'score': 16, 'fulltime': 0},
    16: {'userId': 'arial_1', 'daily_ot_limit': 8, 'weekly_ot_limit': 44, 'score': 17, 'fulltime': 0},
    17: {'userId': 'tina_1', 'daily_ot_limit': 10, 'weekly_ot_limit': 46, 'score': 18, 'fulltime': 0},
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
                        shiftSlots[shift]['hours'],
                        (shiftSlots[shift]['start'], shiftSlots[shift]['end']),
                    ])
            else:
                shifts_data[staff][day].append(
                    [0, 0, (0, 0)])

# print(json.dumps(shifts_data[0]))


def main():
    # This program tries to find an optimal assignment of all_staff to shifts
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
    # Constraint 1:
    # - Each shiftslot is assigned to at most one staff.
    # [START at_most_one_staff]
    for d in all_days:
        for s in all_shifts:
            # Constraint 1
            model.Add(sum(shifts[(n, d, s)] for n in all_staff) <= 1)
    # [END at_most_one_staff]
    #
    # =======================================================================================
    #
    # Constraint 2:
    # - Each staff works at most n hour per week according to weekly OT limit.
    # [START at_most_n_weekly_hours]
    for n in all_staff:
        # Constraint 2
        model.Add(sum(shifts[(n, d, s)] * shifts_data[n][d][s][1]
                  for d in all_days for s in all_shifts) <= staff_dict[n]['weekly_ot_limit'])
    # [END at_most_n_weekly_hours]
    #
    # =======================================================================================
    #
    # Constraint 3:
    # - Each staff works at most m hour per day according to daily OT limit.
    # [START at_most_m_daily_hours]
    for n in all_staff:
        for d in all_days:
            # Constraint 3
            model.Add(sum(shifts[(n, d, s)] * shifts_data[n][d][s][1]
                          for s in all_shifts) <= staff_dict[n]['daily_ot_limit'])
    # [END at_most_m_daily_hours]
    #
    # =======================================================================================
    #
    # Constraint 4:
    # - There should not be any clashing shiftSlot within a day
    # [START no_clashing_shiftSlots_within_a_day]
    for n in all_staff:
        for d in all_days:
            for s in days[d]:
                for s1 in days[d]:
                    if (s == s1):
                        continue
                    clash = not (shiftSlots[s]['end'] <= shiftSlots[s1][
                        'start'] or shiftSlots[s]['start'] >= shiftSlots[s1]['end'])
                    # Constraint 4
                    model.Add(
                        (shifts[n, d, s] + shifts[n, d, s1]) * clash != 2)
    # [END no_clashing_shiftSlots_within_a_day]
    #
    # ======================================================================================
    #
    # Constraint 5:
    # - There should not be any clashing shiftSlot across 2 consecutive day
    # Constraint 6:
    # - There should be atleast a 7 hours gap between end of shift for previous day and start of shift for next day
    # [START no_clashing_shiftSlots_across_day AND enforce_7_hours_gap_for_shiftSlots_across_day]
    for n in all_staff:
        for d in all_days:
            for s in days[d]:
                for s1 in days[(d+1) % 7]:
                    overnight_shiftSlot = shiftSlots[s]['end'] < shiftSlots[s]['start']

                    if (overnight_shiftSlot):
                        clashing_across_day = shiftSlots[s]['end'] > shiftSlots[s1]['start']
                        # Constraint 5
                        model.Add(
                            (shifts[n, d, s] + shifts[n, (d+1) % 7, s1]) * clashing_across_day != 2)

                        less_than_7_hours_gap = (
                            shiftSlots[s1]['start'] - shiftSlots[s]['end']) < 7

                        # Constraint 6
                        model.Add(
                            (shifts[n, d, s] + shifts[n, (d+1) % 7, s1]) *
                            less_than_7_hours_gap != 2
                        )
    # [END no_clashing_shiftSlots_across_day AND enforce_7_hours_gap_for_shiftSlots_across_day]
    #
    # ======================================================================================
    #
    # Constraint 7:
    # - User should not be assigned shiftSlots for 5 consecutive days
    # [START no_5_consecutive_days]
    for n in all_staff:
        for d in all_days:
            # Constraint 7
            model.Add(sum(shifts[n, (d + d1) % 7, s]
                      for d1 in range(5) for s in all_shifts) < 5)
    # [END no_5_consecutive_days]
    #
    # ======================================================================================

    # Objective 1: Maximize assignment of shiftSlot to user with higher score
    # By maximizing the score of user, the algorithm will prioritize assignment to user
    # with the highest score
    # model.Maximize(
    #     sum(
    #         shifts[n, d, s] * shifts_data[n][d][s][0] * staff_dict[n]['score']
    #         # adding 100 to full-timer to give precedence for full-timer over part-timer
    #         # (staff_dict[n]['score'] + (100 if staff_dict[n]
    #         #  ['fulltime'] == 1 else 0))
    #         for n in all_staff
    #         for d in all_days
    #         for s in all_shifts
    #     )
    # )

    # Objective 2: Maximize assignment of shiftSlot to user with higher score with full-timer prioritization
    # Similar to Objective 1 but if the user is a full-timer, prioritize the full-timer first
    # before considering the score.
    model.Maximize(
        sum(
            shifts[n, d, s] * shifts_data[n][d][s][0] *
            # adding 100 to full-timer to give precedence for full-timer over part-timer
            (staff_dict[n]['score'] + (100 if staff_dict[n]
             ['fulltime'] == 1 else 0))
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

    output = {}
    for n in all_staff:
        output[n] = []

    for d in all_days:
        print('Day', d)
        for n in all_staff:
            for s in all_shifts:
                if solver.Value(shifts[n, d, s]) == 1:
                    if shifts_data[n][d][s][0] == 1:
                        print('Staff', n, 'works shift',
                              s, '-', shifts_data[n][d][s][1], 'hours', shifts_data[n][d][s][2])
                        output[n].append(s)

        print()

    print(output)

    # Statistics.
    print()
    print('Statistics')
    print(solver.ResponseStats())


if __name__ == '__main__':
    main()