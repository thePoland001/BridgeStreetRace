def analyze_age_finishing_time_correlation(data):
    """
    Analyze whether there is a correlation between age and finishing time.

    Args:
        data: DataFrame containing the race data with fixed marathon times

    Returns:
        The correlation coefficient and other statistics
    """
    print("\nQuestion 5: Is there a correlation between age and finishing time?")
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
            print(f"Warning: Could not convert '{time_str}' to seconds")
            return None
    if 'fixed_half_marathon_time' in data.columns:
        time_column = 'fixed_half_marathon_time'
    else:
        time_column = 'half_maraton_time'
    data['time_seconds'] = data[time_column].apply(time_to_seconds)
    complete_data = data.dropna(subset=['age', 'time_seconds'])
    print(f"Analysis based on {len(complete_data)} runners with valid age and time data")
    correlation = complete_data['age'].corr(complete_data['time_seconds'])
    print(f"Correlation coefficient: {correlation:.4f}")
    if abs(correlation) < 0.1:
        interpretation = "very weak or no correlation"
    elif abs(correlation) < 0.3:
        interpretation = "weak correlation"
    elif abs(correlation) < 0.5:
        interpretation = "moderate correlation"
    elif abs(correlation) < 0.7:
        interpretation = "strong correlation"
    else:
        interpretation = "very strong correlation"
    direction = "positive" if correlation > 0 else "negative"
    relationship = "older runners tend to have longer finishing times" if correlation > 0 else "older runners tend to have shorter finishing times"
    print(f"This indicates a {interpretation} in the {direction} direction")
    print(f"Meaning that {relationship}")
    bins = [0, 20, 30, 40, 50, 60, 100]
    labels = ['Under 20', '20-29', '30-39', '40-49', '50-59', '60+']
    complete_data['age_group'] = pd.cut(complete_data['age'], bins=bins, labels=labels, right=False)
    age_group_stats = complete_data.groupby('age_group')['time_seconds'].agg(['count', 'mean', 'median', 'std'])
    def seconds_to_time(seconds):
        if seconds is None or np.isnan(seconds):
            return "N/A"
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours)}:{int(minutes):02d}:{int(seconds):02d}"
    age_group_stats['mean_time'] = age_group_stats['mean'].apply(seconds_to_time)
    age_group_stats['median_time'] = age_group_stats['median'].apply(seconds_to_time)
    print("\nStatistics by age group:")
    print(f"{'Age Group':<10}{'Count':<8}{'Mean Time':<12}{'Median Time':<12}")
    print("-" * 45)
    for age_group, row in age_group_stats.iterrows():
        print(f"{age_group:<10}{int(row['count']):<8}{row['mean_time']:<12}{row['median_time']:<12}")
    return {
        'correlation': correlation,
        'interpretation': interpretation,
        'direction': direction,
        'age_group_stats': age_group_stats
    }
