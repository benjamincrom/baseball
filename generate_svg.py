import multiprocessing
import os
import sys

import baseball_events
import constants
import fetch_game


def get_game_width(game):
    inning_length = max(len(game.inning_list), constants.NUM_MINIMUM_INNINGS)
    game_width = constants.BOX_WIDTH * (inning_length + constants.EXTRA_COLUMNS)

    return game_width

def get_big_svg_header(game):
    inning_length = max(len(game.inning_list), constants.NUM_MINIMUM_INNINGS)
    game_width = get_game_width(game)

    big_svg_str = constants.BIG_SVG_HEADER.format(width=game_width)

    for inning_num in range(1, inning_length + 1):
        x_pos = inning_num * constants.BOX_WIDTH
        text_x_pos = x_pos + (constants.BOX_WIDTH // 2)

        big_svg_str += constants.BIG_SVG_COLUMN.format(inning_num=inning_num,
                                                       x_pos=x_pos,
                                                       text_x_pos=text_x_pos,
                                                       width=game_width)

    box_score_header_x_pos = (inning_length + 1) * constants.BOX_WIDTH
    box_score_header_text_x_pos = box_score_header_x_pos + 13

    big_svg_str += constants.BOX_SCORE_COLUMN_HEADER.format(
        x_pos=box_score_header_x_pos,
        text_x_pos=box_score_header_text_x_pos,
    )

    return big_svg_str

def get_summary_svg(plate_appearance):
    batter_on_base = False

    for event in plate_appearance.event_list:
        batter_on_base = (
            isinstance(event, baseball_events.RunnerAdvance) and
            event.runner == plate_appearance.batter and
            event.end_base
        )

    if plate_appearance.got_on_base:
        return_str = constants.SVG_SUMMARY_TEMPLATE.format(
            summary=plate_appearance.scorecard_summary,
            title=plate_appearance.plate_appearance_description
        )
    else:
        if (plate_appearance.scorecard_summary == 'K' and
                not batter_on_base):
            return_str = constants.SVG_SWINGING_STRIKEOUT_TEMPLATE.format(
                title=plate_appearance.plate_appearance_description
            )
        elif (plate_appearance.scorecard_summary == 'ꓘ' and
              not batter_on_base):
            return_str = constants.SVG_CALLED_STRIKEOUT_TEMPLATE.format(
                title=plate_appearance.plate_appearance_description
            )
        else:
            return_str = constants.SVG_FIELDING_TEMPLATE.format(
                summary=plate_appearance.scorecard_summary.replace('ꓘ', 'K'),
                title=plate_appearance.plate_appearance_description
            )

    if plate_appearance.got_on_base and plate_appearance.error_str:
        return_str += constants.SVG_FIELDING_TEMPLATE.format(
            summary=plate_appearance.error_str,
            title=plate_appearance.plate_appearance_description
        )

    return return_str

def get_pitch_color(event):
    if ('Strike' in event.pitch_description or
            'Foul' in event.pitch_description):
        color = constants.RED_COLOR
    elif 'In play' in event.pitch_description:
        color = constants.BLUE_COLOR
    else:
        color = constants.BLACK_COLOR

    return color

def process_pitch_position(event):
    if event.pitch_position == constants.AUTOMATIC_BALL_POSITION:
        x_coord, y_coord = constants.AUTOMATIC_BALL_COORDINATE
    else:
        x_scale_factor = event.pitch_position[0] / constants.PITCH_MAX_COORD
        x_coord = int(
            constants.PITCH_X_MAX - (constants.PITCH_BOX_WIDTH * x_scale_factor)
        )

        y_scale_factor = event.pitch_position[1] / constants.PITCH_MAX_COORD
        y_coord = int(
            constants.PITCH_Y_MIN + (constants.PITCH_BOX_HEIGHT *
                                     y_scale_factor)
        )

    return x_coord, y_coord

def process_pitch(x_val, y_val, event, pitch_svg):
    color = get_pitch_color(event)
    description = event.pitch_description.split(' (')[0]
    code = constants.PITCH_TYPE_DESCRIPTION[description]

    pitch_type = event.pitch_type or ''
    x_coord, y_coord = process_pitch_position(event)

    if event.pitch_speed:
        speed = int(round(event.pitch_speed))
    else:
        speed = ''

    pitch_svg += constants.SVG_PITCH_TEMPLATE.format(
        pitch_text_x_1=x_val,
        pitch_text_x_2=x_val + constants.PITCH_TYPE_X_OFFSET,
        pitch_text_x_3=x_val + constants.PITCH_SPEED_X_OFFSET,
        pitch_text_y=y_val,
        pitch_color=color,
        pitch_code=code,
        pitch_type=pitch_type,
        pitch_speed=speed,
        pitch_location_x=x_coord,
        pitch_location_y=y_coord,
        title=event.pitch_description
    )

    return pitch_svg

def process_pickoff(x_val, y_val, event, pitch_svg):
    pickoff_base = event.pickoff_base[0]

    if event.pickoff_was_successful:
        color = constants.RED_COLOR
        pickoff_result = 'OUT'
    else:
        color = constants.BLACK_COLOR
        pickoff_result = 'SAFE'

    pitch_svg += constants.SVG_PICKOFF_TEMPLATE.format(
        pickoff_text_x_1=x_val,
        pickoff_text_x_2=x_val + constants.PITCH_TYPE_X_OFFSET,
        pickoff_text_y=y_val,
        pickoff_color=color,
        pickoff_base=pickoff_base,
        pickoff_result=pickoff_result,
        title=event.pickoff_description
    )

    return pitch_svg

def get_pitch_svg(plate_appearance):
    pitch_svg = ''
    x_val = constants.FIRST_PITCH_X_VAL
    y_val = constants.FIRST_PITCH_Y_VAL

    for event in plate_appearance.event_list:
        if y_val > constants.PITCH_Y_LIMIT:
            y_val = constants.PITCH_ROW_2_Y_VAL
            x_val += constants.PITCH_X_OFFSET

        if isinstance(event, baseball_events.Pitch):
            pitch_svg = process_pitch(x_val, y_val, event, pitch_svg)
            y_val += constants.PITCH_Y_OFFSET
        elif isinstance(event, baseball_events.Pickoff):
            pitch_svg += process_pickoff(x_val, y_val, event, pitch_svg)
            y_val += constants.PITCH_Y_OFFSET

    return pitch_svg

def get_runner_title_str(event):
    title_flag_str = ''
    if event.runner_scored:
        title_flag_list = []
        if event.run_earned:
            title_flag_list.append('Earned')

        if event.is_rbi:
            title_flag_list.append('RBI')

        if title_flag_list:
            title_flag_str = ' ({})'.format(', '.join(title_flag_list))
        else:
            title_flag_str = ''

    return title_flag_str

def get_runner_color(event):
    if not event.end_base and not event.runner_scored:
        color = constants.RED_COLOR
    elif event.runner_scored:
        color = constants.DARK_GREEN_COLOR
    else:
        color = constants.BLACK_COLOR

    return color

def get_runner_end_base_str(plate_appearance, event):
    if event.end_base:
        this_end_base_str = event.end_base[0]
    elif event.runner_scored:
        this_end_base_str = 'H'
    else:
        this_end_base_str = ''
        for out_runner, out_base in plate_appearance.out_runners_list:
            if out_runner == event.runner:
                this_end_base_str = out_base[0]
                if this_end_base_str == 'h':
                    this_end_base_str = 'H'

    return this_end_base_str

def get_runners_svg(plate_appearance):
    runner_svg_str = ''
    for event in plate_appearance.event_list:
        if (isinstance(event, baseball_events.RunnerAdvance) and
                event.start_base):
            color = get_runner_color(event)
            start_base_num = int(event.start_base[0])
            this_end_base = get_runner_end_base_str(plate_appearance,
                                                    event)

            summary = '{}-{}'.format(start_base_num, this_end_base)
            is_forceout_desc = ('Forceout' in event.run_description or
                                'Double Play' in event.run_description or
                                'Triple Play' in event.run_description or
                                'DP' in event.run_description or
                                'TP' in event.run_description)

            if (is_forceout_desc and event.end_base == '' and this_end_base and
                    not event.runner_scored):
                summary += 'f'

            title_flag_str = get_runner_title_str(event)

            title = '{}: {}{}'.format(
                str(event.runner),
                event.run_description,
                title_flag_str
            )

            y_val = constants.RUNNER_SUMMARY_Y_VAL
            if start_base_num == 2:
                y_val += constants.RUNNER_SUMMARY_Y_OFFSET
            elif start_base_num == 3:
                y_val += (constants.RUNNER_SUMMARY_Y_OFFSET * 2)

            runner_svg_str += constants.SVG_RUNNER_TEMPLATE.format(
                y_val=y_val,
                color=color,
                summary=summary,
                title=title
            )

    return runner_svg_str

def get_outs_svg(plate_appearance, prev_plate_appearance):
    outs_svg = ''
    outs_list = []

    if not prev_plate_appearance:
        outs_before = 0
    else:
        outs_before = prev_plate_appearance.inning_outs

    outs_this_pa = plate_appearance.inning_outs - outs_before
    if outs_this_pa > 0:
        outs_list = range(outs_before + 1, plate_appearance.inning_outs + 1)

    y_val = constants.OUT_CIRCLE_Y_VAL
    for out in outs_list:
        outs_svg += constants.SVG_OUT_TEMPLATE.format(
            y_val=y_val,
            y_text=y_val + constants.OUT_TEXT_Y_OFFSET,
            out_number=out
        )

        y_val += constants.OUT_CIRCLE_Y_OFFSET

    return outs_svg

def get_components(plate_appearance):
    number = plate_appearance.batter.number

    if plate_appearance.scorecard_summary:
        summary = plate_appearance.scorecard_summary.split()[0]
    else:
        summary = None

    title = plate_appearance.plate_appearance_description

    return number, summary, title

def get_all_base_components(base_2_pa, base_3_pa, home_pa):
    if base_2_pa:
        base_2_number, base_2_summary, base_2_title = get_components(base_2_pa)
    else:
        base_2_number, base_2_summary, base_2_title = '', '', ''

    if base_3_pa:
        base_3_number, base_3_summary, base_3_title = get_components(base_3_pa)
    else:
        base_3_number, base_3_summary, base_3_title = '', '', ''

    if home_pa:
        base_4_number, base_4_summary, base_4_title = get_components(home_pa)
    else:
        base_4_number, base_4_summary, base_4_title = '', '', ''

    return (base_2_number,
            base_2_summary,
            base_2_title,
            base_3_number,
            base_3_summary,
            base_3_title,
            base_4_number,
            base_4_summary,
            base_4_title)

def process_base_appearances(base_2_pa, base_3_pa, home_pa, batter_final_base,
                             batter_out_base):
    (base_2_number,
     base_2_summary,
     base_2_title,
     base_3_number,
     base_3_summary,
     base_3_title,
     base_4_number,
     base_4_summary,
     base_4_title) = get_all_base_components(base_2_pa, base_3_pa, home_pa)

    if batter_out_base:
        if batter_out_base == '1B':
            base_svg = ''
        elif batter_out_base == '2B':
            base_svg = constants.SVG_BASE_2_OUT_TEMPLATE.format(
                base_2_number=base_2_number,
                base_2_summary=base_2_summary,
                base_2_title=base_2_title
            )
        elif batter_out_base == '3B':
            base_svg = constants.SVG_BASE_3_OUT_TEMPLATE.format(
                base_2_number=base_2_number,
                base_2_summary=base_2_summary,
                base_2_title=base_2_title,
                base_3_number=base_3_number,
                base_3_summary=base_3_summary,
                base_3_title=base_3_title
            )
        elif batter_out_base == 'H':
            base_svg = constants.SVG_BASE_4_OUT_TEMPLATE.format(
                base_2_number=base_2_number,
                base_2_summary=base_2_summary,
                base_2_title=base_2_title,
                base_3_number=base_3_number,
                base_3_summary=base_3_summary,
                base_3_title=base_3_title,
                base_4_number=base_4_number,
                base_4_summary=base_4_summary,
                base_4_title=base_4_title
            )
        else:
            raise ValueError('Invalid Base')
    elif batter_final_base:
        if batter_final_base == '1B':
            base_svg = constants.SVG_BASE_1
        elif batter_final_base == '2B':
            base_svg = constants.SVG_BASE_2_TEMPLATE.format(
                base_2_number=base_2_number,
                base_2_summary=base_2_summary,
                base_2_title=base_2_title
            )
        elif batter_final_base == '3B':
            base_svg = constants.SVG_BASE_3_TEMPLATE.format(
                base_2_number=base_2_number,
                base_2_summary=base_2_summary,
                base_2_title=base_2_title,
                base_3_number=base_3_number,
                base_3_summary=base_3_summary,
                base_3_title=base_3_title
            )
        elif batter_final_base == 'H':
            base_svg = constants.SVG_BASE_4_TEMPLATE.format(
                base_2_number=base_2_number,
                base_2_summary=base_2_summary,
                base_2_title=base_2_title,
                base_3_number=base_3_number,
                base_3_summary=base_3_summary,
                base_3_title=base_3_title,
                base_4_number=base_4_number,
                base_4_summary=base_4_summary,
                base_4_title=base_4_title
            )
        else:
            raise ValueError('Invalid Base')
    else:
        raise ValueError('No Final Base')

    return base_svg

def player_got_on_base(plate_appearance):
    got_on_base = False
    for event in plate_appearance.event_list:
        if (isinstance(event, baseball_events.RunnerAdvance) and
                event.runner == plate_appearance.batter):
            got_on_base = True

    return got_on_base

def fix_pa(plate_appearance, event):
    summary = None
    description = None

    if 'Stolen' in event.run_description:
        summary = 'S'
        description = '{} batting: Stolen Base'.format(plate_appearance.batter)
    elif 'Caught Stealing' in event.run_description:
        summary = 'CS'
        description = '{} batting: Caught Stealing'.format(
            plate_appearance.batter
        )
    elif 'Passed Ball' in event.run_description:
        summary = 'PB'
        description = '{} batting: Passed Ball'.format(plate_appearance.batter)
    elif 'Wild Pitch' in event.run_description:
        summary = 'WP'
        description = '{} batting: Wild Pitch'.format(plate_appearance.batter)
    elif 'Balk' in event.run_description:
        summary = 'BLK'
        description = '{} batting: Balk'.format(plate_appearance.batter)
    elif 'Defensive Indiff' in event.run_description:
        summary = 'DI'
        description = '{} batting: Defensive Indifference'.format(
            plate_appearance.batter
        )

    if summary and description:
        return_pa = constants.FakePlateAppearance(summary,
                                                  plate_appearance.batter,
                                                  description)
    else:
        return_pa = plate_appearance

    return return_pa

def get_base_svg(plate_appearance, plate_appearance_list):
    plate_appearance_index = plate_appearance_list.index(plate_appearance)
    plate_appearance_list = plate_appearance_list[plate_appearance_index:]

    second_base_pa, third_base_pa, home_plate_pa = None, None, None
    batter_final_base, batter_out_base, batter_is_done = None, None, None

    batter = plate_appearance.batter
    for this_pa in plate_appearance_list:
        for event in this_pa.event_list:
            if (isinstance(event, baseball_events.RunnerAdvance) and
                    event.runner == batter):
                if not event.end_base:
                    batter_is_done = True

                for out_runner, out_base in this_pa.out_runners_list:
                    if out_runner == batter:
                        if out_base == '1st':
                            batter_out_base = '1B'
                        elif out_base == '2nd':
                            batter_out_base = '2B'
                            if plate_appearance != this_pa:
                                second_base_pa = fix_pa(this_pa, event)
                        elif out_base == '3rd':
                            batter_out_base = '3B'
                            if plate_appearance != this_pa:
                                third_base_pa = fix_pa(this_pa, event)
                        elif out_base == 'home':
                            batter_out_base = 'H'
                            if plate_appearance != this_pa:
                                home_plate_pa = fix_pa(this_pa, event)

                if event.end_base == '1B':
                    batter_final_base = '1B'
                elif event.end_base == '2B':
                    batter_final_base = '2B'
                    if plate_appearance != this_pa:
                        second_base_pa = fix_pa(this_pa, event)
                elif event.end_base == '3B':
                    batter_final_base = '3B'
                    if plate_appearance != this_pa:
                        third_base_pa = fix_pa(this_pa, event)
                elif event.runner_scored:
                    batter_final_base = 'H'
                    if plate_appearance != this_pa:
                        home_plate_pa = fix_pa(this_pa, event)
            elif isinstance(event, baseball_events.Substitution):
                if event.outgoing_player == batter and event.position == 'PR':
                    batter = event.incoming_player

        if batter_is_done:
            break

    base_svg = process_base_appearances(second_base_pa,
                                        third_base_pa,
                                        home_plate_pa,
                                        batter_final_base,
                                        batter_out_base)

    return base_svg

def get_hit_svg(plate_appearance):
    hit_svg = ''
    hit_location = plate_appearance.hit_location
    if hit_location:
        if hit_location[0] == 'S':
            hit_location = hit_location[1:]

        if len(hit_location) == 2:
            hit_type = hit_location[0]
            hit_position_num = int(hit_location[1])

            is_valid_hit_type = False
            if hit_type in ['B', 'G']:
                template = constants.SVG_HIT_GROUNDER_TEMPLATE
                is_valid_hit_type = True
            elif hit_type in ['L', 'E']:
                template = constants.SVG_HIT_LINE_TEMPLATE
                is_valid_hit_type = True
            elif hit_type in ['P', 'F']:
                template = constants.SVG_HIT_FLY_TEMPLATE
                is_valid_hit_type = True

            if is_valid_hit_type:
                if hit_position_num == 1:
                    hit_svg = template.format(hit_x=constants.PITCHER_X,
                                              hit_y=constants.PITCHER_Y)
                elif hit_position_num == 2:
                    hit_svg = template.format(hit_x=constants.PITCHER_X,
                                              hit_y=constants.CATCHER_Y)
                elif hit_position_num == 3:
                    hit_svg = template.format(hit_x=constants.FIRST_BASE_X,
                                              hit_y=constants.FIRST_BASE_Y)
                elif hit_position_num == 4:
                    hit_svg = template.format(hit_x=constants.SECOND_BASE_X,
                                              hit_y=constants.SECOND_BASE_Y)
                elif hit_position_num == 5:
                    hit_svg = template.format(hit_x=constants.THIRD_BASE_X,
                                              hit_y=constants.FIRST_BASE_Y)
                elif hit_position_num == 6:
                    hit_svg = template.format(hit_x=constants.SHORTSTOP_X,
                                              hit_y=constants.SHORTSTOP_Y)
                elif hit_position_num == 7:
                    hit_svg = template.format(hit_x=constants.LEFT_FIELDER_X,
                                              hit_y=constants.LEFT_FIELDER_Y)
                elif hit_position_num == 8:
                    hit_svg = template.format(hit_x=constants.PITCHER_X,
                                              hit_y=constants.CENTER_FIELDER_Y)
                elif hit_position_num == 9:
                    hit_svg = template.format(hit_x=constants.RIGHT_FIELDER_X,
                                              hit_y=constants.LEFT_FIELDER_Y)

    return hit_svg

def get_count_svg(plate_appearance):
    balls = 0
    strikes = 0
    for event in plate_appearance.event_list:
        if (isinstance(event, baseball_events.Pitch) and
                'In play' not in event.pitch_description):
            if ('Strike' in event.pitch_description or
                    'Missed Bunt' in event.pitch_description or
                    'Foul Bunt' in event.pitch_description):
                strikes += 1
            elif 'Foul' in event.pitch_description and strikes < 2:
                strikes += 1
            elif 'Foul' not in event.pitch_description:
                balls += 1

    count_str = '{}-{}'.format(balls, strikes)
    count_svg = constants.SVG_COUNT_TEMPLATE.format(count_str=count_str)

    return count_svg

def get_inning_half_stats_tuple_list(game):
    inning_half_stats_tuple_list = []
    for inning_index, inning in enumerate(game.inning_list):
        inning_half_stats_tuple_list.extend(
            [(inning_index + 1, 'top', inning.top_half_inning_stats),
             (inning_index + 1, 'bottom', inning.bottom_half_inning_stats)]
        )

    return inning_half_stats_tuple_list

def get_svg_content_list(game):
    content_list = []
    for inning_index, inning in enumerate(game.inning_list):
        tuple_list = [(inning.top_half_appearance_list, 'top'),
                      (inning.bottom_half_appearance_list, 'bottom')]

        for plate_appearance_list, inning_half_str in tuple_list:
            if plate_appearance_list:
                prev_plate_appearance = None
                for plate_appearance_tuple in enumerate(plate_appearance_list):
                    pa_index, plate_appearance = plate_appearance_tuple

                    plate_appearance_svg = '{}{}{}{}{}{}'.format(
                        get_summary_svg(plate_appearance),
                        get_pitch_svg(plate_appearance),
                        get_runners_svg(plate_appearance),
                        get_count_svg(plate_appearance),
                        get_hit_svg(plate_appearance),
                        get_outs_svg(plate_appearance, prev_plate_appearance)
                    )

                    if player_got_on_base(plate_appearance):
                        plate_appearance_svg += get_base_svg(
                            plate_appearance,
                            plate_appearance_list
                        )

                    id_tuple = (inning_index + 1, inning_half_str, pa_index + 1)
                    content_list.append(
                        (id_tuple,
                         plate_appearance_svg,
                         plate_appearance.plate_appearance_summary)
                    )

                    prev_plate_appearance = plate_appearance

    return content_list

def get_batter_spacing_values(batter_list):
    if len(batter_list) <= 5:
        batter_font_size = constants.BATTER_FONT_SIZE_BIG
        batter_space_increment = constants.BATTER_SPACE_BIG
        stats_y_offset = constants.BATTER_STATS_OFFSET_BIG
        box_score_line_template = (
            ('&#160;' * (constants.BATTER_STATS_SPACES_BIG // 2)) + '%s' +
            ('&#160;' * constants.BATTER_STATS_SPACES_BIG + '%s') * 6
        )
    elif len(batter_list) > 5 and len(batter_list) < 9:
        batter_font_size = constants.BATTER_FONT_SIZE_MED
        batter_space_increment = constants.BATTER_SPACE_MED
        stats_y_offset = constants.BATTER_STATS_OFFSET_MED
        box_score_line_template = (
            ('&#160;' * (constants.BATTER_STATS_SPACES_MED // 2)) + '%s' +
            ('&#160;' * constants.BATTER_STATS_SPACES_MED + '%s') * 6
        )
    else:
        batter_font_size = constants.BATTER_FONT_SIZE_SMALL
        batter_space_increment = constants.BATTER_SPACE_SMALL
        stats_y_offset = constants.BATTER_STATS_OFFSET_SMALL
        box_score_line_template = (
            ('&#160;' * (constants.BATTER_STATS_SPACES_SMALL // 2)) + '%s' +
            ('&#160;' * constants.BATTER_STATS_SPACES_SMALL + '%s') * 6
        )

    return (batter_font_size,
            batter_space_increment,
            stats_y_offset,
            box_score_line_template)

def get_team_batter_box_score_list(game, team, box_score_dict, offset):
    box_score_svg = ''
    num_innings = max(len(game.inning_list), constants.NUM_MINIMUM_INNINGS)
    box_score_x_offset = constants.BOX_WIDTH * (num_innings + 1)

    for batter_list in team.batting_order_list_list:
        box_score_svg += constants.BATTER_SVG_HEADER.format(
            x_pos=box_score_x_offset,
            y_pos=offset + (constants.BOX_HEIGHT // 2)
        )

        batter_font_size, batter_space_increment, _, box_score_line_template = (
            get_batter_spacing_values(batter_list)
        )

        batter_y_pos = constants.BATTER_INITIAL_Y_POS
        last_batter = None
        for batter_appearance in batter_list:
            if last_batter == batter_appearance.player_obj:
                box_score_line_str = ''
            else:
                box_score_line_str = (
                    box_score_line_template %
                    box_score_dict[batter_appearance.player_obj]
                )

            box_score_svg += constants.BOX_SCORE_LINE_TEMPLATE.format(
                name_y_pos=batter_y_pos,
                box_score_line=box_score_line_str,
                batter_font_size=batter_font_size
            )

            batter_y_pos += batter_space_increment
            last_batter = batter_appearance.player_obj

        box_score_svg += constants.SVG_FOOTER
        offset += constants.BOX_HEIGHT

    return box_score_svg

def get_team_batter_list(team, offset):
    batter_svg = ''
    for batter_list in team.batting_order_list_list:
        batter_svg += constants.BATTER_SVG_HEADER.format(
            x_pos=0,
            y_pos=offset + (constants.BOX_HEIGHT // 2)
        )

        batter_font_size, batter_space_increment, stats_y_offset, _ = (
            get_batter_spacing_values(batter_list)
        )

        batter_y_pos = constants.BATTER_INITIAL_Y_POS
        last_batter = None
        for batter_appearance in batter_list:
            if last_batter == batter_appearance.player_obj:
                batter_str = ''
                stats_str = ''
            else:
                batter_str = '{}'.format(batter_appearance.player_obj)
                if (batter_appearance.player_obj.obp and
                        batter_appearance.player_obj.slg):
                    stats_str = 'OBP: {:.3f}, SLG: {:.3f}'.format(
                        batter_appearance.player_obj.obp,
                        batter_appearance.player_obj.slg
                    )
                else:
                    stats_str = ''

            appears_str = '({}, {})'.format(batter_appearance.start_inning_num,
                                            batter_appearance.position)

            batter_svg += constants.BATTER_NAME_TEMPLATE.format(
                batter_id=batter_appearance.player_obj.mlb_id,
                name_y_pos=batter_y_pos,
                stats_y_pos=batter_y_pos + stats_y_offset,
                stats=stats_str,
                appears=appears_str,
                batter=batter_str,
                batter_font_size=batter_font_size,
                stats_font_size=batter_font_size - 5
            )

            batter_y_pos += batter_space_increment
            last_batter = batter_appearance.player_obj

        batter_svg += constants.SVG_FOOTER
        offset += constants.BOX_HEIGHT

    return batter_svg

def get_batter_list_and_stats(game):
    both_teams_batters_svg = ''

    tuple_list = [
        (game.away_team, game.away_batter_box_score_dict, 0),
        (game.home_team, game.home_batter_box_score_dict, constants.HEIGHT // 2)
    ]

    for team, box_score_dict, offset in tuple_list:
        both_teams_batters_svg += '{}{}'.format(
            get_team_batter_list(team, offset),
            get_team_batter_box_score_list(game, team, box_score_dict, offset)
        )

    return both_teams_batters_svg

def get_team_stats_box(box_x, box_y, stats_tuple):
    box_1_x = box_x
    stats_box_1_svg = constants.INNING_STATS_BOX.format(
        box_x=box_1_x,
        box_y=box_y,
        stats_str_1='1B: &#160;{}'.format(stats_tuple.B1),
        stats_str_2='2B: &#160;{}'.format(stats_tuple.B2),
        stats_str_3='3B: &#160;{}'.format(stats_tuple.B3),
        stats_str_4='HR: {}'.format(stats_tuple.HR),
        stats_str_5='SF:',
        stats_str_6='SAC:',
        stats_str_7='DP:',
        stats_str_8='HBP:',
        stats_str_9='{}'.format(stats_tuple.SF),
        stats_str_10='{}'.format(stats_tuple.SAC),
        stats_str_11='{}'.format(stats_tuple.DP),
        stats_str_12='{}'.format(stats_tuple.HBP)
    )

    box_2_x = box_x + constants.BOX_WIDTH
    stats_box_2_svg = constants.INNING_STATS_BOX.format(
        box_x=box_2_x,
        box_y=box_y,
        stats_str_1='WP: {}'.format(stats_tuple.WP),
        stats_str_2='PB: &#160;{}'.format(stats_tuple.PB),
        stats_str_3='SB: &#160;{}'.format(stats_tuple.SB),
        stats_str_4='CS: &#160;{}'.format(stats_tuple.CS),
        stats_str_5='PA:',
        stats_str_6='',
        stats_str_7='',
        stats_str_8='',
        stats_str_9='{}'.format(stats_tuple.PA),
        stats_str_10='',
        stats_str_11='',
        stats_str_12=''
    )

    both_stats_boxes_svg = stats_box_1_svg + stats_box_2_svg

    return both_stats_boxes_svg

def get_inning_stats_box(box_x, box_y, stats_tuple):
    stats_box_svg = (
        constants.INNING_STATS_BOX.format(
            box_x=box_x,
            box_y=box_y,
            stats_str_1='R: {}'.format(stats_tuple.R),
            stats_str_2='E: {}'.format(stats_tuple.E),
            stats_str_3='K: {}'.format(stats_tuple.K),
            stats_str_4='S: {}'.format(stats_tuple.S),
            stats_str_5='H:',
            stats_str_6='LOB:',
            stats_str_7='BB:',
            stats_str_8='P:',
            stats_str_9='{}'.format(stats_tuple.H),
            stats_str_10='{}'.format(stats_tuple.LOB),
            stats_str_11='{}'.format(stats_tuple.BB),
            stats_str_12='{}'.format(stats_tuple.P)
        )
    )

    return stats_box_svg

def get_this_pa_num(player_appearance, appearance_list):
    this_pa_num = None
    if appearance_list:
        for pa_index, plate_app in enumerate(appearance_list):
            if plate_app.batter == player_appearance.player_obj:
                this_pa_num = pa_index + 1

    return this_pa_num

def add_away_batter_sub_division_lines(game):
    sub_divisions_svg = ''
    for batter_appearance_list in game.away_team.batting_order_list_list:
        batting_pos_index = game.away_team.batting_order_list_list.index(
            batter_appearance_list
        )

        last_batter = None
        for batter_app in batter_appearance_list:
            same_last_batter = last_batter == batter_app.player_obj
            if not same_last_batter:
                x_pos = constants.BOX_WIDTH * batter_app.start_inning_num
                y_pos = ((constants.BOX_HEIGHT * batting_pos_index) +
                         (constants.BOX_HEIGHT // 2))

                for inning_index, inning in enumerate(game.inning_list):
                    if batter_app.start_inning_num == inning_index + 1:
                        inning_pa_num = get_this_pa_num(
                            batter_app,
                            inning.top_half_appearance_list
                        )

                        if (not inning_pa_num or
                                batter_app.start_inning_batter_num > inning_pa_num
                                or batter_app.start_inning_half == 'bottom'):
                            x_pos += constants.BOX_WIDTH

                if not (batter_app.start_inning_num == 1 and
                        batter_app.start_inning_batter_num == 1 and
                        batter_app.start_inning_half == 'top'):
                    sub_divisions_svg += (
                        constants.BATTER_SUB_DIVISION_LINE.format(
                            x_pos=x_pos,
                            y_pos_1=y_pos,
                            y_pos_2=y_pos + constants.BOX_HEIGHT
                        )
                    )

            last_batter = batter_app.player_obj

    return sub_divisions_svg

def add_home_batter_sub_division_lines(game):
    sub_divisions_svg = ''
    for batter_appearance_list in game.home_team.batting_order_list_list:
        batting_pos_index = game.home_team.batting_order_list_list.index(
            batter_appearance_list
        )
        last_batter = None
        for batter_app in batter_appearance_list:
            same_last_batter = last_batter == batter_app.player_obj

            if not same_last_batter:
                x_pos = constants.BOX_WIDTH * batter_app.start_inning_num
                y_pos = ((constants.BOX_HEIGHT * batting_pos_index) +
                         (constants.HEIGHT // 2 + constants.BOX_HEIGHT // 2))

                for inning_index, inning in enumerate(game.inning_list):
                    if batter_app.start_inning_num == inning_index + 1:
                        inning_pa_num = get_this_pa_num(
                            batter_app,
                            inning.bottom_half_appearance_list
                        )

                        if ((not inning_pa_num or
                             batter_app.start_inning_batter_num > inning_pa_num)
                                and batter_app.start_inning_half == 'bottom'):
                            x_pos += constants.BOX_WIDTH

                if not (batter_app.start_inning_num == 1 and
                        batter_app.start_inning_batter_num == 1 and
                        batter_app.start_inning_half == 'top'):
                    sub_divisions_svg += (
                        constants.BATTER_SUB_DIVISION_LINE.format(
                            x_pos=x_pos,
                            y_pos_1=y_pos,
                            y_pos_2=y_pos + constants.BOX_HEIGHT
                        )
                    )

            last_batter = batter_app.player_obj

    return sub_divisions_svg

def add_away_pitcher_sub_division_lines(game):
    sub_divisions_svg = ''

    for pitcher_app in game.away_team.pitcher_list:
        if pitcher_app.end_inning_num:
            total_pa_num = 0

            for inning_index, inning in enumerate(game.inning_list):
                inning_num = inning_index + 1
                inning_pa_num = 1

                if not inning.bottom_half_appearance_list:
                    continue

                for appearance in inning.bottom_half_appearance_list:
                    if (inning_num == pitcher_app.end_inning_num and
                            (inning_pa_num == pitcher_app.end_inning_batter_num
                             or pitcher_app.end_inning_half == 'top')):

                        x_pos = (constants.BOX_WIDTH *
                                 pitcher_app.end_inning_num)

                        y_pos = (
                            (constants.BOX_HEIGHT *
                             (total_pa_num % constants.LEN_BATTING_LIST)) +
                            (constants.HEIGHT // 2 + constants.BOX_HEIGHT // 2)
                        )

                        sub_divisions_svg += (
                            constants.PITCHER_SUB_DIVISION_LINE.format(
                                x_pos_1=x_pos,
                                x_pos_2=x_pos + constants.BOX_WIDTH,
                                y_pos=y_pos
                            )
                        )

                    if appearance.plate_appearance_summary != 'Runner Out':
                        inning_pa_num += 1
                        total_pa_num += 1

    return sub_divisions_svg

def add_home_pitcher_sub_division_lines(game):
    sub_divisions_svg = ''

    for pitcher_app in game.home_team.pitcher_list:
        if pitcher_app.end_inning_num:
            total_pa_num = 0

            for inning_index, inning in enumerate(game.inning_list):
                inning_num = inning_index + 1
                inning_pa_num = 1
                last_batter_no_pa = False

                for appearance in inning.top_half_appearance_list:
                    if (inning_num == pitcher_app.end_inning_num and
                            inning_pa_num == pitcher_app.end_inning_batter_num
                            and pitcher_app.end_inning_half != 'bottom'):

                        x_pos = constants.BOX_WIDTH * pitcher_app.end_inning_num
                        y_pos = ((constants.BOX_HEIGHT *
                                  (total_pa_num % constants.LEN_BATTING_LIST)) +
                                 (constants.BOX_HEIGHT // 2))

                        sub_divisions_svg += (
                            constants.PITCHER_SUB_DIVISION_LINE.format(
                                x_pos_1=x_pos,
                                x_pos_2=x_pos + constants.BOX_WIDTH,
                                y_pos=y_pos
                            )
                        )

                    if appearance.plate_appearance_summary == 'Runner Out':
                        last_batter_no_pa = True
                    else:
                        total_pa_num += 1
                        inning_pa_num += 1

                if (inning_num == pitcher_app.end_inning_num and
                        pitcher_app.end_inning_half == 'bottom'):
                    sub_divisions_svg += add_end_inning_pitcher_sub(
                        pitcher_app,
                        total_pa_num,
                        last_batter_no_pa
                    )

    return sub_divisions_svg

def add_end_inning_pitcher_sub(pitcher_app, total_pa_num, last_batter_no_pa):
    batting_pos_index = (
        (total_pa_num % constants.LEN_BATTING_LIST) +
        int(last_batter_no_pa)
    )

    x_pos = constants.BOX_WIDTH * pitcher_app.end_inning_num
    y_pos = ((constants.BOX_HEIGHT * batting_pos_index) +
             (constants.BOX_HEIGHT // 2))

    this_sub_division_svg = (
        constants.PITCHER_SUB_DIVISION_LINE.format(
            x_pos_1=x_pos,
            x_pos_2=x_pos + constants.BOX_WIDTH,
            y_pos=y_pos
        )
    )

    return this_sub_division_svg

def get_box_score_whip_era(box_score_tuple):
    if box_score_tuple.ERA is not None:
        if box_score_tuple.ERA == '&#8734;':
            era_str = '&#8734;'
        else:
            era_str = ('%.2f' % box_score_tuple.ERA)
    else:
        era_str = ''

    if box_score_tuple.WHIP is not None:
        if box_score_tuple.WHIP == '&#8734;':
            whip_str = '&#8734;'
        else:
            whip_str = ('%.3f' % box_score_tuple.WHIP)
    else:
        whip_str = ''

    return era_str, whip_str

def get_pitcher_box_score_lines(pitcher_app_list, chunk_size, box_score_dict):
    pitcher_rows_svg = ''
    row_increment = 0

    if chunk_size == constants.SMALL_CHUNK_SIZE:
        initial_y = constants.PITCHER_BOX_SCORE_LARGE_Y
        text_size_1 = constants.PITCHER_LARGE_FONT_SIZE
        text_size_2 = constants.PITCHER_STATS_LARGE_FONT_SIZE
        stats_offset = constants.PITCHER_BOX_STATS_LARGE_Y_OFFSET
        defined_text_increment = constants.PITCHER_BOX_SCORE_LARGE_Y_INCREMENT
    elif chunk_size == constants.LARGE_CHUNK_SIZE:
        initial_y = constants.PITCHER_BOX_SCORE_SMALL_Y
        text_size_1 = constants.PITCHER_SMALL_FONT_SIZE
        text_size_2 = constants.PITCHER_STATS_SMALL_FONT_SIZE
        stats_offset = constants.PITCHER_BOX_STATS_SMALL_Y_OFFSET
        defined_text_increment = constants.PITCHER_BOX_SCORE_SMALL_Y_INCREMENT

    for pitcher_app in pitcher_app_list:
        initial_y = constants.PITCHER_BOX_SCORE_SMALL_Y
        box_score_tuple = box_score_dict[pitcher_app.player_obj]
        era_str, whip_str = get_box_score_whip_era(box_score_tuple)
        initial_era_stat_str = 'ERA: ' + str(pitcher_app.player_obj.era)
        appears_str = '({}, {})'.format(pitcher_app.start_inning_num,
                                        pitcher_app.position)

        pitcher_rows_svg += constants.PITCHER_STATS_LINE_TEMPLATE.format(
            pitcher_id=pitcher_app.player_obj.mlb_id,
            name_y_pos=initial_y + row_increment,
            stats_y_pos=stats_offset + row_increment,
            pitcher=pitcher_app.player_obj,
            box_score_1=box_score_tuple.IP, box_score_2=box_score_tuple.WLS,
            box_score_3=box_score_tuple.BF, box_score_4=box_score_tuple.H,
            box_score_5=box_score_tuple.R, box_score_6=box_score_tuple.ER,
            box_score_7=box_score_tuple.SO, box_score_8=box_score_tuple.BB,
            box_score_9=box_score_tuple.IBB, box_score_10=box_score_tuple.HBP,
            box_score_11=box_score_tuple.BLK, box_score_12=box_score_tuple.WP,
            box_score_13=box_score_tuple.HR, box_score_14=box_score_tuple.S,
            box_score_15=box_score_tuple.P, box_score_16=era_str,
            box_score_17=whip_str,
            stats=initial_era_stat_str,
            appears=appears_str,
            size_1=text_size_1,
            size_2=text_size_2
        )

        row_increment += defined_text_increment

    return pitcher_rows_svg

def chunks(this_list, num_elements):
    for i in range(0, len(this_list), num_elements):
        yield this_list[i:i + num_elements]

def create_pitcher_stats_svg(chunk_tuple_list, chunk_size, box_score_dict):
    pitcher_stats_svg = ''
    for location, pitcher_chunk in chunk_tuple_list:
        x_box, y_box = location
        pitcher_stats_svg += constants.PITCHER_STATS_HEADER.format(x_box=x_box,
                                                                   y_box=y_box)

        pitcher_stats_svg += '{}{}'.format(
            get_pitcher_box_score_lines(pitcher_chunk,
                                        chunk_size,
                                        box_score_dict),
            constants.SVG_FOOTER
        )

    return pitcher_stats_svg

def add_team_pitcher_box_score(team, box_score_dict, offset):
    pitcher_app_list = team.pitcher_list
    if len(pitcher_app_list) <= 10:
        chunk_size = constants.SMALL_CHUNK_SIZE
    else:
        chunk_size = constants.LARGE_CHUNK_SIZE

    pitcher_chunk_list = list(chunks(pitcher_app_list, chunk_size))
    location_tuple_list = [
        (0, constants.BOX_HEIGHT * 10 + offset),
        (constants.WIDTH // 2, constants.BOX_HEIGHT * 10 + offset)
    ]

    chunk_tuple_list = []
    for location_index, location_tuple in enumerate(location_tuple_list):
        if location_index < len(pitcher_chunk_list):
            pitcher_chunk = pitcher_chunk_list[location_index]
        else:
            pitcher_chunk = []

        chunk_tuple_list.append((location_tuple, pitcher_chunk))

    pitcher_stats_svg = create_pitcher_stats_svg(chunk_tuple_list,
                                                 chunk_size,
                                                 box_score_dict)

    return pitcher_stats_svg

def add_all_pitcher_box_scores(game):
    all_pitcher_box_svg = ''

    tuple_list = [
        (game.home_team,
         game.home_pitcher_box_score_dict,
         0),
        (game.away_team,
         game.away_pitcher_box_score_dict,
         constants.HEIGHT // 2)
    ]

    for this_tuple in tuple_list:
        team, box_score_dict, offset = this_tuple
        all_pitcher_box_svg += add_team_pitcher_box_score(team,
                                                          box_score_dict,
                                                          offset)

    return all_pitcher_box_svg

def get_team_stats_svg(game):
    team_stats_svg = ''
    game_width = get_game_width(game)
    tuple_list = [
        (
            game_width - (constants.BOX_WIDTH * 2),
            (constants.BOX_HEIGHT * constants.LEN_BATTING_LIST +
             constants.BOX_HEIGHT // 2),
            game.away_team_stats
        ), (
            game_width - (constants.BOX_WIDTH * 2),
            (constants.HEIGHT // 2 +
             constants.BOX_HEIGHT * constants.LEN_BATTING_LIST +
             constants.BOX_HEIGHT // 2),
            game.home_team_stats
        )
    ]

    for box_x, box_y, stats_tuple in tuple_list:
        team_stats_svg += get_team_stats_box(box_x, box_y, stats_tuple)

    return team_stats_svg

def get_box_score_totals(game):
    box_score_totals_svg = ''
    game_width = get_game_width(game)

    tuple_list = [
        (
            game.away_batter_box_score_dict,
            game_width - constants.BOX_WIDTH,
            6 * constants.BOX_HEIGHT + constants.BOX_HEIGHT // 2
        ),
        (
            game.home_batter_box_score_dict,
            game_width - constants.BOX_WIDTH,
            (6 * constants.BOX_HEIGHT + constants.BOX_HEIGHT // 2 +
             constants.HEIGHT // 2)
        )
    ]

    for box_score_dict, x_pos, y_pos in tuple_list:
        box_score_totals_svg += constants.TOTAL_BOX_SCORE_STATS_BOX.format(
            box_x=x_pos,
            box_y=y_pos,
            stats_str_1=box_score_dict['TOTAL'].AB,
            stats_str_2=box_score_dict['TOTAL'].R,
            stats_str_3=box_score_dict['TOTAL'].H,
            stats_str_4=box_score_dict['TOTAL'].RBI,
            stats_str_5=box_score_dict['TOTAL'].BB,
            stats_str_6=box_score_dict['TOTAL'].SO,
            stats_str_7=box_score_dict['TOTAL'].LOB
        )

    return box_score_totals_svg

def is_bat_around(this_inning_tuple_list, inning_pa_num):
    return (
        len(this_inning_tuple_list) > constants.LEN_BATTING_LIST and
        (inning_pa_num > constants.LEN_BATTING_LIST or
         inning_pa_num <= (len(this_inning_tuple_list) %
                           constants.LEN_BATTING_LIST))
    )

def assemble_stats_svg(game):
    stats_svg = ''
    inning_half_stats_list = get_inning_half_stats_tuple_list(game)
    for inning_num, inning_half_str, stats_tuple in inning_half_stats_list:
        if stats_tuple:
            box_x = inning_num * constants.BOX_WIDTH

            if inning_half_str == 'bottom':
                box_y = (constants.HEIGHT // 2 +
                         constants.BOX_HEIGHT * constants.LEN_BATTING_LIST +
                         constants.BOX_HEIGHT // 2)
            elif inning_half_str == 'top':
                box_y = (constants.BOX_HEIGHT * constants.LEN_BATTING_LIST +
                         constants.BOX_HEIGHT // 2)
            else:
                raise ValueError('Invalid inning half str')

            stats_svg += get_inning_stats_box(box_x, box_y, stats_tuple)

    return stats_svg

def get_signature(game):
    signature_svg = ''
    game_width = get_game_width(game)

    tuple_list = [
        (
            game_width - constants.BOX_WIDTH,
            8 * constants.BOX_HEIGHT + constants.BOX_HEIGHT // 2
        ),
        (
            game_width - constants.BOX_WIDTH,
            (8 * constants.BOX_HEIGHT + constants.BOX_HEIGHT // 2 +
             constants.HEIGHT // 2)
        )
    ]

    for x_pos, y_pos in tuple_list:
        signature_svg += constants.SIGNATURE.format(x_pos=x_pos, y_pos=y_pos)

    return signature_svg

def write_individual_pa_svg(svg_content, inning_pa_num, this_inning_tuple_list,
                            this_x_pos, this_y_pos):
    this_svg = ''
    bat_around_flag = is_bat_around(this_inning_tuple_list, inning_pa_num)
    if bat_around_flag:
        this_svg += constants.HALF_SCALE_HEADER
        this_x_pos *= 2
        this_y_pos *= 2
        if inning_pa_num > 9:
            this_x_pos += constants.BOX_WIDTH
            this_y_pos += constants.BOX_HEIGHT

    this_svg += '{}{}{}'.format(
        constants.SVG_HEADER.format(x_pos=this_x_pos, y_pos=this_y_pos),
        svg_content,
        constants.SVG_FOOTER
    )

    if bat_around_flag:
        this_svg += constants.HALF_SCALE_FOOTER

    return this_svg

def assemble_box_content_dict(game):
    content_list_svg = ''
    svg_content_list = get_svg_content_list(game)
    top_pa_index = 0
    bottom_pa_index = 0
    for id_tuple, svg_content, summary in svg_content_list:
        inning_num, inning_half_str, inning_pa_num = id_tuple
        top_offset = top_pa_index % constants.LEN_BATTING_LIST
        bottom_offset = bottom_pa_index % constants.LEN_BATTING_LIST
        this_x_pos = inning_num * constants.BOX_WIDTH
        if inning_half_str == 'bottom':
            if summary != 'Runner Out':
                bottom_pa_index += 1

            this_y_pos = (constants.HEIGHT // 2 +
                          bottom_offset * constants.BOX_HEIGHT +
                          constants.BOX_HEIGHT // 2)
        elif inning_half_str == 'top':
            if summary != 'Runner Out':
                top_pa_index += 1

            this_y_pos = (top_offset * constants.BOX_HEIGHT +
                          constants.BOX_HEIGHT // 2)
        else:
            raise ValueError('Invalid inning half str')

        this_inning_tuple_list = [
            id_tuple for (id_tuple, _, _) in svg_content_list
            if id_tuple[0] == inning_num and id_tuple[1] == inning_half_str
        ]

        content_list_svg += write_individual_pa_svg(svg_content,
                                                    inning_pa_num,
                                                    this_inning_tuple_list,
                                                    this_x_pos,
                                                    this_y_pos)

    return content_list_svg

def get_game_title_str(game):
    game_teams_str = '{} @ {}'.format(game.away_team.name,
                                      game.home_team.name)

    return game_teams_str

def assemble_game_title_svg(game):
    game_title_svg = ''
    game_str = '{} @ {}'.format(
        game.away_team.name,
        game.home_team.name,
    )

    if game.first_pitch_str and game.last_pitch_str:
        game_datetime = '{}{}'.format(game.first_pitch_str, game.last_pitch_str)
    else:
        game_datetime = game.game_date_str

    game_width = get_game_width(game)

    tuple_list = [('TOP', 0), ('BOTTOM', constants.HEIGHT // 2)]
    for inning_half_str, y_pos in tuple_list:
        game_title_svg += constants.BIG_SVG_TITLE.format(
            x_pos=game_width - constants.BOX_WIDTH,
            y_pos=y_pos,
            inning_half=inning_half_str,
            game_str=game_str,
            location=game.location.replace('&', '&amp;'),
            datetime=game_datetime
        )

    return game_title_svg

def get_big_rectangles(game):
    game_width = get_game_width(game)

    big_rectangles_svg = '{}{}'.format(
        constants.BIG_RECTANGLE.format(y_pos=0,
                                       y_pos_2=constants.HEIGHT // 2,
                                       width=game_width),
        constants.BIG_RECTANGLE.format(y_pos=constants.HEIGHT // 2,
                                       y_pos_2=constants.HEIGHT,
                                       width=game_width)
    )

    return big_rectangles_svg

def get_footer_box(game):
    game_width = get_game_width(game)
    footer_box_svg = '{}'.format(constants.FOOTER_BOX.format(width=game_width))

    return footer_box_svg

def write_big_svg(game):
    big_svg_text = '{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}'.format(
        get_big_svg_header(game),
        get_batter_list_and_stats(game),
        assemble_stats_svg(game),
        assemble_box_content_dict(game),
        get_team_stats_svg(game),
        add_away_batter_sub_division_lines(game),
        add_home_batter_sub_division_lines(game),
        add_away_pitcher_sub_division_lines(game),
        add_home_pitcher_sub_division_lines(game),
        add_all_pitcher_box_scores(game),
        assemble_game_title_svg(game),
        get_signature(game),
        get_box_score_totals(game),
        get_big_rectangles(game),
        get_footer_box(game),
        constants.SVG_FOOTER
    )

    return big_svg_text

def wrap_in_html(title, filename):
    return constants.HTML_WRAPPER.format(title=title,
                                         filename=filename)

def generate_from_files(start_date_str, end_date_str, output_dir, input_dir):
    if not os.path.exists(input_dir):
        raise ValueError('Invalid input directory')

    input_path = os.path.abspath(input_dir)
    filename_tuple_list = fetch_game.get_filename_list(start_date_str,
                                                       end_date_str,
                                                       input_path)

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    output_path = os.path.abspath(output_dir)
    list_of_filename_tuple_lists = fetch_game.get_list_of_lists(
        filename_tuple_list,
        constants.NUM_SUBLISTS
    )

    for filename_tuple_list in list_of_filename_tuple_lists:
        process = multiprocessing.Process(
            target=write_file,
            args=(filename_tuple_list, output_path)
        )

        process.start()

def write_file(filename_tuple_list, output_path):
    for game_id, boxscore_file, player_file, inning_file in filename_tuple_list:
        this_game = fetch_game.get_game(boxscore_file, player_file, inning_file)
        svg_filename = game_id + '.svg'
        html_filename = game_id + '.html'
        print('Writing: ' + svg_filename)
        print('Writing: ' + html_filename)

        title = get_game_title_str(this_game)
        svg_text = write_big_svg(this_game)
        html_text = wrap_in_html(title, svg_filename)

        with open(output_path + '/' + svg_filename, 'w', encoding='utf-8') as fh:
            fh.write(svg_text)

        with open(output_path + '/' + html_filename, 'w', encoding='utf-8') as fh:
            fh.write(html_text)

def generate_from_url(date_str, away_code, home_code, game_num, output_dir):
    game_id, this_game = fetch_game.get_game_from_url(
        date_str, away_code, home_code, game_num
    )

    if this_game:
        svg_filename = game_id + '.svg'
        html_filename = game_id + '.html'
        title = get_game_title_str(this_game)
        svg_text = write_big_svg(this_game)
        html_text = wrap_in_html(title, svg_filename)

        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        output_path = os.path.abspath(output_dir)
        with open(output_path + '/' + svg_filename, 'w', encoding='utf-8') as fh:
            fh.write(svg_text)

        with open(output_path + '/' + html_filename, 'w', encoding='utf-8') as fh:
            fh.write(html_text)

        print(svg_filename)
        print(html_filename)

        status = True
    else:
        status = False

    return status

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(constants.GENERATE_SVG_USAGE_STR)
        exit()
    if sys.argv[1] == 'files' and len(sys.argv) == 6:
        generate_from_files(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    elif sys.argv[1] == 'url' and len(sys.argv) == 7:
        generate_from_url(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5],
                          sys.argv[6])
    else:
        print(constants.GENERATE_SVG_USAGE_STR)
