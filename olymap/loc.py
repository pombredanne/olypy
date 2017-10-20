#!/usr/bin/python

import math

from olypy.oid import to_oid
import olymap.utilities as u
from olymap.utilities import anchor
from olymap.utilities import anchor2
import olypy.details as details
from operator import itemgetter

pd_directions = {0: 'North', 1: 'East', 2: 'South', 3: 'West', 4: 'Up', 5: 'Down'}


def write_loc_page_header(v, k, data, outf):
    outf.write('<H3>')
    loc_type = u.return_type(v['firstline'][0])
    outf.write('{} [{}]'.format(v['na'][0], to_oid(k)))
    outf.write(', {}'.format(loc_type))
    if u.return_type(v['firstline'][0]) != 'region':
        outf.write(', in')
        if 'city' in loc_type:
            outf.write(' province ')
        try:
            loc2 = data[v['LI']['wh'][0]]
            outf.write(' {} [{}]'.format(loc2['na'][0],
                                         anchor(to_oid(u.return_unitid(loc2['firstline'][0])))))
        except KeyError:
            pass
    # if 'city' in loc_type:
    #    outf.write(' [{}]'.format(anchor(to_oid(v['LI']['wh'][0]))))
    if 'SL' in v:
        if 'sh' in v['SL']:
            outf.write(', safe haven')
    if 'LO' in v:
        if 'hi' in v['LO']:
            outf.write(', hidden')
    if loc_type != 'ocean' and u.loc_depth(u.return_type(v['firstline'][0])) == 2 \
            and data[u.region(k, data)]['na'][0] != 'faery' and data[u.region(k, data)]['na'][0] != 'hades':
        civ_level = 'wilderness'
        if 'LO' in v:
            if 'lc' in v['LO']:
                if v['LO']['lc'][0] == '0':
                    civ_level = 'wilderness'
                else:
                    civ_level = 'civ-' + v['LO']['lc'][0]
        outf.write(', {}'.format(civ_level))
    outf.write('</H3>\n')


def write_loc_shroud(v, k, outf):
    if 'LO' in v:
        if 'sh' in v['LO']:
            if int(v['LO']['sh'][0]) > 0:
                outf.write('<p>A magical barrier surrounds {} [{}].</p>\n'.format(v['na'][0],
                                                                                  anchor(to_oid(k))))


def write_loc_barrier(v, k, outf):
    if 'LO' in v:
        if 'ba' in v['LO']:
            if int(v['LO']['ba'][0]) > 0:
                outf.write('<p>A magical shroud surrounds {} [{}].</p>\n'.format(v['na'][0],
                                                                                 anchor(to_oid(k))))


def write_loc_controlled_by(v, data, outf):
    if 'LI' in v:
        if 'hl' in v['LI']:
            here_list = v['LI']['hl']
            if len(here_list) > 0:
                for loc in here_list:
                    try:
                        charac = data[loc]
                        if 'MI' in charac:
                            if 'gc' in charac['MI']:
                                if int(charac['MI']['gc'][0]) != 0:
                                    dest_loc = data[charac['MI']['gc'][0]]
                                    dest_loc2 = data[dest_loc['LI']['wh'][0]]
                                    outf.write('<p>Province controlled by ')
                                    dest_name = dest_loc['na'][0]
                                    dest_id = anchor(to_oid(u.return_unitid(dest_loc['firstline'][0])))
                                    dest_type = u.return_type(dest_loc['firstline'][0])
                                    outf.write('{} [{}], {}'.format(dest_name, dest_id, dest_type))
                                    dest_type2 = u.return_type(dest_loc2['firstline'][0])
                                    if 'city' not in dest_type2:
                                        dest_name2 = dest_loc2['na'][0]
                                        dest_id2 = anchor(to_oid(u.return_unitid(dest_loc2['firstline'][0])))
                                        outf.write(', in {} [{}]'.format(dest_name2, dest_id2))
                                    else:
                                        dest_loc2 = data[dest_loc2['LI']['wh'][0]]
                                        dest_name2 = dest_loc2['na'][0]
                                        dest_id2 = anchor(to_oid(u.return_unitid(dest_loc2['firstline'][0])))
                                        outf.write(', in {} [{}]'.format(dest_name2, dest_id2))
                                    try:
                                        garrison = data[dest_loc2['LI']['hl'][0]]
                                        garr_type = u.return_type(garrison['firstline'][0])
                                        if garr_type == 'garrison':
                                            # calculate top of pledge chain
                                            if 'LI' in dest_loc:
                                                if 'hl' in dest_loc['LI']:
                                                    top_guy = u.top_ruler(dest_loc['LI']['hl'][0],data)
                                                    a = ''
                                                    b = ''
                                                    try:
                                                        top_dog = data[top_guy]
                                                        a = top_dog['na'][0]
                                                        b = anchor(to_oid(top_guy))
                                                        outf.write('<br>Ruled by {} [{}]'.format(a, b))
                                                    except KeyError:
                                                        pass
                                    except KeyError:
                                        pass
                                    outf.write('</p>\n')
                    except KeyError:
                        pass


def write_province_destination(loc, dest_loc, direction, data, outf):
    if (u.is_port_city(dest_loc, data) or
        u.province_has_port_city(dest_loc, data) != '0') and \
        u.return_type(loc['firstline'][0]) == 'ocean':
        if u.is_port_city(dest_loc, data) == False:
            dest_loc = data[u.province_has_port_city(dest_loc, data)]
        dest_loc_host = data[dest_loc['LI']['wh'][0]]
        outf.write('<li>{}, port city, to {} [{}]'
                   .format(direction,
                           dest_loc['na'][0],
                           anchor(to_oid(u.return_unitid(dest_loc['firstline'][0])))))
        if u.region(u.return_unitid(loc['firstline'][0]), data) != u.region(u.return_unitid(dest_loc['firstline'][0]), data):
            region_key = u.return_unitid(dest_loc['firstline'][0])
            region_rec = data[u.region(region_key, data)]
            outf.write(', {}'.format(region_rec['na'][0]))
        barrier = int(0)
        if 'LO' in dest_loc:
            if 'ba' in dest_loc['LO']:
                barrier = int(dest_loc['LO']['ba'][0])
        if barrier > 0:
            outf.write(', impassable<br>&nbsp;&nbsp;&nbsp;A magical barrier prevents entry.')
        else:
            out_distance = u.calc_exit_distance(loc, dest_loc)
            outf.write(', {} {}'.format(out_distance,
                                        'day' if out_distance == 1 else 'days'))
        outf.write('</li>\n')
        outf.write('<li> {}, to {} [{}]'.format(direction,
                                                dest_loc_host['na'][0],
                                                anchor(to_oid(u.return_unitid(dest_loc_host['firstline'][0])))))
        if u.region(u.return_unitid(loc['firstline'][0]), data) != \
           u.region(u.return_unitid(dest_loc['firstline'][0]), data):
            region_key = u.return_unitid(dest_loc_host['firstline'][0])
            region_rec = data[u.region(region_key, data)]
            outf.write(', {}'.format(region_rec['na'][0]))
        barrier = int(0)
        if 'LO' in dest_loc_host:
            if 'ba' in dest_loc_host['LO']:
                barrier = int(dest_loc_host['LO']['ba'][0])
        if barrier > 0:
            outf.write(', impassable<br>&nbsp;&nbsp;&nbsp;A magical barrier prevents entry.')
        else:
            outf.write(', impassable')
        outf.write('</li>\n')
    else:
        outf.write('<li>{}'.format(direction))
        if direction == 'Out':
            outf.write(', {}'.format(u.return_type(dest_loc['firstline'][0])))
        outf.write(', to {} [{}]'.format(dest_loc['na'][0],
                                         anchor(to_oid(u.return_unitid(dest_loc['firstline'][0])))))
        if u.region(u.return_unitid(loc['firstline'][0]), data) != \
                u.region(u.return_unitid(dest_loc['firstline'][0]), data):
            region_key = u.return_unitid(dest_loc['firstline'][0])
            region_rec = data[u.region(region_key, data)]
            outf.write(', {}'.format(region_rec['na'][0]))
        barrier = int(0)
        if 'LO' in dest_loc:
            if 'ba' in dest_loc['LO']:
                barrier = int(dest_loc['LO']['ba'][0])
        if barrier > 0:
            outf.write(', impassable<br>&nbsp;&nbsp;&nbsp;A magical barrier prevents entry.')
        elif u.return_type(loc['firstline'][0]) == 'ocean' and u.return_type(dest_loc['firstline'][0]) == 'mountain':
            outf.write(', impassable')
        else:
            out_distance = u.calc_exit_distance(loc, dest_loc)
            outf.write(', {} {}'.format(out_distance,
                                        'day' if out_distance == 1 else 'days'))
        outf.write('</li>\n')


def write_province_destinations(v, data, outf):
    outf.write('<H4>Routes leaving {}:</H4>\n'.format(v['na'][0]))
    outf.write('<ul>\n')
    pd_list = v['LO']['pd']
    i = int(0)
    for pd in pd_list:
        if int(pd) != 0:
            write_province_destination(v,
                                       data[pd],
                                       pd_directions[i],
                                       data,
                                       outf)
        i = i + 1
    outf.write('</ul>\n')


def write_loc_routes_out(v, data, outf):
    if 'city' not in u.return_type(v['firstline'][0]):
        if 'LO' in v:
            if 'pd' in v['LO']:
                if len(v['LO']['pd']) > 0:
                    write_province_destinations(v, data, outf)
    else:
        outf.write('<H4>Routes leaving {}:</H4\n'.format(v['na'][0]))
        outf.write('<ul>\n')
        host_prov = data[v['LI']['wh'][0]]
        # If city is in a mountain, can't move from city to ocean
        if 'mountain' not in u.return_type(host_prov['firstline'][0]):
            dest_loc_list = host_prov['LO']['pd']
            i = int(0)
            for pd in dest_loc_list:
                try:
                    pd_loc = data[pd]
                    if 'ocean' in u.return_type(pd_loc['firstline'][0]):
                        pd_name = pd_loc['na'][0]
                        pd_loc_id = u.return_unitid(pd_loc['firstline'][0])
                        out_distance = u.calc_exit_distance(v, pd_loc)
                        outf.write('<li>{}, to {} [{}], {}, {} {}</li>\n'
                                   .format(pd_directions[i],
                                           pd_name,
                                           anchor(to_oid(pd_loc_id)),
                                           data[u.region(pd_loc_id, data)]['na'][0],
                                           out_distance,
                                           'day' if out_distance == 1 else 'days'))
                except KeyError:
                    pass
                i = i + 1
        out_distance = u.calc_exit_distance(v, host_prov)
        outf.write('<li>Out, to {} [{}], {} {}</li>\n'
                   .format(host_prov['na'][0],
                           anchor(to_oid(u.return_unitid(host_prov['firstline'][0]))),
                           out_distance,
                           'day' if out_distance == 1 else 'days'))
        outf.write('</ul>\n')


def write_structure_basic_info(v, outf):
    try:
        defense = int(v['SL']['de'][0])
    except KeyError:
        defense = 0
    try:
        damage = int(v['SL']['dea'][0])
    except KeyError:
        damage = 0
    try:
        effort_given = int(v['SL']['eg'][0])
    except KeyError:
        effort_given = 0
    try:
        effort_required = int(v['SL']['er'][0])
    except KeyError:
        effort_required = 0
    try:
        depth = int(v['SL']['sd'][0])
    except KeyError:
        depth = 0
    try:
        level = int(v['SL']['cl'][0])
    except KeyError:
        level = 0
    if defense > 0 or damage > 0 or effort_given < effort_required:
        outf.write('<table>\n')
        if effort_given < effort_required:
            outf.write('<tr><td>Percent Complete:</td><td>{}%</td></tr>\n'
                       .format(int(effort_given / effort_required) * 100))
        if defense > 0:
            outf.write('<tr><td>Defense:</td><td>{}</td></tr>\n'
                       .format(defense))
        outf.write('<tr><td>Damage:</td><td>{}%</td></tr>\n'
                   .format(damage))
        if depth > 0:
            outf.write('<tr><td>Level:</td><td>{}</td></tr>\n'
                       .format(int(depth / 3)))
        if u.return_type(v['firstline'][0]) == 'castle':
            outf.write('<tr><td>Level:</td><td>{}</td></tr>\n'
                       .format(level))
        outf.write('</table>\n')


def write_loc_skills_report(v, data, outf):
    if 'SL' in v:
        if 'te' in v['SL']:
            skills_list = v['SL']['te']
            if len(skills_list) > 0:
                outf.write('<H4> Skills taught here:</H4>\n')
                outf.write('<ul>\n')
                for skill in skills_list:
                    outf.write('<li>{} [{}]</li>\n'
                                .format(data[skill]['na'][0],
                                        anchor(to_oid(skill))))
                outf.write('</ul>\n')


def write_loc_market_report(v, k, data, outf, trade_chain):
    try:
        trade_list = v['tl']
    except KeyError:
        return
    # load city/character trades
    city_trade_list = []
    if len(trade_list) > 0:
        # city trades
        iterations = int(len(trade_list) / 8)
        for trade in range(0, iterations):
            if trade_list[(trade * 8) + 0] in {'1', '2'}:
                city_trade_list.append([trade_list[(trade * 8) + 0],
                                        trade_list[(trade * 8) + 1],
                                        k,
                                        trade_list[(trade * 8) + 2],
                                        trade_list[(trade * 8) + 3]])
        # character trades - needs to be recursive
        if 'LI' in v:
            if 'hl' in v['LI']:
                seen_here_list = v['LI']['hl']
            else:
                seen_here_list = []
        else:
            seen_here_list = []
        list_length = len(seen_here_list)
        if list_length > 1:
            for un in seen_here_list[1:]:
                charac_rec = data[un]
                if u.return_kind(charac_rec['firstline'][0]) == 'char':
                    if 'tl' in charac_rec:
                        trade_list = charac_rec['tl']
                        if len(trade_list) > 0:
                            # character trades
                            iterations = int(len(trade_list) / 8)
                            for trade in range(0, iterations):
                                if trade_list[(trade * 8) + 0] in {'1', '2'}:
                                    city_trade_list.append([trade_list[(trade * 8) + 0],
                                                            trade_list[(trade * 8) + 1],
                                                            un,
                                                            trade_list[(trade * 8) + 2],
                                                            trade_list[(trade * 8) + 3]])
    if len(city_trade_list) > 0:
        sorted_list = sorted(city_trade_list, key=itemgetter(0, 1, 2))
        outf.write('<H4>Market Report:</H4>\n')
        outf.write('<table border="1" cellpadding="5">\n')
        outf.write('<tr>')
        outf.write('<th>trade</th><th>who</th><th>price</th><th>qty</th><th>wt/ea</th><th>item</th><th>recip who</th><th>recip price</th><th>recip qty</th>\n')
        outf.write('</tr>\n')
        for trade in sorted_list:
            if trade[0] in {'1', '2'}:
                trade_kind = 'buy' if trade[0] == '1' else 'sell'
                item_rec = data[trade[1]]
                trade_item = anchor(to_oid(trade[1]))
                trade_qty = trade[3]
                trade_price = trade[4]
                trade_who = anchor(to_oid(trade[2]))
                trade_recip = trade_chain[trade[1]]
                recip_name = ''
                recip_loc = '0'
                if len(trade_recip) > 0:
                    for recip in trade_recip:
                        if recip[0] != k:
                            recip_type = recip[1]
                            if recip_type != trade[0]:
                                recip_loc = recip[0]
                                recip_rec = data[recip_loc]
                                recip_name = recip_rec['na'][0]
                outf.write('<tr>')
                outf.write('<td>{}</td>\n'.format(trade_kind))
                outf.write('<td>{}</td>\n'.format(trade_who))
                outf.write('<td>{}</td>\n'.format(trade_price))
                outf.write('<td>{}</td>\n'.format(trade_qty))
                outf.write('<td>{}</td>\n'.format(item_rec['IT']['wt'][0]))
                outf.write('<td>{} [{}]</td>\n'.format(item_rec['na'][0], trade_item))
                if recip_loc != '0':
                    outf.write('<td>{} [{}]</td>\n'.format(recip_name,
                                                           anchor(to_oid(recip_loc))))
                    recip_trade_list = recip_rec['tl']
                    recip_iterations = int(len(recip_trade_list) / 8)
                    for recip in range(0, recip_iterations):
                        if recip_trade_list[(recip * 8) + 1] == trade[1]:
                            if recip_trade_list[(recip * 8) + 0] in {'1','2'}:
                                recip_qty = recip_trade_list[(recip * 8) + 2]
                                recip_price = recip_trade_list[(recip * 8) + 3]
                                outf.write('<td>{}</td>\n'.format(recip_price))
                                outf.write('<td>{}</td>\n'.format(recip_qty))
                else:
                    outf.write('<td>&nbsp;</td>\n')
                    outf.write('<td>&nbsp;</td>\n')
                    outf.write('<td>&nbsp;</td>\n')
            outf.write('</tr>\n')
        outf.write('</table>\n')


def write_characters(v, k, data, outf):
    outf.write('<li>')
    # code fix to bug in lib where garrison name is sometimes missing
    if u.return_type(v['firstline'][0]) == 'garrison':
        name = 'Garrison'
    else:
        name = v['na'][0]
    outf.write('{} [{}]'.format(name,
                                anchor(to_oid(k))))
    if u.xlate_loyalty(v) not in {'Undefined', 'Npc'}:
        outf.write(' ({}'.format(u.xlate_loyalty(v)))
        if 'CH' in v:
            if 'sl' in v['CH']:
                skills_list = v['CH']['sl']
                if int(len(skills_list)) > 0:
                    iterations = int(len(skills_list) / 5)
                    for skill in range(0, iterations):
                        if skills_list[skill * 5] == '909':
                            if skills_list[(skill * 5) + 1] == '2':
                                outf.write(':AB')
        outf.write(')')
    else:
        if 'CH' in v:
            if 'sl' in v['CH']:
                skills_list = v['CH']['sl']
                if int(len(skills_list)) > 0:
                    iterations = int(len(skills_list) / 5)
                    for skill in range(0, iterations):
                        if skills_list[skill * 5] == '909':
                            if skills_list[(skill * 5) + 1] == '2':
                                outf.write('(AB')
    if u.return_type(v['firstline'][0]) != '0':
        outf.write(', {}'.format(u.return_type(v['firstline'][0])))
    if 'CH' in v:
        if 'pr' in v['CH']:
            if v['CH']['pr'][0] == '2':
                outf.write(', prisoner')
    if u.is_priest(v):
        outf.write(', priest')
    if u.is_magician(v):
        if u.xlate_magetype(v) not in {'', 'undefined'}:
            outf.write(', {}'.format(u.xlate_magetype(v)))
    if 'CH' in v:
        if 'gu' in v['CH']:
            if v['CH']['gu'][0] == '1':
                outf.write(', on guard')
    if 'CH' in v:
        if 'hs' in v['CH']:
            if v['CH']['hs'][0] == '1':
                outf.write(' concealed')
    if 'il' in v:
        item_list = v['il']
        iterations = int(len(item_list) / 2)
        if iterations > 0:
            for items in range(0, iterations):
                itemz = data[item_list[items * 2]]
                if 'IT' in itemz:
                    if 'pr' in itemz['IT']:
                        if itemz['IT']['pr'][0] == '1':
                            item_name = itemz['na'][0] if int(item_list[(items * 2) + 1]) == 1 else itemz['IT']['pl'][0]
                            outf.write(', {} {}'.format(item_list[(items * 2) + 1], item_name))
    if 'LI' in v:
        if 'hl' in v['LI']:
            outf.write(', accompanied by: ')
    outf.write('</li>\n')
    if 'LI' in v:
        if 'hl' in v['LI']:
            here_list = v['LI']['hl']
            if len(here_list) > 0:
                outf.write('<ul>\n')
                for here in here_list:
                    charac = data[here]
                    write_characters(charac, here, data, outf)
                outf.write('</ul>\n')


def write_sub_locs(loc, sub_loc, k, data, outf):
    outf.write('<li>')
    outf.write('{} [{}], {}'.format(sub_loc['na'][0],
                                      anchor(to_oid(k)),
                                      u.return_type(sub_loc['firstline'][0])))
    if 'LO' in sub_loc:
        if 'hi' in sub_loc['LO']:
            outf.write(', hidden')
    out_distance = u.calc_exit_distance(loc, sub_loc)
    if out_distance > 0:
        outf.write(', {} {}'.format(out_distance,
                                    'day' if out_distance == 1 else 'days'))
    if 'SL' in sub_loc:
        if 'de' in sub_loc['SL']:
            outf.write(', defense {}'.format(sub_loc['SL']['de'][0]))
    if 'castle' in u.return_type(sub_loc['firstline'][0]):
        if 'SL' in sub_loc:
            if 'cl' in sub_loc['SL']:
                if int(sub_loc['SL']['cl'][0]) > 0:
                    outf.write(', level {}'.format(sub_loc['SL']['cl'][0]))
    if 'mine' in u.return_type(sub_loc['firstline'][0]):
        if 'SL' in sub_loc:
            if 'sd' in sub_loc['SL']:
                if int(sub_loc['SL']['sd'][0]) > 0:
                    outf.write(', level {}'.format(int(sub_loc['SL']['sd'][0]) / 3))
    if 'SL' in sub_loc:
        if 'eg' and 'er' in sub_loc['SL']:
            effort_given = int(sub_loc['SL']['eg'][0])
            effort_required = int(sub_loc['SL']['er'][0])
            pct_complete = int(float(effort_given / effort_required)*100)
            outf.write(', {}% completed'.format(pct_complete))
    if 'SL' in sub_loc:
        if 'da' in sub_loc['SL']:
            outf.write(', {}% damaged'.format(sub_loc['SL']['da'][0]))
    if 'LI' in sub_loc:
        if 'hl' in sub_loc['LI']:
            sub_here_list = sub_loc['LI']['hl']
            if len(sub_here_list) > 0:
                first_here = data[sub_here_list[0]]
                if u.return_kind(first_here['firstline'][0]) == 'char':
                    outf.write(', owner:')
    outf.write('</li>\n')
    # see if stuff stacked under it
    if 'LI' in sub_loc:
        if 'hl' in sub_loc['LI']:
            sub_here_list = sub_loc['LI']['hl']
            if len(sub_here_list) > 0:
                outf.write('<ul>\n')
                for sub_hl in sub_here_list:
                    sub_sub_here = data[sub_hl]
                    if u.return_kind(sub_sub_here['firstline'][0]) == 'loc':
                        write_sub_locs(sub_loc,
                                       sub_sub_here,
                                       sub_hl,
                                       data,
                                       outf)
                    elif u.return_kind(sub_sub_here['firstline'][0]) == 'char':
                        write_characters(sub_sub_here,
                                         u.return_unitid(sub_sub_here['firstline'][0]),
                                         data, outf)
                    elif u.return_kind(sub_sub_here['firstline'][0]) == 'ship':
                        write_ships(sub_sub_here,
                                    u.return_unitid(sub_sub_here['firstline'][0]),
                                    data,
                                    outf)
                outf.write('</ul>\n')


def write_ships(v, k, data, outf):
    outf.write('<li>\n')
    outf.write('{} [{}], {}'.format(v['na'][0],
                                    anchor(to_oid(k)),
                                    u.return_type(v['firstline'][0])))
    if 'SL' in v:
        if 'bs' in v['SL']:
            storm = data[v['SL']['bs'][0]]
            if 'na' in storm:
                name = storm['na'][0]
            else:
                name = u.return_type(storm['firstline'][0])
            outf.write(', {} [{}] (strength: {})'.format(name,
                                                       anchor(to_oid(v['SL']['bs'][0])),
                                                       storm['MI']['ss'][0]))
    if 'SL' in v:
        if 'de' in v['SL']:
            outf.write(', defense {}'.format(v['SL']['de'][0]))
        if 'eg' and 'er' in v['SL']:
            effort_given = int(v['SL']['eg'][0])
            effort_required = int(v['SL']['er'][0])
            pct_complete = int(float(effort_given / effort_required)*100)
            outf.write(', {}% completed'.format(pct_complete))
        if 'da' in v['SL']:
            outf.write(', {}% damaged'.format(v['SL']['da'][0]))
    if 'LI' in v:
        if 'hl' in v['LI']:
            sub_here_list = v['LI']['hl']
            if len(sub_here_list) > 0:
                first_here = data[sub_here_list[0]]
                if u.return_kind(first_here['firstline'][0]) == 'char':
                    outf.write(', owner:')
    outf.write('</li>\n')
    # see if stuff stacked under it
    if 'LI' in v:
        if 'hl' in v['LI']:
            sub_here_list = v['LI']['hl']
            if len(sub_here_list) > 0:
                outf.write('<ul>\n')
                for sub_hl in sub_here_list:
                    sub_sub_here = data[sub_hl]
                    if u.return_kind(sub_sub_here['firstline'][0]) == 'loc':
                        write_sub_locs(v, sub_sub_here, sub_hl, data, outf)
                    elif u.return_kind(sub_sub_here['firstline'][0]) == 'char':
                        write_characters(sub_sub_here,
                                         u.return_unitid(sub_sub_here['firstline'][0]),
                                         data, outf)
                outf.write('</ul>\n')


def write_storms(v, k, outf):
    outf.write('<li>\n')
    if 'na' in v:
        name = v['na'][0]
    else:
        name = u.return_type(v['firstline'][0]).capitalize()
    outf.write('{} [{}], {}'.format(name,
                                    anchor(to_oid(k)),
                                    u.return_type(v['firstline'][0])))
    if 'MI' in v:
        if 'ss' in v['MI']:
            outf.write(' (strength: {})'.format(v['MI']['ss'][0]))
    outf.write('</li>\n')


def write_inner_locs(v, data, outf, here_list):
    outf.write('<ul>\n')
    for here in here_list:
        here_rec = data[here]
        if u.return_kind(here_rec['firstline'][0]) == 'loc':
            write_sub_locs(v, here_rec, u.return_unitid(here_rec['firstline'][0]),
                           data, outf)
    outf.write('</ul>\n')


def write_seen_here(data, outf, here_list):
    outf.write('<ul>\n')
    for here in here_list:
        here_rec = data[here]
        if u.return_kind(here_rec['firstline'][0]) == 'char':
            write_characters(here_rec, here, data, outf)
    outf.write('</ul>\n')


def write_ships_docked(data, outf, here_list):
    outf.write('<ul>\n')
    for here in here_list:
        here_rec = data[here]
        if u.return_kind(here_rec['firstline'][0]) == 'ship':
            write_ships(here_rec, here, data, outf)
    outf.write('</ul>\n')


def write_storms_here(data, outf, here_list):
    outf.write('<ul>\n')
    for here in here_list:
        here_rec = data[here]
        if u.return_kind(here_rec['firstline'][0]) == 'storm':
            write_storms(here_rec, here, outf)
    outf.write('</ul>\n')


def write_here_list(v, data, outf):
    try:
        here_list = v['LI']['hl']
    except KeyError:
        return
    print_inner = False
    seen_here = False
    ships_docked = False
    storms_here = False
    for here in here_list:
        here_rec = data[here]
        if u.return_kind(here_rec['firstline'][0]) == 'loc':
            print_inner = True
        elif u.return_kind(here_rec['firstline'][0]) == 'char':
            seen_here = True
        elif u.return_kind(here_rec['firstline'][0]) == 'ship':
            ships_docked = True
        elif u.return_kind(here_rec['firstline'][0]) == 'storm':
            storms_here = True
    if print_inner:
        outf.write('<H4>Inner Locations:</H4>\n')
        write_inner_locs(v, data, outf, here_list)
    if seen_here:
        outf.write('<H4>Seen Here:</H4>\n')
        write_seen_here(data, outf, here_list)
    if ships_docked:
        outf.write('<H4>{}:</H4>\n'.format('Ships docked' if u.return_type(v['firstline'][0]) != 'ocean' else 'Ships sighted'))
        write_ships_docked(data, outf, here_list)
    if storms_here:
        outf.write('<H4>Storms Here:</H4>\n')
        write_storms_here(data, outf, here_list)


def write_hidden_access(v, k, data, outf, hidden_chain):
    if 'LO' in v:
        if 'hi' in v['LO']:
            if v['LO']['hi'][0] == '1' or \
                    u.region(k, data) in {'faery', 'hades'}:
                # PL/kn
                try:
                    hidden_list = hidden_chain[k]
                    if len(hidden_list) > 0:
                        outf.write('Hidden location known by:</H4>\n')
                        outf.write('<ul>\n')
                        for hidden in hidden_list:
                            hidden_rec = data[hidden]
                            outf.write('<li>{} [{}]</td></li>\n'.format(hidden_rec['na'][0],
                                                                        anchor(to_oid(hidden))))
                        outf.write('</ul>\n')
                finally:
                    pass


def write_garrisons(v, k, data, outf, garrisons_chain):
    if u.return_type(v['firstline'][0]) == 'castle':
        garrison_list = garrisons_chain[k]
        if len(garrison_list) > 0:
            province_list = []
            for garrison in garrison_list:
                province = data[garrison]
                province_list.append(province['LI']['wh'][0])
            province_list.sort()
            outf.write('<H4>Garrisons:</H4>\n')
            outf.write('<table>\n')
            rows = int(math.ceil(len(province_list) / 5))
            for garrison in range(0, rows):
                outf.write('<tr>')
                if (rows * 0) + garrison < len(province_list):
                    province_rec = data[province_list[(rows * 0) + garrison]]
                    outf.write('<td>{} [{}]</td>'.format(province_rec['na'][0],
                                                         anchor(to_oid(u.return_unitid(
                                                         province_rec['firstline'][0])))))
                else:
                    outf.write('<td></td>')
                if (rows * 1) + garrison < len(province_list):
                    province_rec = data[province_list[(rows * 1) + garrison]]
                    outf.write('<td>{} [{}]</td>'.format(province_rec['na'][0],
                                                         anchor(to_oid(u.return_unitid(
                                                         province_rec['firstline'][0])))))
                else:
                    outf.write('<td></td>')
                if (rows * 2) + garrison < len(province_list):
                    province_rec = data[province_list[(rows * 2) + garrison]]
                    outf.write('<td>{} [{}]</td>'.format(province_rec['na'][0],
                                                         anchor(to_oid(u.return_unitid(
                                                         province_rec['firstline'][0])))))
                else:
                    outf.write('<td></td>')
                if(rows * 3) + garrison < len(province_list):
                    province_rec = data[province_list[(rows * 3) + garrison]]
                    outf.write('<td>{} [{}]</td>'.format(province_rec['na'][0],
                                                         anchor(to_oid(u.return_unitid(
                                                         province_rec['firstline'][0])))))
                else:
                    outf.write('<td></td>')
                if (rows * 4) + garrison < len(province_list):
                    province_rec = data[province_list[(rows * 4) + garrison]]
                    outf.write('<td>{} [{}]</td>'.format(province_rec['na'][0],
                                                         anchor(to_oid(u.return_unitid(
                                                         province_rec['firstline'][0])))))
                else:
                    outf.write('<td></td>')
                outf.write('</tr>\n')
            outf.write('</table>\n')


def write_loc_map_anchor(v, k, data, outf):
    if int(k) >= 10000 and int(k) < 18000:
        x_coord = int(10 * math.floor((int(k) % 100) / 10))
        if x_coord >= 70:
            x_coord = 60
        y_coord = int(1000 * math.floor(int(k) / 1000))
        if y_coord >= 17000:
            y_coord = 16000
        outf.write('<p>{}</p>\n'.format(anchor2('main_map_leaf_'+ to_oid(y_coord + x_coord), 'Return to map')))
    elif (int(k) >= 56760 and int(k) < 57860) or (int(k) >= 59000 and int(k) < 79000):
        # determine host province
        if u.return_type(v['firstline'][0]) in details.province_kinds:
            p = k
        else:
            v = data[v['LI']['wh'][0]]
            k = u.return_unitid(v['firstline'][0])
            if u.return_type(v['firstline'][0]) in details.province_kinds:
                p = k
            else:
                v = data[v['LI']['wh'][0]]
                k = u.return_unitid(v['firstline'][0])
                if u.return_type(v['firstline'][0]) in details.province_kinds:
                    p = k
                else:
                    v = data[v['LI']['wh'][0]]
                    k = u.return_unitid(v['firstline'][0])
                    if u.return_type(v['firstline'][0]) in details.province_kinds:
                        p = k
        x_coord = int(10 * math.floor((int(p) % 100) / 10))
        if x_coord >= 70:
            x_coord = 60
        y_coord = int(1000 * math.floor(int(p) / 1000))
        if y_coord >= 17000:
            y_coord = 16000
        outf.write('<p>{}</p>\n'.format(anchor2('main_map_leaf_' + to_oid(y_coord + x_coord), 'Return to map')))


def write_loc_basic_info(v, k, data, outf, hidden_chain, garrisons_chain, trade_chain):
    write_loc_map_anchor(v, k, data, outf)
    write_loc_barrier(v, k, outf)
    write_loc_shroud(v, k, outf)
    write_loc_controlled_by(v, data, outf)
    write_loc_routes_out(v, data, outf)
    # not doing nearby cities because lib doesn't support
    write_structure_basic_info(v, outf)
    write_loc_skills_report(v, data, outf)
    write_loc_market_report(v, k, data, outf, trade_chain)
    write_here_list(v, data, outf)
    write_hidden_access(v, k, data, outf, hidden_chain)
    write_garrisons(v, k, data, outf, garrisons_chain)
    write_loc_map_anchor(v, k, data, outf)


def write_loc_html(v, k, data, hidden_chain, garrisons_chain, trade_chain):
    # generate loc page
    outf = open(to_oid(k)+'.html', 'w')
    outf.write('<HTML>\n')
    outf.write('<HEAD>\n')
    name = v['na'][0]
    try:
        loc2 = data[v['LI']['wh'][0]]
        loc2_name = ', in ' + loc2['na'][0]
    except KeyError:
        loc2_name = ''
    outf.write('<TITLE>{} [{}], {}{}'.format(name,
               to_oid(k), u.return_type(v['firstline'][0]), loc2_name))
    outf.write('</TITLE>\n')
    outf.write('</HEAD>\n')
    outf.write('<BODY>\n')
    write_loc_page_header(v, k, data, outf)
    write_loc_basic_info(v, k, data, outf, hidden_chain, garrisons_chain, trade_chain)
    outf.write('</BODY>\n')
    outf.write('</HTML>\n')
    outf.close()
