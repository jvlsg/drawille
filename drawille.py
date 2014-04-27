# -*- coding: utf-8 -*-

# drawille is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# drawille is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with drawille. If not, see < http://www.gnu.org/licenses/ >.
#
# (C) 2014- by Adam Tauber, <asciimoo@gmail.com>

from collections import defaultdict
import math

"""

source: http://www.alanwood.net/unicode/braille_patterns.html

dots:
   ,___,
   |1 4|
   |2 5|
   |3 6|
   |7 8|
   `````
"""

pixel_map = (('1', '4'),
             ('2', '5'),
             ('3', '6'),
             ('7', '8'))

braille_map = {
''         : '⠀',
'1'        : '⠁',
'2'        : '⠂',
'12'       : '⠃',
'3'        : '⠄',
'13'       : '⠅',
'23'       : '⠆',
'123'      : '⠇',
'4'        : '⠈',
'14'       : '⠉',
'24'       : '⠊',
'124'      : '⠋',
'34'       : '⠌',
'134'      : '⠍',
'234'      : '⠎',
'1234'     : '⠏',
'5'        : '⠐',
'15'       : '⠑',
'25'       : '⠒',
'125'      : '⠓',
'35'       : '⠔',
'135'      : '⠕',
'235'      : '⠖',
'1235'     : '⠗',
'45'       : '⠘',
'145'      : '⠙',
'245'      : '⠚',
'1245'     : '⠛',
'345'      : '⠜',
'1345'     : '⠝',
'2345'     : '⠞',
'12345'    : '⠟',
'6'        : '⠠',
'16'       : '⠡',
'26'       : '⠢',
'126'      : '⠣',
'36'       : '⠤',
'136'      : '⠥',
'236'      : '⠦',
'1236'     : '⠧',
'46'       : '⠨',
'146'      : '⠩',
'246'      : '⠪',
'1246'     : '⠫',
'346'      : '⠬',
'1346'     : '⠭',
'2346'     : '⠮',
'12346'    : '⠯',
'56'       : '⠰',
'156'      : '⠱',
'256'      : '⠲',
'1256'     : '⠳',
'356'      : '⠴',
'1356'     : '⠵',
'2356'     : '⠶',
'12356'    : '⠷',
'456'      : '⠸',
'1456'     : '⠹',
'2456'     : '⠺',
'12456'    : '⠻',
'3456'     : '⠼',
'13456'    : '⠽',
'23456'    : '⠾',
'123456'   : '⠿',
'7'        : '⡀',
'17'       : '⡁',
'27'       : '⡂',
'127'      : '⡃',
'37'       : '⡄',
'137'      : '⡅',
'237'      : '⡆',
'1237'     : '⡇',
'47'       : '⡈',
'147'      : '⡉',
'247'      : '⡊',
'1247'     : '⡋',
'347'      : '⡌',
'1347'     : '⡍',
'2347'     : '⡎',
'12347'    : '⡏',
'57'       : '⡐',
'157'      : '⡑',
'257'      : '⡒',
'1257'     : '⡓',
'357'      : '⡔',
'1357'     : '⡕',
'2357'     : '⡖',
'12357'    : '⡗',
'457'      : '⡘',
'1457'     : '⡙',
'2457'     : '⡚',
'12457'    : '⡛',
'3457'     : '⡜',
'13457'    : '⡝',
'23457'    : '⡞',
'123457'   : '⡟',
'67'       : '⡠',
'167'      : '⡡',
'267'      : '⡢',
'1267'     : '⡣',
'367'      : '⡤',
'1367'     : '⡥',
'2367'     : '⡦',
'12367'    : '⡧',
'467'      : '⡨',
'1467'     : '⡩',
'2467'     : '⡪',
'12467'    : '⡫',
'3467'     : '⡬',
'13467'    : '⡭',
'23467'    : '⡮',
'123467'   : '⡯',
'567'      : '⡰',
'1567'     : '⡱',
'2567'     : '⡲',
'12567'    : '⡳',
'3567'     : '⡴',
'13567'    : '⡵',
'23567'    : '⡶',
'123567'   : '⡷',
'4567'     : '⡸',
'14567'    : '⡹',
'24567'    : '⡺',
'124567'   : '⡻',
'34567'    : '⡼',
'134567'   : '⡽',
'234567'   : '⡾',
'1234567'  : '⡿',
'8'        : '⢀',
'18'       : '⢁',
'28'       : '⢂',
'128'      : '⢃',
'38'       : '⢄',
'138'      : '⢅',
'238'      : '⢆',
'1238'     : '⢇',
'48'       : '⢈',
'148'      : '⢉',
'248'      : '⢊',
'1248'     : '⢋',
'348'      : '⢌',
'1348'     : '⢍',
'2348'     : '⢎',
'12348'    : '⢏',
'58'       : '⢐',
'158'      : '⢑',
'258'      : '⢒',
'1258'     : '⢓',
'358'      : '⢔',
'1358'     : '⢕',
'2358'     : '⢖',
'12358'    : '⢗',
'458'      : '⢘',
'1458'     : '⢙',
'2458'     : '⢚',
'12458'    : '⢛',
'3458'     : '⢜',
'13458'    : '⢝',
'23458'    : '⢞',
'123458'   : '⢟',
'68'       : '⢠',
'168'      : '⢡',
'268'      : '⢢',
'1268'     : '⢣',
'368'      : '⢤',
'1368'     : '⢥',
'2368'     : '⢦',
'12368'    : '⢧',
'468'      : '⢨',
'1468'     : '⢩',
'2468'     : '⢪',
'12468'    : '⢫',
'3468'     : '⢬',
'13468'    : '⢭',
'23468'    : '⢮',
'123468'   : '⢯',
'568'      : '⢰',
'1568'     : '⢱',
'2568'     : '⢲',
'12568'    : '⢳',
'3568'     : '⢴',
'13568'    : '⢵',
'23568'    : '⢶',
'123568'   : '⢷',
'4568'     : '⢸',
'14568'    : '⢹',
'24568'    : '⢺',
'124568'   : '⢻',
'34568'    : '⢼',
'134568'   : '⢽',
'234568'   : '⢾',
'1234568'  : '⢿',
'78'       : '⣀',
'178'      : '⣁',
'278'      : '⣂',
'1278'     : '⣃',
'378'      : '⣄',
'1378'     : '⣅',
'2378'     : '⣆',
'12378'    : '⣇',
'478'      : '⣈',
'1478'     : '⣉',
'2478'     : '⣊',
'12478'    : '⣋',
'3478'     : '⣌',
'13478'    : '⣍',
'23478'    : '⣎',
'123478'   : '⣏',
'578'      : '⣐',
'1578'     : '⣑',
'2578'     : '⣒',
'12578'    : '⣓',
'3578'     : '⣔',
'13578'    : '⣕',
'23578'    : '⣖',
'123578'   : '⣗',
'4578'     : '⣘',
'14578'    : '⣙',
'24578'    : '⣚',
'124578'   : '⣛',
'34578'    : '⣜',
'134578'   : '⣝',
'234578'   : '⣞',
'1234578'  : '⣟',
'678'      : '⣠',
'1678'     : '⣡',
'2678'     : '⣢',
'12678'    : '⣣',
'3678'     : '⣤',
'13678'    : '⣥',
'23678'    : '⣦',
'123678'   : '⣧',
'4678'     : '⣨',
'14678'    : '⣩',
'24678'    : '⣪',
'124678'   : '⣫',
'34678'    : '⣬',
'134678'   : '⣭',
'234678'   : '⣮',
'1234678'  : '⣯',
'5678'     : '⣰',
'15678'    : '⣱',
'25678'    : '⣲',
'125678'   : '⣳',
'35678'    : '⣴',
'135678'   : '⣵',
'235678'   : '⣶',
'1235678'  : '⣷',
'45678'    : '⣸',
'145678'   : '⣹',
'245678'   : '⣺',
'1245678'  : '⣻',
'345678'   : '⣼',
'1345678'  : '⣽',
'2345678'  : '⣾',
'12345678' : '⣿'
}

def normalize(coord):
    coord_type = type(coord)

    if coord_type == int:
        return coord

    elif coord_type == float:
        return int(round(coord))




class Canvas(object):
    """docstring for Surface"""
    def __init__(self, line_ending='\n'):
        super(Canvas, self).__init__()
        self.clear()
        self.line_ending = line_ending

    def clear(self):
        self.pixels = defaultdict(dict)

    def set(self, x, y):
        x = normalize(x)
        y = normalize(y)
        self.pixels[y][x] = pixel_map[y % 4][x % 2]

    def unset(self, x, y):
        x = normalize(x)
        y = normalize(y)
        if y in self.pixels and x in self.pixels[y]:
            del(self.pixels[y][x])
            if not self.pixels[y]:
                del(self.pixels[y])

    def toggle(self, x, y):
        x = normalize(x)
        y = normalize(y)
        if y in self.pixels and x in self.pixels[y]:
            self.unset(x, y)
        else:
            self.set(x, y)

    def frame(self):
        minrow = min(self.pixels.keys())
        minrow -= minrow % 4
        maxrow = max(self.pixels.keys())
        mincol = min(min(x) for x in self.pixels.values())//2
        mincol -= mincol % 2
        maxcol = max(max(x) for x in self.pixels.values())//2
        maxcol += maxcol % 2
        ret = ''
        i = 0
        for rownum in range(minrow, maxrow+1):

            if not i % 4:
                buff = defaultdict(set)

            if rownum in self.pixels:
                for colnum in self.pixels[rownum]:
                    buff[colnum // 2].add(self.pixels[rownum][colnum])

            if i % 4 == 3:
                maxcol = max(max(buff.keys() or [0]), 4)
                ret += ''.join(braille_map[''.join(sorted(buff.get(x, [])))] for x in range(mincol, maxcol+1))
                if rownum != maxrow:
                    ret += self.line_ending

            i += 1

        if buff and i % 4:
            maxcol = max(max(buff.keys() or [0]), 4)
            ret += ''.join(braille_map[''.join(sorted(buff.get(x, [])))] for x in range(mincol, maxcol+1))

        return ret


def line(x1, y1, x2, y2):


    x1 = normalize(x1)
    y1 = normalize(y1)
    x2 = normalize(x2)
    y2 = normalize(y2)

    xdiff = max(x1, x2) - min(x1, x2)
    ydiff = max(y1, y2) - min(y1, y2)
    xdir = 1 if x1 <= x2 else -1
    ydir = 1 if y1 <= y2 else -1

    r = max(xdiff, ydiff)

    for i in range(r+1):
        x = x1
        y = y1
        if ydiff:
            y += (float(i)*ydiff)/r*ydir
        if xdiff:
            x += (float(i)*xdiff)/r*xdir
        yield (x, y)


def polygon(center_x=0, center_y=0, sides=4, radius=4):
    degree = float(360)/sides

    for n in range(sides):
        a = n*degree
        b = (n+1)*degree
        x1 = (center_x+math.cos(math.radians(a)))*(radius+1)/2
        y1 = (center_x+math.sin(math.radians(a)))*(radius+1)/2
        x2 = (center_x+math.cos(math.radians(b)))*(radius+1)/2
        y2 = (center_x+math.sin(math.radians(b)))*(radius+1)/2
        for x,y in line(x1,y1,x2,y2):
            yield x,y
