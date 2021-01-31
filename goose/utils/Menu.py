import curses

class Menu:
  def __init__(self, menu_list):
    self.menu_list = menu_list

  def draw_menu(self, stdscr, selected_row_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    for i, row in enumerate(self.menu_list):
      x = w // 2 - len(row) // 2
      y = h // 2 - len(self.menu_list) // 2 + i

      if i == selected_row_idx:
        stdscr.attron(curses.color_pair(1))
        stdscr.addstr(y, x, row)
        stdscr.attroff(curses.color_pair(1))
      else:
        stdscr.addstr(y, x, row)

    stdscr.refresh()

  def menu(self, stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    current_row_idx = 0

    self.draw_menu(stdscr, current_row_idx)

    while 1:
      key = stdscr.getch()
      stdscr.clear()

      if key == curses.KEY_UP and current_row_idx > 0:
        current_row_idx -= 1
      elif key == curses.KEY_DOWN and current_row_idx < len(self.menu_list) - 1:
        current_row_idx += 1
      elif key == curses.KEY_ENTER or key in [10, 13]:
        if current_row_idx == len(self.menu_list) - 1:
          break
        stdscr.addstr(0, 0, "You pressed {}".format(self.menu_list[current_row_idx]))
        stdscr.refresh()
        stdscr.getch()

      self.draw_menu(stdscr, current_row_idx)
      stdscr.refresh()

  def print(self):
    curses.wrapper(self.menu)
