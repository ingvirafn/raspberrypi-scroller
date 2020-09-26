#!/usr/bin/env python

import scrollphathd

import threading
import logging



PREFIX_OFFSET = 1
SCROLL_PAGE_SIZE = 3
ROTATED = 180
ALL_UPPERCASE = False
INITIAL_DELAY = 3.0
POST_DELAY = 1.0

class AutoScroll():
    _is_enabled = False
    _interval = 0.05
    _items = []
    _current = None
    _currentIndexCountdown = 0
    _overflow_length = 0

    def AutoScroll(self, interval=0.05):
        self._interval = interval

    def startstop(self):
        if self._is_enabled is False:
            logging.info("Starting Autoscroll")
            self._is_enabled = True
            # if ROTATED != 0:
            logging.info("Autoscroll rotated {}".format(ROTATED))
            scrollphathd.rotate(degrees=ROTATED)
            self.run()
        else:
            self._is_enabled = False

    def append(self, msg):
        logging.info("Autoscroll append")
        self._items.insert(0, msg + (" " * 3))
    
    def clear(self):
        self._items.clear()

    def run(self):
        if self._is_enabled is False:
            return
        
        next_interval = self._interval

        if self._currentIndexCountdown < 0:

            if len(self._items) > 0:
                upcoming = self._items.pop()
                if ALL_UPPERCASE:
                    upcoming = upcoming.upper()

                scrollphathd.clear()
                scrollphathd.write_string(upcoming, x=PREFIX_OFFSET, y=0, font=None, letter_spacing=1, brightness=0.2, monospaced=False, fill_background=False)
                scrollphathd.show()

                shape = scrollphathd.get_shape()
                buffer_shape = scrollphathd.get_buffer_shape()
                self._overflow_length = buffer_shape[0] - shape[0]
                logging.info("Autoscroll.run: Decreasing index countdown: {} ({} - {})".format(str(self._overflow_length), shape[0], buffer_shape[0]))
                self._currentIndexCountdown = self._overflow_length

                next_interval = INITIAL_DELAY  # inital delay
            else:
                logging.info("Autoscroll.run: No items to pop..")
                # self.demo()
                
        else:
            logging.info("Autoscroll.run: Just scrolling..")

            # Scroll the buffer content
            scrollphathd.scroll(x=SCROLL_PAGE_SIZE)
            # Show the buffer
            scrollphathd.show()

            self._currentIndexCountdown -= SCROLL_PAGE_SIZE

        # Start a timer
        threading.Timer(next_interval, self.run).start()


def main():
    logging.basicConfig(level=logging.INFO)

    scrollphathd.set_clear_on_exit(True)
    autoscroll = AutoScroll()
    autoscroll.startstop()

if __name__ == '__main__':
    main()

