def analyze_city_distribution(data):
    """
    Analyze the percentage of participants from Huntsville and Madison

    Args:
        data: DataFrame containing the race data

    Returns:
        A dictionary with the analysis results
    """
    city_counts = data['city'].value_counts()
    total_runners = data.shape[0]
    huntsville_count = city_counts.get('Huntsville', 0)
    madison_count = city_counts.get('Madison', 0)
    huntsville_pct = (huntsville_count / total_runners) * 100
    madison_pct = (madison_count / total_runners) * 100
    combined_pct = huntsville_pct + madison_pct
    print(f"\nQuestion 1: What percentage of participants are from Huntsville and Madison?")
    print(f"Total runners: {total_runners}")
    print(f"Runners from Huntsville: {huntsville_count} ({huntsville_pct:.2f}%)")
    print(f"Runners from Madison: {madison_count} ({madison_pct:.2f}%)")
    print(f"Combined Huntsville & Madison: {huntsville_count + madison_count} ({combined_pct:.2f}%)")
    missing_city = data['city'].isna().sum()
    print(f"Number of runners with missing city: {missing_city}")
    return {
        'total_runners': total_runners,
        'huntsville_count': huntsville_count,
        'madison_count': madison_count,
        'huntsville_percentage': huntsville_pct,
        'madison_percentage': madison_pct,
        'combined_percentage': combined_pct,
        'missing_city_count': missing_city
    }
