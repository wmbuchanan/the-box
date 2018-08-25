import sys
import re
import time
import subprocess

BOX_IS_ON = False

# Actions
TURN_BOX_ON = '--turn-box-on'
TURN_BOX_OFF = '--turn-box-off'
LET_BOX_JUST_SIT_THERE_DOING_WHAT_IT_IS_DOING = '--do-nothing'

def turn_box_on():
    if not BOX_IS_ON:
        flip_switch(box_is_being_turned_on=True)

def turn_box_off():
    if BOX_IS_ON:
        wait(5)
        flip_switch(box_is_being_turned_on=False)

def wait(seconds):
    for _ in range(seconds - 1):
        time.sleep(1)
        # sys.stdout.write instead of print for Python version compatibility
        sys.stdout.write('. ')
        sys.stdout.flush()
    time.sleep(1)
    sys.stdout.write('\n')

def flip_switch(box_is_being_turned_on):
    with open(__file__, 'r+') as box:
        contents = box.read()
        flipped_state = re.sub(r'(?<=BOX_IS_ON = )\w+', str(box_is_being_turned_on), contents)
        toggle(box, flipped_state)

    message = 'The box is {}'.format('on' if box_is_being_turned_on else 'off')
    print(message)

    next_action = TURN_BOX_OFF if box_is_being_turned_on else LET_BOX_JUST_SIT_THERE_DOING_WHAT_IT_IS_DOING
    act(next_action)

def toggle(switchable, new_state):
    switchable.seek(0)
    switchable.write(new_state)
    switchable.truncate()

def act(action):
    subprocess.call([sys.executable, __file__, action])

if __name__ == '__main__':
    args = sys.argv

    if len(args) > 1:
        if args[1] == TURN_BOX_ON:
            turn_box_on()
        elif args[1] == TURN_BOX_OFF:
            turn_box_off()

    if BOX_IS_ON:
        act(LET_BOX_JUST_SIT_THERE_DOING_WHAT_IT_IS_DOING)
