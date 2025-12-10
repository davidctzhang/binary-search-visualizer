# Algorithm Name: BINARY SEARCH VISUALIZER!!
# goal: visualize each step of a binary search, giving users a look into the "thinking" process of the algorithm

## Demo video/gif/screenshot of test: included in #binary-search-pngs folder

## Problem Breakdown & Computational Thinking (You can add a flowchart and write the four pillars of computational thinking briefly in bullets):
# flowchart:
1. user enters array of integers, separated by commas, as well as a target integer
2. user clicks "start/reset" button
    - inputs are parsed and validated
    - array is sorted
    - state is initialized for low/high/mid/step
3. user repeatedly clicks "next step" button
    - 1 binary search at a time
    - state is updated each time
    - UI rerenders array view and status
4. search ends when:
- mid == target -> found
- or low > high -> not found

# Decomposition 
- input handling uses parse_inputs(array_str, target_str) to clean strings, convert to integers, sort the array and validate the target.
- init_state() creates a dictionary with the array, target, low/high/mid, step, finished, found, and message states
    - wrapped in gr.State so it persists between button clicks (not calling function scratch every time)
- render_array(state) builds markdown string with values in current search window and the current mid element
    - render_status(state) explains the current step
- start_search() intializes everything when the "start/reset" button is pressed
- next_step(state) performs ONE binary search iteration per click

# Pattern Recognition
- binary search always follows a pattern:
    1. work on sorted array
    2. maintain window of low/high
    3. repeatedly compute mid (low + high) // 2
    4. discard empty search space (half)
- can use while loop, probably better if implemented in anything else, but i wanted each step to be one button press.

# Abstraction
- hide the highlighted array/current indices and instead print a readable explanation of pointers
- user does not see gr.State, or the state dictionary, or parsing and error handling
- separate parsing and UI functions allow start_search and next_step to be focused on algorithm logic, which made it a lot easier to display each step to the user.

# Algorithm Design
- inputs: 
    - textbox(array as comma separated integers)
    - textbox(target integer)
- buttons: Start/Reset and Next Step
- states track everything (array,target,low/high/mid,step,found,finished,message).
- rules:
    - if low > high, target is not in array -> stop
    - mid = (low + high) // 2
    - if mid == target -> found, stop
    - if mid < target, move low up to mid + 1
    - if mid > target, move high down to mid - 1
- outputs: 
    - updated array view with search window and highlighted mid
    - updated status message for each step
- O(logn) in the worst case, spread across multiple button presses instead of 1 loop

## Steps to Run:
# Local: 
# pip install -r requirements.txt
# python app.py

## Hugging Face Link
https://huggingface.co/spaces/davidctzhang/binary-search-visualizer

## Author & Acknowledgment
all code written by myself, AI level 4 used to help me add appropriate comments for readability. also to help me understand huggingface (not relevant in github). AI was also used in debugging step, where it caught an indentation error on line 18. 