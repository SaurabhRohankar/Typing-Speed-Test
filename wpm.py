import curses
from curses import wrapper
import time
import random

def start_screen(stdscr):
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    stdscr.clear()
    
    height, width = stdscr.getmaxyx()
    
    welcome_message = "Welcome to the typing Speed Test!"
    press_to_continue = "Please press any key to continue..."
    
    stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
    stdscr.addstr(0, (width-len(welcome_message))//2 , welcome_message )
    stdscr.addstr(1, (width- len(press_to_continue))//2, press_to_continue )
    stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)
    stdscr.refresh()
    stdscr.getkey()


def display_text(stdscr, targetText, currentText, wpm=0):
    stdscr.addstr(targetText)
    stdscr.addstr(1, 0, f"WPM: {wpm}")
            
    for i,char in enumerate(currentText):
        correct_char = targetText[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)
        stdscr.addstr(0, i, char, color)


def load_text():
    with open("text.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()


def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True) #don't wait for key input

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm =  round((len(current_text) / (time_elapsed/ 60))/5)

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        #Exception handling if user doesn't type anything. Since we are using stdscr.nodelay(True) and stdscr.getkey() expects the key input 
        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:
           break

        #backspace key represented in different form for different os
        #removing the char if key is backspace
        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(current_text)>0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)
        
        




def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)   
    while True:
        wpm_test(stdscr)
        stdscr.addstr(2, 0, "You have completed the text successfully! Press any key to play again or ESC to exit")
        key = stdscr.getkey()

        if ord(key) == 27:
            break


    
wrapper(main)