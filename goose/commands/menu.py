import curses
import time

menu_items = ["Desktop", "Documents", "Public", "Music", "Exit"]

def print_menu(stdscr, selected_row_idx):
  stdscr.clear()
  h, w = stdscr.getmaxyx()

  for i, row in enumerate(menu_items):
    x = w // 2 - len(row) // 2
    y = h // 2 - len(menu_items) // 2 + i

    if i == selected_row_idx:
      stdscr.attron(curses.color_pair(1))
      stdscr.addstr(y, x, row)
      stdscr.attroff(curses.color_pair(1))
    else:
      stdscr.addstr(y, x, row)

  stdscr.refresh()

def _menu(stdscr):
  curses.curs_set(0)
  curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
  current_row_idx = 0

  print_menu(stdscr, current_row_idx)

  while 1:
    key = stdscr.getch()
    stdscr.clear()

    if key == curses.KEY_UP and current_row_idx > 0:
      current_row_idx -= 1
    elif key == curses.KEY_DOWN and current_row_idx < len(menu_items) - 1:
      current_row_idx += 1
    elif key == curses.KEY_ENTER or key in [10, 13]:
      if current_row_idx == len(menu_items) - 1:
        break
      stdscr.addstr(0, 0, "You pressed {}".format(menu_items[current_row_idx]))
      stdscr.refresh()
      stdscr.getch()

    print_menu(stdscr, current_row_idx)
    stdscr.refresh()

def menu():
  curses.wrapper(_menu)
