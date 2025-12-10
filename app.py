import gradio as gr

# --state & helpers--

def init_state():       # state dictionary to store variables across button clicks in Gradio. "memory" of the algorithm
    return{
        "array": [],
        "target": None,
        "low": None,
        "high": None,
        "mid": None,
        "step": 0,
        "found": False,
        "finished": False,
        "message": "",
    }

def parse_inputs(array_str, target_str):
    # convert array_str to list of ints
    parts = array_str.split(",")
    nums = []
    for p in parts:
        p = p.strip()
        if p == "":
            continue
        try:
            nums.append(int(p))
        except ValueError:
            raise gr.Error("Array must contain only integers!")
    
    if not nums:
        raise gr.Error("Enter at least one number.")
    
    nums = sorted(nums)

    # convert target_str to int
    try:
        target = int(target_str)
    except ValueError:
        raise gr.Error("Target must be a single integer!")

    return nums, target

def render_array(state):        # visual representation of array, including high and low, mid. displayed using markdown in UI
    if not state["array"]:
        return "Array will appear here once you start the program!"
    
    low = state["low"]
    high = state["high"]
    mid = state["mid"]

    pieces = []
    for i, val in enumerate(state["array"]):
        if mid is not None and i == mid:
            pieces.append(f"**[{val}]**")
        elif low is not None and high is not None and low <= i <= high:
            pieces.append(f"[{val}]")
        else:
            pieces.append(str(val))

    return " | ".join(pieces)

def render_status(state):       # multiline status describing current step, low/mid/high, short explanation
    if not state["array"]:
        return "Status will appear here."
    
    lines = [
        f"Step: {state['step']}",
        f"Target: {state['target']}",
        f"low: {state['low']}",
        f"high: {state['high']}",
    ]

    if state["mid"] is not None:
        mid = state["mid"]
        val = state["array"][mid]
        lines.append(f"mid: {mid} (value {val})")

    lines.append("")
    lines.append(state["message"])

    return "\n".join(lines)

# --callbacks--

def start_search(array_str, target_str, state):     # initialize search, parse user inputs, reset state vars, set low and high pointers. also prepares UI.
    nums, target = parse_inputs(array_str, target_str)

    state = init_state()
    state["array"] = nums
    state["target"] = target
    state["low"] = 0
    state["high"] = len(nums) - 1
    state["step"] = 0
    state["message"] = "Binary search initialized. Click Next Step."

    return render_array(state), render_status(state), state

def next_step(state):       # ONE STEp of binary search. check if search is finished, compute mid, compare mid with target, update low and high, set appropriate status message.runs with "next step" button.
    if not state["array"]:
        state["message"] = "Start the search first!"
        return render_array(state), render_status(state), state
    
    if state["finished"]:
        state["message"] = "Search is already complete, please reset and try again."
        return render_array(state), render_status(state), state
    
    low = state["low"]
    high = state["high"]
    target = state["target"]
    arr = state["array"]

    if low > high:
        state["finished"] = True
        state["message"] = "Target not found"
        return render_array(state), render_status(state), state
    
    mid = (low + high) // 2     # compute mid
    state["mid"] = mid
    state["step"] += 1

    if arr[mid] == target:
        state["found"] = True
        state["finished"] = True
        state["message"] = f"Found target {target} at index {mid}."
    elif arr[mid] < target:
        state["low"] = mid + 1
        state["message"] = f"{arr[mid]} < {target}, moving low upward!"
    else:
        state["high"] = mid - 1
        state["message"] = f"{arr[mid]} > {target}, moving high downward!"

    return render_array(state), render_status(state), state


# --UI--

with gr.Blocks(title="Binary Search Visualizer") as demo:

    gr.Markdown("# Binary Search Visualizer")

    with gr.Row():
        with gr.Column():
            array_in = gr.Textbox(label="Array")
            target_in = gr.Textbox(label="Target")
            start_btn = gr.Button("Start / Reset")
            next_btn = gr.Button("Next Step")

        with gr.Column():
            array_out = gr.Markdown()
            status_out = gr.Markdown()

    state = gr.State(init_state())

    start_btn.click(
        fn=start_search,
        inputs=[array_in, target_in, state],
        outputs=[array_out, status_out, state]
    )

    next_btn.click(
        fn=next_step,
        inputs=[state],
        outputs=[array_out, status_out, state]
    )

if __name__ == "__main__":
    print("about to launch Gradio...")
    demo.launch()
    print("Gradio has stopped.")
