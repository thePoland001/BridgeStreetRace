def analyze_dr_h_chen_pacer(data):
    """
    Analyze when Dr. H. Chen was dropped by the 3-hour pacer by comparing pace per mile, excluding laps 2 and 20.

    Args:
        data: DataFrame containing the race data

    Returns:
        The lap number where Dr. H. Chen was dropped by the pacer
    """
    print("\nQuestion 3: When did Dr. H. Chen get dropped by the 3-hour pacer?")
    dr_chen = data[data['place'] == 456]
    split_columns = [f'split_{i}' for i in range(1, 21)]
    split_times = dr_chen[split_columns].iloc[0].tolist()
    def time_to_seconds(time_str):
        if pd.isna(time_str) or str(time_str).strip() == '':
            return None
        time_str = str(time_str)
        parts = time_str.split(':')
        if len(parts) == 2:
            return int(parts[0]) * 60 + float(parts[1])
        elif len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
        else:
            try:
                return float(time_str)
            except:
                return None
    split_times_seconds = [time_to_seconds(t) for t in split_times]
    distances = [0.31] * 2 + [0.7159] * 17 + [0.31]
    cumulative_distances = []
    total_distance = 0
    for d in distances:
        total_distance += d
        cumulative_distances.append(total_distance)
    paces_per_mile = []
    for i, (time, distance) in enumerate(zip(split_times_seconds, distances)):
        if time is None:
            paces_per_mile.append(None)
        else:
            pace = time / distance
            paces_per_mile.append(pace)
    pacer_pace_per_mile = (3 * 60 * 60) / 13.1
    def seconds_to_time(seconds):
        if seconds is None:
            return "N/A"
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        if hours > 0:
            return f"{int(hours)}:{int(minutes):02d}:{int(seconds):02d}"
        else:
            return f"{int(minutes)}:{int(seconds):02d}"
    drop_threshold = 60
    drop_lap = None
    print("\nPace Analysis for Dr. H. Chen (Pace in seconds per mile):")
    print(f"{'Lap':<5}{'Distance':<10}{'Split':<10}{'Pace':<15}{'Pacer Pace':<15}{'Difference':<15}{'Status'}")
    print("-" * 75)
    for i in range(len(split_times_seconds)):
        if paces_per_mile[i] is None:
            continue
        pace_diff = paces_per_mile[i] - pacer_pace_per_mile
        status = "On pace"
        if i in [1, 19]:  # Exclude laps 2 and 20 (indices 1 and 19)
            status = "Excluded (short lap)"
        elif pace_diff > drop_threshold:
            status = "Dropped"
            if drop_lap is None:
                drop_lap = i + 1
        print(f"{i+1:<5}{distances[i]:<10.4f}{seconds_to_time(split_times_seconds[i]):<10}"
              f"{seconds_to_time(paces_per_mile[i]):<15}"
              f"{seconds_to_time(pacer_pace_per_mile):<15}"
              f"{seconds_to_time(pace_diff):<15}{status}")
    if drop_lap:
        print(f"\nDr. H. Chen was dropped by the 3-hour pacer at lap {drop_lap}")
        print(f"Dr. Chen's pace at lap {drop_lap}: {seconds_to_time(paces_per_mile[drop_lap-1])} per mile")
        print(f"Pacer's pace: {seconds_to_time(pacer_pace_per_mile)} per mile")
        print(f"Pace difference: {seconds_to_time(paces_per_mile[drop_lap-1] - pacer_pace_per_mile)} per mile")
    return drop_lap
