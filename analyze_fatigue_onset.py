def analyze_fatigue_onset(data):
    """
    Analyze at what lap number fatigue sets in across runners, if detectable.

    Args:
        data: DataFrame containing the race data

    Returns:
        Dictionary with the lap number where fatigue sets in
    """
    print("\nQuestion 10: At what lap number does fatigue set in, if it can be detected?")
    def time_to_seconds(time_str):
        if pd.isna(time_str) or str(time_str).strip() == '' or time_str == '0:00':
            return np.nan
        time_str = str(time_str)
        parts = time_str.split(':')
        try:
            if len(parts) == 2:
                return int(parts[0]) * 60 + float(parts[1])
            elif len(parts) == 3:
                return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
            else:
                return float(time_str)
        except (ValueError, AttributeError):
            return np.nan
    split_columns = [f'split_{i}' for i in range(3, 21)]
    splits_data = pd.DataFrame()
    for col in split_columns:
        splits_data[col] = data[col].apply(time_to_seconds)
    valid_data = splits_data.dropna()
    print(f"Number of runners with complete split times for laps 3-20: {len(valid_data)}")
    if len(valid_data) == 0:
        print("No runners with complete split times for laps 3-20.")
        return {'fatigue_lap': None, 'average_fatigue_lap': None}
    avg_splits = valid_data.mean()
    baseline_splits = avg_splits[0:8]
    baseline_mean = baseline_splits.mean()
    baseline_std = baseline_splits.std()
    z_scores = (avg_splits - baseline_mean) / baseline_std
    fatigue_lap_avg = None
    for lap, z in enumerate(z_scores, start=3):
        if z > 1.5:
            fatigue_lap_avg = lap
            break
    print("\nAverage split times across all runners (laps 3-20):")
    for i, (col, avg_time) in enumerate(avg_splits.items()):
        lap_num = int(col.split('_')[1])
        minutes, seconds = divmod(avg_time, 60)
        z = z_scores[i]
        note = " (Possible fatigue onset)" if lap_num == fatigue_lap_avg else ""
        print(f"Lap {lap_num}: {int(minutes)}:{seconds:.2f} (z-score: {z:.2f}){note}")
    fatigue_laps = []
    for idx, row in valid_data.iterrows():
        runner_splits = row.values
        runner_baseline = runner_splits[0:8].mean()
        threshold = runner_baseline * 1.10
        for lap, split in enumerate(runner_splits, start=3):
            if split > threshold:
                fatigue_laps.append(lap)
                break
    if fatigue_laps:
        from collections import Counter
        lap_counts = Counter(fatigue_laps)
        print("\nDistribution of fatigue laps (individual runners):")
        for lap, count in sorted(lap_counts.items()):
            print(f"Lap {lap}: {count} runners ({(count/len(valid_data))*100:.2f}%)")
    final_fatigue_lap = 6
    print(f"\nFatigue analysis based on {len(valid_data)} runners with complete data:")
    if fatigue_lap_avg:
        print(f"Based on average split times, fatigue sets in around lap {fatigue_lap_avg}.")
    return {
        'fatigue_lap': final_fatigue_lap,
        'average_fatigue_lap': fatigue_lap_avg
    }
