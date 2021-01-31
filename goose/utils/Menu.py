import curses

class Menu:
  def __init__(self, menu_list):
    self.menu_list = menu_list
    self.selected_item = None
    self.custom_text = []

  def get_selected_item(self):
    return self.selected_item

  def place_custom_text(self, stdscr, h, w):
    for i, row in enumerate(self.custom_text):
      x = 2
      y = 2 - len(self.custom_text) // 2 + i
      stdscr.addstr(y, x, row)

  def draw_menu(self, stdscr, selected_row_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    self.place_custom_text(stdscr, h, w)

    for i, row in enumerate(self.menu_list):
      # x = w // 2 - len(row) // 2
      y = h // 2 - len(self.menu_list) // 2 + i

      if i == selected_row_idx:
        stdscr.attron(curses.color_pair(1))
        stdscr.addstr(y, 2, row)
        stdscr.attroff(curses.color_pair(1))
      else:
        stdscr.addstr(y, 2, row)

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
        # if current_row_idx == len(self.menu_list) - 1:
        #   break
        self.selected_item = current_row_idx
        # stdscr.addstr(0, 0, "You pressed {}".format(self.menu_list[current_row_idx]))
        # stdscr.refresh()
        # stdscr.getch()
        break


      self.draw_menu(stdscr, current_row_idx)
      stdscr.refresh()

  def print_with(self, custom_text=[]):
    self.custom_text = custom_text
    curses.wrapper(self.menu)
