def fix_half_marathon_times(data):
    """
    Fix the half marathon times by adding the hour component based on the runner's place.

    Rules:
    - Places 1-156: Add 1 hour (prefix with "1:")
    - Places 157-443: Add 2 hours (prefix with "2:")
    - Places 444-488: Add 3 hours (prefix with "3:")
    - Places 489-493: Add 4 hours (prefix with "4:")

    Args:
        data: DataFrame containing the race data

    Returns:
        DataFrame with fixed times
    """
    print("\nQuestion 2: Fix half marathon time format")
    data['original_half_marathon_time'] = data['half_maraton_time'].copy()
    def add_appropriate_hour(row):
        time_str = row['half_maraton_time']
        place = row['place']
        if pd.isna(time_str) or str(time_str).strip() == '':
            return time_str
        time_str = str(time_str)
        if ":" in time_str and time_str.count(":") > 1:
            return time_str
        if place < 157:
            return f"1:{time_str}"
        elif place < 444:
            return f"2:{time_str}"
        elif place < 489:
            return f"3:{time_str}"
        else:
            return f"4:{time_str}"
    data['fixed_half_marathon_time'] = data.apply(add_appropriate_hour, axis=1)
    print("\nExample corrections:")
    place_ranges = [(1, 156), (157, 443), (444, 488), (489, 493)]
    for start, end in place_ranges:
        range_data = data[(data['place'] >= start) & (data['place'] <= end)]
        if len(range_data) > 0:
            sample = range_data.iloc[0]
            print(f"Place {start}-{end}: Runner #{sample['place']}: {sample['original_half_marathon_time']} → {sample['fixed_half_marathon_time']}")
    changed_count = (data['fixed_half_marathon_time'] != data['original_half_marathon_time']).sum()
    unchanged_count = len(data) - changed_count
    print(f"\nSummary of changes:")
    print(f"Total times fixed: {changed_count} ({changed_count/len(data)*100:.2f}%)")
    print(f"Times unchanged: {unchanged_count} ({unchanged_count/len(data)*100:.2f}%)")
    for start, end in place_ranges:
        range_data = data[(data['place'] >= start) & (data['place'] <= end)]
        range_changed = (range_data['fixed_half_marathon_time'] != range_data['original_half_marathon_time']).sum()
        print(f"  Places {start}-{end}: {range_changed}/{len(range_data)} times fixed")
    return data
