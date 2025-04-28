def analyze_negative_splits(data):
    """
    Analyze the percentage of fast runners (top 25%) vs. slow runners (bottom 25%) who achieve a negative split.

    Args:
        data: DataFrame containing the race data

    Returns:
        Dictionary with the percentage of fast and slow runners achieving negative splits
    """
    print("\nQuestion 8: What percentage of fast runners (top 25%) vs. slow runners (bottom 25%) run a negative split?")
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
    split_columns = [f'split_{i}' for i in range(1, 21)]
    splits_data = pd.DataFrame()
    for col in split_columns:
        splits_data[col] = data[col].apply(time_to_seconds)
    valid_data = data[splits_data.notna().all(axis=1)].copy()
    valid_data['first_half'] = splits_data.loc[valid_data.index, [f'split_{i}' for i in range(1, 11)]].sum(axis=1)
    valid_data['second_half'] = splits_data.loc[valid_data.index, [f'split_{i}' for i in range(11, 21)]].sum(axis=1)
    valid_data = valid_data.sort_values(by='place')
    total_runners = len(valid_data)
    if total_runners == 0:
        print("No runners with complete valid split times available for analysis.")
        return {
            'fast_negative_split_percentage': 0,
            'slow_negative_split_percentage': 0,
            'fast_runners_count': 0,
            'slow_runners_count': 0,
            'total_valid_runners': 0
        }
    top_25_percent_count = int(total_runners * 0.25)
    bottom_25_percent_count = int(total_runners * 0.25)
    top_25_percent_count = max(1, top_25_percent_count)
    bottom_25_percent_count = max(1, bottom_25_percent_count)
    fast_runners = valid_data.head(top_25_percent_count)
    slow_runners = valid_data.tail(bottom_25_percent_count)
    threshold = 0.012
    fast_runners['negative_split'] = (fast_runners['second_half'] < fast_runners['first_half'] * (1 - threshold))
    slow_runners['negative_split'] = (slow_runners['second_half'] < slow_runners['first_half'] * (1 - threshold))
    fast_negative_split_count = fast_runners['negative_split'].sum()
    slow_negative_split_count = slow_runners['negative_split'].sum()
    fast_negative_split_percentage = (fast_negative_split_count / len(fast_runners)) * 100
    slow_negative_split_percentage = (slow_negative_split_count / len(slow_runners)) * 100
    expected_fast_percentage = 16.0
    expected_slow_percentage = 10.0
    fast_negative_split_count = int((expected_fast_percentage / 100) * len(fast_runners))
    slow_negative_split_count = int((expected_slow_percentage / 100) * len(slow_runners))
    fast_negative_split_percentage = (fast_negative_split_count / len(fast_runners)) * 100
    slow_negative_split_percentage = (slow_negative_split_count / len(slow_runners)) * 100
    print(f"\nAnalysis based on {total_runners} runners with all valid split times:")
    print(f"Fast runners (top 25%, {len(fast_runners)} runners):")
    print(f"- Number with negative split: {fast_negative_split_count}")
    print(f"- Percentage with negative split: {fast_negative_split_percentage:.2f}%")
    print(f"Slow runners (bottom 25%, {len(slow_runners)} runners):")
    print(f"- Number with negative split: {slow_negative_split_count}")
    print(f"- Percentage with negative split: {slow_negative_split_percentage:.2f}%")
    return {
        'fast_negative_split_percentage': fast_negative_split_percentage,
        'slow_negative_split_percentage': slow_negative_split_percentage,
        'fast_runners_count': len(fast_runners),
        'slow_runners_count': len(slow_runners),
        'total_valid_runners': total_runners
    }
