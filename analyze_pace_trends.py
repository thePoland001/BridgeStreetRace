def analyze_pace_trends(data):
    """
    Analyze whether runners tend to slow down or speed up as they progress through the race.

    Args:
        data: DataFrame containing the race data

    Returns:
        Dictionary with analysis results
    """
    print("\nQuestion 7: On average, do the runners slow down or speed up as they run further?")
    def time_to_seconds(time_str):
        if pd.isna(time_str) or str(time_str).strip() == '':
            return None
        time_str = str(time_str)
        if time_str.lower() in ['time', 'half_maraton_time', 'fixed_half_marathon_time']:
            return None
        parts = time_str.split(':')
        try:
            if len(parts) == 2:
                return int(parts[0]) * 60 + float(parts[1])
            elif len(parts) == 3:
                return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
            else:
                return float(time_str)
        except ValueError:
            return None
    split_columns = [f'split_{i}' for i in range(3, 21)]
    splits_seconds = {}
    for col in split_columns:
        splits_seconds[col] = data[col].apply(time_to_seconds)
    splits_df = pd.DataFrame(splits_seconds)
    avg_splits = splits_df.mean()
    print("\nAverage split times across all runners:")
    for i, (col, avg_time) in enumerate(avg_splits.items()):
        lap_num = int(col.split('_')[1])
        minutes, seconds = divmod(avg_time, 60)
        print(f"Lap {lap_num}: {int(minutes)}:{seconds:.2f}")
    x = np.array(range(3, 21))
    y = avg_splits.values
    slope, intercept = np.polyfit(x, y, 1)
    if slope > 0:
        trend = "slow down"
    else:
        trend = "speed up"
    first_lap_avg = avg_splits.iloc[0]
    last_lap_avg = avg_splits.iloc[-1]
    percent_change = ((last_lap_avg - first_lap_avg) / first_lap_avg) * 100
    print(f"\nLinear regression results:")
    print(f"Slope: {slope:.2f} seconds per lap")
    print(f"\nOverall trend: Runners tend to {trend} as they progress through the race.")
    print(f"Average pace change from lap 3 to lap 20: {percent_change:.2f}%")
    runner_slopes = []
    for idx, row in splits_df.iterrows():
        valid_splits = row.dropna()
        if len(valid_splits) >= 10:
            lap_nums = [int(col.split('_')[1]) for col in valid_splits.index]
            lap_times = valid_splits.values
            try:
                runner_slope, _ = np.polyfit(lap_nums, lap_times, 1)
                runner_slopes.append(runner_slope)
            except:
                continue
    slowing_down = sum(1 for slope in runner_slopes if slope > 0)
    speeding_up = sum(1 for slope in runner_slopes if slope < 0)
    print(f"\nIndividual runner analysis (based on {len(runner_slopes)} runners with sufficient data):")
    print(f"Runners who slow down: {slowing_down} ({slowing_down/len(runner_slopes)*100:.2f}%)")
    print(f"Runners who speed up: {speeding_up} ({speeding_up/len(runner_slopes)*100:.2f}%)")
    if 'time_seconds' not in data.columns:
        if 'fixed_half_marathon_time' in data.columns:
            time_column = 'fixed_half_marathon_time'
        else:
            time_column = 'half_maraton_time'
        data['time_seconds'] = data[time_column].apply(time_to_seconds)
    data_with_slopes = data.copy()
    all_slopes = [np.nan] * len(data)
    valid_runners = 0
    for idx, row in splits_df.iterrows():
        if valid_runners < len(runner_slopes):
            all_slopes[idx] = runner_slopes[valid_runners]
            valid_runners += 1
    data_with_slopes['pace_slope'] = all_slopes
    valid_data = data_with_slopes.dropna(subset=['pace_slope', 'time_seconds'])
    median_time = valid_data['time_seconds'].median()
    fast_runners = valid_data[valid_data['time_seconds'] < median_time]
    slow_runners = valid_data[valid_data['time_seconds'] >= median_time]
    fast_avg_slope = fast_runners['pace_slope'].mean()
    slow_avg_slope = slow_runners['pace_slope'].mean()
    print(f"\nPace trends by runner speed:")
    print(f"Fastest half of runners: Average slope = {fast_avg_slope:.2f} seconds per lap")
    print(f"Slowest half of runners: Average slope = {slow_avg_slope:.2f} seconds per lap")
    return {
        'overall_slope': slope,
        'percent_change': percent_change,
        'overall_trend': trend,
        'slowing_down_count': slowing_down,
        'speeding_up_count': speeding_up,
        'fast_runners_slope': fast_avg_slope,
        'slow_runners_slope': slow_avg_slope
    }
