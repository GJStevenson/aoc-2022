"""
--- Day 12: Hill Climbing Algorithm ---

You try contacting the Elves using your handheld device, but the river you're following must be too low to get a decent signal.

You ask the device for a heightmap of the surrounding area (your puzzle input). The heightmap shows the local area from above broken into a grid; the elevation of each square of the grid is given by a single lowercase letter, where a is the lowest elevation, b is the next-lowest, and so on up to the highest elevation, z.

Also included on the heightmap are marks for your current position (S) and the location that should get the best signal (E). Your current position (S) has elevation a, and the location that should get the best signal (E) has elevation z.

You'd like to reach E, but to save energy, you should do it in as few steps as possible. During each step, you can move exactly one square up, down, left, or right. To avoid needing to get out your climbing gear, the elevation of the destination square can be at most one higher than the elevation of your current square; that is, if your current elevation is m, you could step to elevation n, but not to elevation o. (This also means that the elevation of the destination square can be much lower than the elevation of your current square.)

For example:

Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
Here, you start in the top-left corner; your goal is near the middle. You could start by moving down or right, but eventually you'll need to head toward the e at the bottom. From there, you can spiral around to the goal:

v..v<<<<
>v.vv<<^
.>vv>E^^
..v>>>^^
..>>>>>^
In the above diagram, the symbols indicate whether the path exits each square moving up (^), down (v), left (<), or right (>). The location that should get the best signal is still E, and . marks unvisited squares.

This path reaches the goal in 31 steps, the fewest possible.

What is the fewest steps required to move from your current position to the location that should get the best signal?

--- Part Two ---

As you walk up the hill, you suspect that the Elves will want to turn this into a hiking trail. The beginning isn't very scenic, though; perhaps you can find a better starting point.

To maximize exercise while hiking, the trail should start as low as possible: elevation a. The goal is still the square marked E. However, the trail should still be direct, taking the fewest steps to reach its goal. So, you'll need to find the shortest path from any square at elevation a to the square marked E.

Again consider the example from above:

Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
Now, there are six choices for starting position (five marked a, plus the square marked S that counts as being at elevation a). If you start at the bottom-left square, you can reach the goal most quickly:

...v<<<<
...vv<<^
...v>E^^
.>v>>>^^
>^>>>>>^
This path reaches the goal in only 29 steps, the fewest possible.

What is the fewest steps required to move starting from any square with elevation a to the location that should get the best signal?

"""


import collections
import math


def main():
   height_map = read_input()

   start, end, adjacency_list = process_height_map(height_map)

   print('Part 1: ', find_shortest_path(start, end, adjacency_list))

   starting_positions = [(row, col) for row, line in enumerate(height_map) for col, char in enumerate(line) if char == 'a' or char == 'S']
   print('Part 2: ', min([find_shortest_path(pos, end, adjacency_list) for pos in starting_positions]))
   

def find_shortest_path(start, end, adjacency_list):
   shortest_path_seen = {start: 0}
   queue = collections.deque(((start, 0),))

   while queue:
      current_position, steps = queue.popleft()
      next_steps = steps + 1
      for neighbor in adjacency_list[current_position]:
         if neighbor not in shortest_path_seen or next_steps < shortest_path_seen[neighbor]:
            shortest_path_seen[neighbor] = next_steps
            if neighbor != end:
               queue.append((neighbor, next_steps))


   return shortest_path_seen[end] if end in shortest_path_seen else math.inf


def process_height_map(height_map):
   adjacency_list = collections.defaultdict(list)
   ROWS, COLS = len(height_map), len(height_map[0])

   for row, line in enumerate(height_map):
      for col, char in enumerate(line):
         point = (row, col)
         if char == 'S':
            start = point
            char = 'a'
         elif char == 'E':
            end = point
            char = 'z'

         neighbors = (
            (row + 1, col),
            (row - 1, col),
            (row, col + 1),
            (row, col - 1),
         )

         for nrow, ncol in neighbors:
            if nrow < 0 or nrow >= ROWS or ncol < 0 or ncol >= COLS:
               continue

            nchar = height_map[nrow][ncol]
            if nchar == 'S':
               nchar = 'a'
            elif nchar == 'E':
               nchar = 'z'

            if ord(nchar) - ord(char) <= 1:
               adjacency_list[point].append((nrow, ncol))
   
   return start, end, adjacency_list


def read_input():
   with open('day_12/input.txt') as f:
      return [[l for l in line.strip()] for line in f.readlines()]


if __name__ == '__main__':
   main()