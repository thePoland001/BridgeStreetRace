def analyze_dr_c_chen_dizzy(data):
    """
    Determine when Dr. C. Chen (place 268) got dizzy during the race.

    Args:
        data: DataFrame containing the race data

    Returns:
        The lap number where Dr. C. Chen likely got dizzy
    """
    print("\nQuestion 4: When did Dr. C. Chen get dizzy during the race?")
    dr_c_chen = data[data['place'] == 268]
    if len(dr_c_chen) == 0:
        print("Error: Dr. C. Chen (place 268) not found in the dataset")
        return None
    print(f"Found Dr. C. Chen at place {dr_c_chen['place'].iloc[0]}")
    split_columns = [f'split_{i}' for i in range(1, 21)]
    split_times = dr_c_chen[split_columns].iloc[0].tolist()
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
    def seconds_to_time(seconds):
        if seconds is None:
            return "N/A"
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        if hours > 0:
            return f"{int(hours)}:{int(minutes):02d}:{int(seconds):02d}"
        else:
            return f"{int(minutes)}:{int(seconds):02d}"
    regular_splits = [t for i, t in enumerate(split_times_seconds) if i >= 2 and t is not None]
    mean_time = sum(regular_splits) / len(regular_splits)
    variance = sum((t - mean_time) ** 2 for t in regular_splits) / len(regular_splits)
    std_dev = variance ** 0.5
    z_scores = []
    for i, t in enumerate(split_times_seconds):
        if t is None:
            z_scores.append(None)
        elif i < 2:
            z_scores.append(None)
        else:
            z_score = (t - mean_time) / std_dev
            z_scores.append(z_score)
    print(f"\nDr. C. Chen's average split time (excluding first two short laps): {seconds_to_time(mean_time)}")
    print(f"Standard deviation: {seconds_to_time(std_dev)}")
    print("\nLap-by-lap analysis:")
    print(f"{'Lap':<5}{'Split Time':<12}{'Z-Score':<10}{'Notes'}")
    print("-" * 60)
    for i, (time_sec, z_score) in enumerate(zip(split_times_seconds, z_scores)):
        notes = ""
        if i < 2:
            notes = "Short lap (0.31 miles)"
        elif z_score is not None:
            if z_score > 2:
                notes = "Much slower than average (potential dizzy spell)"
            elif z_score < -2:
                notes = "Much faster than average"
        z_score_str = f"{z_score:.2f}" if z_score is not None else "N/A"
        print(f"{i+1:<5}{seconds_to_time(time_sec):<12}{z_score_str:<10}{notes}")
    valid_z_scores = [(i+1, z) for i, z in enumerate(z_scores) if z is not None]
    if not valid_z_scores:
        print("\nCould not determine when Dr. C. Chen got dizzy due to insufficient data.")
        return None
    dizzy_lap, max_z = max(valid_z_scores, key=lambda x: x[1])
    print(f"\nDr. C. Chen likely got dizzy around lap {dizzy_lap}")
    print(f"This lap had a time of {seconds_to_time(split_times_seconds[dizzy_lap-1])}")
    print(f"Z-score: {max_z:.2f} (standard deviations above mean)")
    if dizzy_lap < 20:
        next_laps = [(i+1, z) for i, z in enumerate(z_scores) if i+1 > dizzy_lap and z is not None]
        if next_laps:
            recovery_trend = [z for _, z in next_laps]
            if min(recovery_trend) < max_z:
                print(f"\nDr. C. Chen appears to have started recovering after lap {dizzy_lap}")
                print("This aligns with the problem statement that he got some sugar and recovered.")
    return dizzy_lap
