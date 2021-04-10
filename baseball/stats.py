from collections import namedtuple

from baseball.baseball_events import Pickoff, RunnerAdvance, Pitch

NOT_AT_BAT_CODE_LIST = ['SH', 'SF', 'BB', 'CI', 'FI', 'IBB', 'HBP', 'CS', 'PO']
HIT_CODE_LIST = ['1B', '2B', '3B', 'HR']
NON_STRIKE_LIST = ['Ball', 'Intent Ball', 'Automatic Ball', 'Ball In Dirt',
                   'Hit By Pitch']

InningStatsTuple = namedtuple('InningStatsTuple', 'S P BB K LOB E H R')
BatterBoxScore = namedtuple('BatterBoxScore', 'AB R H RBI BB SO LOB')
PitcherBoxScore = namedtuple(
    'PitcherBoxScore',
    'IP WLS BF H R ER SO BB IBB HBP BLK WP HR S P ERA WHIP'
)

TeamBoxScore = namedtuple(
    'TeamBoxScore',
    'B1 B2 B3 HR SF SAC DP HBP WP PB SB CS PA'
)

def process_pickoffs(plate_appearance, first_base, second_base, third_base):
    for event in plate_appearance.event_list:
        if (isinstance(event, Pickoff) and
                event.pickoff_was_successful):
            if event.pickoff_base == '1B':
                first_base = None
            elif event.pickoff_base == '2B':
                second_base = None
            elif event.pickoff_base == '3B':
                third_base = None
        elif (isinstance(event, RunnerAdvance) and
              'Picked off stealing' in event.run_description):
            if event.start_base == '1B':
                first_base = None
            elif event.start_base == '2B':
                second_base = None
            elif event.start_base == '3B':
                third_base = None

    return first_base, second_base, third_base

def process_baserunners(plate_appearance, last_plate_appearance,
                        first_base, second_base, third_base):
    first_base_list = [first_base] if first_base else []
    second_base_list = [second_base] if second_base else []
    third_base_list = [third_base] if third_base else []
    for event in plate_appearance.event_list:
        if isinstance(event, RunnerAdvance):
            if (plate_appearance == last_plate_appearance and
                    ('out' in event.run_description or
                     'Out' in event.run_description)):
                break
            else:
                if event.end_base == '1B':
                    first_base_list.append(event.runner)
                elif event.end_base == '2B':
                    second_base_list.append(event.runner)
                    if event.runner in first_base_list:
                        first_base_list.remove(event.runner)
                elif event.end_base == '3B':
                    third_base_list.append(event.runner)
                    if event.runner in first_base_list:
                        first_base_list.remove(event.runner)
                    if event.runner in second_base_list:
                        second_base_list.remove(event.runner)
                elif event.end_base == '' or 'score':
                    if event.runner in first_base_list:
                        first_base_list.remove(event.runner)
                    if event.runner in second_base_list:
                        second_base_list.remove(event.runner)
                    if event.runner in third_base_list:
                        third_base_list.remove(event.runner)

    if first_base_list:
        first_base = first_base_list[0]
    else:
        first_base = None

    if second_base_list:
        second_base = second_base_list[0]
    else:
        second_base = None

    if third_base_list:
        third_base = third_base_list[0]
    else:
        third_base = None

    return first_base, second_base, third_base

def get_inning_half_list(game, inning_half_str):
    if inning_half_str == 'top':
        inning_half_list = [inning.top_half_appearance_list
                            for inning in game.inning_list]
    elif inning_half_str == 'bottom':
        inning_half_list = [inning.bottom_half_appearance_list
                            for inning in game.inning_list
                            if inning.bottom_half_appearance_list]
    else:
        raise ValueError(
            'Invalid inning half str: {}'.format(inning_half_str)
        )

    return inning_half_list

def get_half_inning_stats(top_half_appearance_list,
                          bottom_half_appearance_list):
    if top_half_appearance_list:
        top_half_inning_stats = InningStatsTuple(
            get_strikes(top_half_appearance_list),
            get_pitches(top_half_appearance_list),
            get_walks(top_half_appearance_list),
            get_strikeouts(top_half_appearance_list),
            get_lob(top_half_appearance_list),
            get_errors(top_half_appearance_list),
            get_hits(top_half_appearance_list),
            get_runs(top_half_appearance_list)
        )
    else:
        top_half_inning_stats = None

    if bottom_half_appearance_list:
        bottom_half_inning_stats = InningStatsTuple(
            get_strikes(bottom_half_appearance_list),
            get_pitches(bottom_half_appearance_list),
            get_walks(bottom_half_appearance_list),
            get_strikeouts(bottom_half_appearance_list),
            get_lob(bottom_half_appearance_list),
            get_errors(bottom_half_appearance_list),
            get_hits(bottom_half_appearance_list),
            get_runs(bottom_half_appearance_list)
        )
    else:
        bottom_half_inning_stats = None

    return top_half_inning_stats, bottom_half_inning_stats

def get_all_pitcher_stats(game, team, pitcher, inning_half_str):
    inning_half_list = get_inning_half_list(game, inning_half_str)

    pitcher_box_score = PitcherBoxScore(
        get_pitcher_innings_pitched(pitcher, inning_half_list),
        get_pitcher_win_loss_save(pitcher, team),
        get_pitcher_batters_faced(pitcher, inning_half_list),
        get_pitcher_hits(pitcher, inning_half_list),
        get_pitcher_runs(pitcher, inning_half_list),
        get_pitcher_earned_runs(pitcher, inning_half_list),
        get_pitcher_strikeouts(pitcher, inning_half_list),
        get_pitcher_nonintentional_walks(pitcher, inning_half_list),
        get_pitcher_intentional_walks(pitcher, inning_half_list),
        get_pitcher_hit_by_pitch(pitcher, inning_half_list),
        get_pitcher_balks(pitcher, inning_half_list),
        get_pitcher_wild_pitches(pitcher, inning_half_list),
        get_pitcher_home_runs(pitcher, inning_half_list),
        get_pitcher_strikes(pitcher, inning_half_list),
        get_pitcher_pitches(pitcher, inning_half_list),
        get_pitcher_era(pitcher, inning_half_list),
        get_pitcher_whip(pitcher, inning_half_list)
    )

    return pitcher_box_score

def get_all_batter_stats(game, batter, inning_half_str):
    inning_half_list = get_inning_half_list(game, inning_half_str)

    batter_box_score = BatterBoxScore(
        get_batter_at_bats(batter, inning_half_list),
        get_batter_runs(batter, inning_half_list),
        get_batter_hits(batter, inning_half_list),
        get_batter_runs_batted_in(batter, inning_half_list),
        get_batter_walks(batter, inning_half_list),
        get_batter_strikeouts(batter, inning_half_list),
        get_batter_lob(batter, inning_half_list)
    )

    return batter_box_score

def get_box_score_total(box_score_dict):
    total_ab = 0
    total_r = 0
    total_h = 0
    total_rbi = 0
    total_bb = 0
    total_so = 0
    total_lob = 0

    for box_score in box_score_dict.values():
        total_ab += box_score.AB
        total_r += box_score.R
        total_h += box_score.H
        total_rbi += box_score.RBI
        total_bb += box_score.BB
        total_so += box_score.SO
        total_lob += box_score.LOB

    box_score_total_tuple = BatterBoxScore(total_ab,
                                           total_r,
                                           total_h,
                                           total_rbi,
                                           total_bb,
                                           total_so,
                                           total_lob)

    return box_score_total_tuple

def get_batter_strikeouts(batter, inning_half_list):
    num_strikeouts = 0

    for inning_half in inning_half_list:
        for plate_appearance in inning_half:
            if batter == plate_appearance.batter:
                if ('K' in plate_appearance.scorecard_summary or
                        'ꓘ' in plate_appearance.scorecard_summary):
                    num_strikeouts += 1

    return num_strikeouts

def get_batter_walks(batter, inning_half_list):
    num_walks = 0

    for inning_half in inning_half_list:
        for plate_appearance in inning_half:
            if batter == plate_appearance.batter:
                if 'BB' in plate_appearance.scorecard_summary:
                    num_walks += 1

    return num_walks

def get_batter_runs_batted_in(batter, inning_half_list):
    num_rbis = 0

    for inning_half in inning_half_list:
        for plate_appearance in inning_half:
            if batter == plate_appearance.batter:
                num_rbis += len(plate_appearance.runners_batted_in_list)

    return num_rbis

def plate_appearance_is_hit(plate_appearance):
    is_hit = False

    for code in HIT_CODE_LIST:
        if code in plate_appearance.scorecard_summary:
            is_hit = True

    return is_hit

def get_batter_hits(batter, inning_half_list):
    num_hits = 0

    for inning_half in inning_half_list:
        for plate_appearance in inning_half:
            if (batter == plate_appearance.batter and
                    plate_appearance_is_hit(plate_appearance)):
                num_hits += 1

    return num_hits

def get_batter_runs(batter, inning_half_list):
    num_runs = 0

    for inning_half in inning_half_list:
        for plate_appearance in inning_half:
            if batter in plate_appearance.scoring_runners_list:
                num_runs += 1

    return num_runs

def is_at_bat(plate_appearance):
    at_bat_flag = True

    if plate_appearance.plate_appearance_summary == 'Runner Out':
        at_bat_flag = False

    for code in NOT_AT_BAT_CODE_LIST:
        if plate_appearance.scorecard_summary.startswith(code):
            at_bat_flag = False

    return at_bat_flag

def get_batter_at_bats(batter, inning_half_list):
    at_bats = 0

    for inning_half in inning_half_list:
        for plate_appearance in inning_half:
            if (batter == plate_appearance.batter and
                    is_at_bat(plate_appearance)):
                at_bats += 1

    return at_bats

def get_batter_lob(batter, inning_half_list):
    player_lob = 0

    for inning_half in inning_half_list:
        first_base = None
        second_base = None
        third_base = None

        for plate_appearance in inning_half:
            (first_base,
             second_base,
             third_base) = process_pickoffs(plate_appearance,
                                            first_base,
                                            second_base,
                                            third_base)

            if (not plate_appearance_is_hit(plate_appearance) and
                    'BB' not in plate_appearance.scorecard_summary and
                    'HBP' not in plate_appearance.scorecard_summary):
                num_lob = 0

                if first_base:
                    num_lob += 1

                if second_base:
                    num_lob += 1

                if third_base:
                    num_lob += 1

                num_lob -= len(plate_appearance.scoring_runners_list)

                if (batter == plate_appearance.batter and
                        is_at_bat(plate_appearance)):
                    player_lob += num_lob

            (first_base,
             second_base,
             third_base) = process_baserunners(plate_appearance,
                                               inning_half[-1],
                                               first_base,
                                               second_base,
                                               third_base)

    return player_lob

def get_ip_incr(num_innings_pitched):
    if num_innings_pitched % 10 < 2:
        increment = 1
    elif num_innings_pitched % 10 == 2:
        increment = 8
    else:
        increment = 0

    return increment

def get_pitcher_innings_pitched(pitcher, inning_half_list):
    innings_pitched = 0
    for inning_half in inning_half_list:
        num_outs = 0
        for plate_appearance in inning_half:
            this_plate_appearance_outs = plate_appearance.inning_outs - num_outs
            num_outs += this_plate_appearance_outs

            if pitcher == plate_appearance.pitcher:
                for _ in range(this_plate_appearance_outs):
                    innings_pitched += get_ip_incr(innings_pitched)

    return innings_pitched / 10

def get_pitcher_win_loss_save(pitcher, team):
    for pitcher_appearance in team.pitcher_list:
        if pitcher_appearance.player_obj == pitcher:
            return pitcher_appearance.pitcher_credit_code

    raise ValueError('Invalid pitcher')

def get_pitcher_batters_faced(pitcher, inning_half_list):
    num_batters_faced = 0

    for inning_half in inning_half_list:
        for plate_appearance in inning_half:
            if (pitcher == plate_appearance.pitcher and
                    'CS' not in plate_appearance.scorecard_summary and
                    'PO' not in plate_appearance.scorecard_summary):
                num_batters_faced += 1

    return num_batters_faced

def get_pitcher_hits(pitcher, inning_half_list):
    num_hits = 0

    for inning_half in inning_half_list:
        for plate_appearance in inning_half:
            if (pitcher == plate_appearance.pitcher and
                    plate_appearance_is_hit(plate_appearance)):
                num_hits += 1

    return num_hits

def get_pitcher_runs(pitcher, inning_half_list):
    num_runs = 0

    for inning_half in inning_half_list:
        if inning_half:
            inning_start_pitcher = inning_half[0].pitcher
            pitcher_change_flag = False
            first_base, second_base, third_base = None, None, None

            for plate_appearance in inning_half:
                if (plate_appearance.pitcher != inning_start_pitcher and
                        not pitcher_change_flag):
                    pitcher_change_flag = True

                    change_baserunner_count = sum(
                        x is not None
                        for x in [first_base, second_base, third_base]
                    )

                (first_base,
                 second_base,
                 third_base) = process_baserunners(plate_appearance,
                                                   inning_half[-1],
                                                   first_base,
                                                   second_base,
                                                   third_base)

                for event in plate_appearance.event_list:
                    if (isinstance(event, RunnerAdvance) and
                            event.runner_scored):
                        if pitcher_change_flag and change_baserunner_count:
                            change_baserunner_count -= 1
                            if (plate_appearance.pitcher != pitcher and
                                    inning_start_pitcher == pitcher):
                                num_runs += 1

                        elif pitcher == plate_appearance.pitcher:
                            num_runs += 1

    return num_runs

def get_pitcher_errors(pitcher, inning_half_list):
    num_errors = 0

    for inning_half in inning_half_list:
        for plate_appearance in inning_half:
            if pitcher == plate_appearance.pitcher:
                if plate_appearance.error_str == 'E1':
                    num_errors += 1

                last_description = None

                for event in plate_appearance.event_list:
                    if isinstance(event, RunnerAdvance):
                        if ('Pickoff Error' in event.run_description and
                                last_description != event.run_description):
                            num_errors += 1
                            last_description = event.run_description
                    else:
                        last_description = None

    return num_errors

def get_pitcher_earned_runs(pitcher, inning_half_list):
    num_er = 0

    for inning_half in inning_half_list:
        if inning_half:
            inning_start_pitcher = inning_half[0].pitcher
            pitcher_change_flag = False
            first_base, second_base, third_base = None, None, None

            for plate_appearance in inning_half:
                if (plate_appearance.pitcher != inning_start_pitcher and
                        not pitcher_change_flag):
                    pitcher_change_flag = True

                    change_baserunner_count = sum(
                        x is not None
                        for x in [first_base, second_base, third_base]
                    )

                (first_base,
                 second_base,
                 third_base) = process_baserunners(plate_appearance,
                                                   inning_half[-1],
                                                   first_base,
                                                   second_base,
                                                   third_base)

                for event in plate_appearance.event_list:
                    if (isinstance(event, RunnerAdvance) and
                            event.runner_scored and
                            event.run_earned):
                        if pitcher_change_flag and change_baserunner_count:
                            if (plate_appearance.pitcher != pitcher and
                                    inning_start_pitcher == pitcher):
                                num_er += 1

                            change_baserunner_count -= 1
                        elif pitcher == plate_appearance.pitcher:
                            num_er += 1

    return num_er

def get_pitcher_strikeouts(pitcher, inning_half_list):
    num_strikeouts = 0

    for inning_half in inning_half_list:
        for plate_appearance in inning_half:
            summary = plate_appearance.plate_appearance_summary

            if (pitcher == plate_appearance.pitcher and
                    'Strikeout' in summary):
                num_strikeouts += 1

    return num_strikeouts

def get_pitcher_nonintentional_walks(pitcher, inning_half_list):
    num_walks = 0

    for inning_half in inning_half_list:
        for plate_appearance in inning_half:
            summary = plate_appearance.plate_appearance_summary

            if pitcher == plate_appearance.pitcher and summary == 'Walk':
                num_walks += 1

    return num_walks

def get_pitcher_intentional_walks(pitcher, inning_half_list):
    num_intent_walks = 0

    for inning_half in inning_half_list:
        for plate_appearance in inning_half:
            summary = plate_appearance.plate_appearance_summary

            if (pitcher == plate_appearance.pitcher and
                    summary == 'Intent Walk'):
                num_intent_walks += 1

    return num_intent_walks

def get_pitcher_hit_by_pitch(pitcher, inning_half_list):
    num_hbp = 0

    for inning_half in inning_half_list:
        for plate_appearance in inning_half:
            summary = plate_appearance.plate_appearance_summary

            if (pitcher == plate_appearance.pitcher and
                    summary == 'Hit By Pitch'):
                num_hbp += 1

    return num_hbp

def get_pitcher_balks(pitcher, inning_half_list):
    num_balks = 0

    for inning_half in inning_half_list:
        for plate_appearance in inning_half:
            if pitcher == plate_appearance.pitcher:
                last_description = None

                for event in plate_appearance.event_list:
                    if isinstance(event, RunnerAdvance):
                        if (event.run_description == 'Balk' and
                                last_description != event.run_description):
                            num_balks += 1
                            last_description = event.run_description
                    else:
                        last_description = None

    return num_balks

def get_pitcher_wild_pitches(pitcher, inning_half_list):
    num_wp = 0

    for inning_half in inning_half_list:
        for plate_appearance in inning_half:
            if pitcher == plate_appearance.pitcher:
                last_description = None

                for event in plate_appearance.event_list:
                    if isinstance(event, RunnerAdvance):
                        if (event.run_description == 'Wild Pitch' and
                                last_description != event.run_description):
                            num_wp += 1
                            last_description = event.run_description
                    else:
                        last_description = None

    return num_wp

def get_pitcher_home_runs(pitcher, inning_half_list):
    num_hr = 0

    for inning_half in inning_half_list:
        for plate_appearance in inning_half:
            if (pitcher == plate_appearance.pitcher and
                    plate_appearance.scorecard_summary == 'HR'):
                num_hr += 1

    return num_hr

def get_pitcher_strikes(pitcher, inning_half_list):
    num_strikes = 0

    for inning_half in inning_half_list:
        for plate_appearance in inning_half:
            if pitcher == plate_appearance.pitcher:
                for event in plate_appearance.event_list:
                    if (isinstance(event, Pitch) and
                            event.pitch_description not in NON_STRIKE_LIST):
                        num_strikes += 1

    return num_strikes

def get_pitcher_pitches(pitcher, inning_half_list):
    num_pitches = 0

    for inning_half in inning_half_list:
        for plate_appearance in inning_half:
            if pitcher == plate_appearance.pitcher:
                for event in plate_appearance.event_list:
                    if (isinstance(event, Pitch) and
                            event.pitch_description != 'Automatic Ball'):
                        num_pitches += 1

    return num_pitches

def get_innings_pitched_calc_num(pitcher, inning_half_list):
    innings_pitched = get_pitcher_innings_pitched(pitcher,
                                                  inning_half_list)

    if str(innings_pitched)[-2:] == '.1':
        innings_pitched_num = float(str(innings_pitched)[:-2]) + (1.0/3.0)
    elif str(innings_pitched)[-2:] == '.2':
        innings_pitched_num = float(str(innings_pitched)[:-2]) + (2.0/3.0)
    else:
        innings_pitched_num = innings_pitched

    return innings_pitched_num

def get_pitcher_era(pitcher, inning_half_list):
    if get_pitcher_innings_pitched(pitcher, inning_half_list) == 0:
        era = '&#8734;'
    else:
        innings_pitched_num = get_innings_pitched_calc_num(pitcher,
                                                           inning_half_list)

        era = round(
            9.0 *
            (
                float(get_pitcher_earned_runs(pitcher, inning_half_list)) /
                innings_pitched_num
            ),
            3
        )

    return era

def get_pitcher_whip(pitcher, inning_half_list):
    num_hits = get_pitcher_hits(pitcher, inning_half_list)
    num_walks = get_pitcher_nonintentional_walks(pitcher,
                                                 inning_half_list)

    innings_pitched_num = get_innings_pitched_calc_num(
        pitcher,
        inning_half_list
    )

    if innings_pitched_num == 0:
        whip = '&#8734;'
    else:
        whip = round(
            float(num_hits + num_walks) / float(innings_pitched_num),
            3
        )

    return whip

def get_strikes(appearance_list):
    num_strikes = 0

    for plate_appearance in appearance_list:
        for event in plate_appearance.event_list:
            if (isinstance(event, Pitch) and
                    event.pitch_description not in NON_STRIKE_LIST):
                num_strikes += 1

    return num_strikes

def get_pitches(appearance_list):
    num_pitches = 0

    for plate_appearance in appearance_list:
        for event in plate_appearance.event_list:
            if (isinstance(event, Pitch) and
                    event.pitch_description != 'Automatic Ball'):
                num_pitches += 1

    return num_pitches

def get_walks(appearance_list):
    num_walks = 0

    for plate_appearance in appearance_list:
        if 'BB' in plate_appearance.scorecard_summary:
            num_walks += 1

    return num_walks


def get_strikeouts(appearance_list):
    num_strikeouts = 0

    for plate_appearance in appearance_list:
        if ('K' in plate_appearance.scorecard_summary or
                'ꓘ' in plate_appearance.scorecard_summary):
            num_strikeouts += 1

    return num_strikeouts

def get_lob(appearance_list):
    first_base = None
    second_base = None
    third_base = None

    for plate_appearance in appearance_list:
        (first_base,
         second_base,
         third_base) = process_baserunners(plate_appearance,
                                           appearance_list[-1],
                                           first_base,
                                           second_base,
                                           third_base)

    num_lob = 0

    if first_base:
        num_lob += 1
    if second_base:
        num_lob += 1
    if third_base:
        num_lob += 1

    return num_lob

def get_errors(appearance_list):
    num_errors = 0

    for plate_appearance in appearance_list:
        if plate_appearance.error_str:
            num_errors += 1

        last_description = None

        for event in plate_appearance.event_list:
            if isinstance(event, RunnerAdvance):
                if ('Pickoff Error' in event.run_description and
                        last_description != event.run_description):
                    num_errors += 1
                    last_description = event.run_description
            else:
                last_description = None

    return num_errors

def get_hits(appearance_list):
    num_hits = 0

    for plate_appearance in appearance_list:
        for code in HIT_CODE_LIST:
            if code in plate_appearance.scorecard_summary:
                num_hits += 1
                continue

    return num_hits

def get_runs(appearance_list):
    num_runs = 0

    for plate_appearance in appearance_list:
        num_runs += len(plate_appearance.scoring_runners_list)

    return num_runs

def count_summaries_by_keyword(inning_half_list, keyword):
    num_keyword_appearances = 0
    for appearance_list in inning_half_list:
        for appearance in appearance_list:
            if keyword in appearance.plate_appearance_summary:
                num_keyword_appearances += 1

    return num_keyword_appearances

def count_runner_advance_unique_keywords(inning_half_list, keyword):
    num_keyword_appearances = 0

    for appearance_list in inning_half_list:
        for appearance in appearance_list:
            runner_list = []
            previous_run_description = None
            new_event_next = True
            for event in appearance.event_list:
                if isinstance(event, RunnerAdvance):
                    if event.run_description != previous_run_description:
                        runner_list = [event.runner]
                        new_event_next = True
                    elif (event.run_description == previous_run_description and
                          event.runner in runner_list):
                        runner_list = [event.runner]
                        new_event_next = True
                    else:
                        runner_list.append(event.runner)
                        new_event_next = False

                    if new_event_next and keyword in event.run_description:
                        num_keyword_appearances += 1

                    previous_run_description = event.run_description

    return num_keyword_appearances

def count_runner_advance_total_keywords(inning_half_list, keyword):
    num_keyword_appearances = 0

    for appearance_list in inning_half_list:
        for appearance in appearance_list:
            for event in appearance.event_list:
                if isinstance(event, RunnerAdvance):
                    if keyword in event.run_description:
                        num_keyword_appearances += 1

    return num_keyword_appearances

def get_team_singles(inning_half_list):
    return count_summaries_by_keyword(inning_half_list, 'Single')

def get_team_doubles(inning_half_list):
    return count_summaries_by_keyword(inning_half_list, 'Double')

def get_team_triples(inning_half_list):
    return count_summaries_by_keyword(inning_half_list, 'Triple')

def get_team_home_runs(inning_half_list):
    return count_summaries_by_keyword(inning_half_list, 'Home Run')

def get_team_sac_flies(inning_half_list):
    return count_summaries_by_keyword(inning_half_list, 'Sac Fly')

def get_team_sac_bunts(inning_half_list):
    return count_summaries_by_keyword(inning_half_list, 'Sac Bunt')

def get_team_batted_into_double_plays(inning_half_list):
    return (
        count_summaries_by_keyword(inning_half_list, 'Double Play') +
        count_summaries_by_keyword(inning_half_list, 'DP')
    )

def get_team_hit_by_pitches(inning_half_list):
    return count_summaries_by_keyword(inning_half_list, 'Hit By Pitch')

def get_team_received_wild_pitches(inning_half_list):
    return count_runner_advance_unique_keywords(inning_half_list, 'Wild Pitch')

def get_team_received_passed_balls(inning_half_list):
    return count_runner_advance_unique_keywords(inning_half_list, 'Passed Ball')

def get_team_stolen_bases(inning_half_list):
    return count_runner_advance_total_keywords(inning_half_list, 'Stolen Base')

def get_team_caught_stealing(inning_half_list):
    return count_runner_advance_total_keywords(inning_half_list,
                                               'Caught Stealing')

def get_team_plate_appearances(inning_half_list):
    return len(
        [appearance
         for appearance_list in inning_half_list
         for appearance in appearance_list
         if appearance.plate_appearance_summary != 'Runner Out']
    )

def get_team_stats(game, inning_half_str):
    inning_half_list = get_inning_half_list(game, inning_half_str)

    team_box_score = TeamBoxScore(
        get_team_singles(inning_half_list),
        get_team_doubles(inning_half_list),
        get_team_triples(inning_half_list),
        get_team_home_runs(inning_half_list),
        get_team_sac_flies(inning_half_list),
        get_team_sac_bunts(inning_half_list),
        get_team_batted_into_double_plays(inning_half_list),
        get_team_hit_by_pitches(inning_half_list),
        get_team_received_wild_pitches(inning_half_list),
        get_team_received_passed_balls(inning_half_list),
        get_team_stolen_bases(inning_half_list),
        get_team_caught_stealing(inning_half_list),
        get_team_plate_appearances(inning_half_list)
    )

    return team_box_score
