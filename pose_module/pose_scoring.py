import time

# ---------------- GLOBAL STATES ----------------
pose_start_time = None
hold_duration = 5

rep_count = 0
rep_stage = "down"

last_rep_time = 0
rep_delay = 0.8   # prevents double counting


# ---------------- POSE CONFIG ----------------
def get_pose_config(pose_name):
    pose_configs = {

        # -------- YOGA (HOLD BASED) --------
        "Mountain Pose": {
            "type": "yoga",
            "elbow": 180,
            "knee": 180,
            "tolerance": 10
        },
        "Chair Pose": {
            "type": "yoga",
            "elbow": 180,
            "knee": 100,
            "tolerance": 12
        },
        "Hands Up Pose": {
            "type": "yoga",
            "elbow": 180,
            "knee": 180,
            "tolerance": 10
        },

        # -------- EXERCISE (REP BASED) --------
        "Arm Raises": {
            "type": "exercise"
        },
        "Squats": {
            "type": "exercise"
        },
        "Arm Circles": {
            "type": "exercise"
        }
    }

    return pose_configs.get(pose_name, None)


# ---------------- YOGA SCORING ----------------
def yoga_score(elbow_angle, knee_angle, config):

    ideal_elbow = config["elbow"]
    ideal_knee = config["knee"]

    score = 100

    elbow_error = abs(elbow_angle - ideal_elbow)
    knee_error = abs(knee_angle - ideal_knee)

    score -= (elbow_error + knee_error) // 2
    score = max(0, min(100, int(score)))

    if score >= 80:
        feedback = "Good posture"
    else:
        feedback = "Adjust posture"

    return score, feedback


# ---------------- EXERCISE REP LOGIC ----------------
def exercise_reps(elbow_angle, knee_angle, pose_name):

    global rep_count, rep_stage, last_rep_time

    current_time = time.time()

    # -------- ARM RAISES --------
    if pose_name == "Arm Raises":

        if elbow_angle > 160:
            rep_stage = "down"

        if elbow_angle < 60 and rep_stage == "down":

            if current_time - last_rep_time > rep_delay:
                rep_stage = "up"
                rep_count += 1
                last_rep_time = current_time


    # -------- SQUATS --------
    elif pose_name == "Squats":

        if knee_angle > 160:
            rep_stage = "up"

        if knee_angle < 100 and rep_stage == "up":

            if current_time - last_rep_time > rep_delay:
                rep_stage = "down"
                rep_count += 1
                last_rep_time = current_time


    # -------- ARM CIRCLES --------
    elif pose_name == "Arm Circles":

        if elbow_angle > 150:
            rep_stage = "down"

        if elbow_angle < 80 and rep_stage == "down":

            if current_time - last_rep_time > rep_delay:
                rep_stage = "up"
                rep_count += 1
                last_rep_time = current_time


    feedback = f"Reps: {rep_count}"

    return rep_count, feedback


# ---------------- MAIN FUNCTION ----------------
def calculate_score(elbow_angle, knee_angle, pose_name):

    config = get_pose_config(pose_name)

    if config is None:
        return 0, "Pose not configured"

    if config["type"] == "yoga":
        return yoga_score(elbow_angle, knee_angle, config)

    else:
        return exercise_reps(elbow_angle, knee_angle, pose_name)