def analyze_skipped_second_loop(data):
    """
    Analyze how many runners skipped the 2nd short loop.

    Args:
        data: DataFrame containing the race data

    Returns:
        Dictionary with statistics about skipped loops
    """
    print("\nQuestion 6: How many runners skipped the 2nd short loop?")
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
    split_columns = [f'split_{i}' for i in range(1, 21)]
    splits_seconds = {}
    for col in split_columns:
        splits_seconds[col] = data[col].apply(time_to_seconds)
    splits_df = pd.DataFrame(splits_seconds)
    median_split1 = splits_df['split_1'].median()
    regular_splits = splits_df.iloc[:, 2:19]
    median_regular_split = regular_splits.median().median()
    print(f"\nMedian time for first short loop (split_1): {median_split1:.2f} seconds")
    print(f"Median time for regular loops (splits 3-19): {median_regular_split:.2f} seconds")
    threshold = (median_split1 + median_regular_split) / 2
    skipped_second_loop = (splits_df['split_2'] > threshold).sum()
    missing_split2 = splits_df['split_2'].isna().sum()
    total_skipped_estimate = skipped_second_loop + missing_split2
    skipped_percentage = (total_skipped_estimate / len(data)) * 100
    print(f"\nBased on our analysis:")
    print(f"- Runners with missing split_2: {missing_split2}")
    print(f"- Runners with split_2 suggesting they ran a regular loop: {skipped_second_loop}")
    print(f"- Total estimate of runners who skipped the second short loop: {total_skipped_estimate}")
    print(f"- This represents {skipped_percentage:.2f}% of all runners.")
    later_short_loops = {}
    for i in range(3, 21):
        col = f'split_{i}'
        short_loops_count = (splits_df[col] < threshold).sum()
        if short_loops_count > 0:
            later_short_loops[col] = short_loops_count
    print("\nEstimate of runners who ran a short loop later in the race:")
    for split, count in later_short_loops.items():
        print(f"- {split}: {count} runners")
    return {
        'total_skipped_estimate': total_skipped_estimate,
        'skipped_percentage': skipped_percentage,
        'missing_split2': missing_split2,
        'skipped_second_loop': skipped_second_loop,
        'later_short_loops': later_short_loops
    }
