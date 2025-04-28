def main():
    """
    Main function to run all analyses for the project.
    """
    data = pd.read_csv('project_data.csv')
    city_results = analyze_city_distribution(data)
    data = fix_half_marathon_times(data)
    drop_lap = analyze_dr_h_chen_pacer(data)
    dizzy_lap = analyze_dr_c_chen_dizzy(data)
    correlation_results = analyze_age_finishing_time_correlation(data)
    skipped_loop_results = analyze_skipped_second_loop(data)
    pace_results = analyze_pace_trends(data)
    negative_split_results = analyze_negative_splits(data)
    penalty_rule_results = analyze_penalty_rule(data)
    fatigue_results = analyze_fatigue_onset(data)
    print("\n--- SUMMARY OF FINDINGS ---")
    print(f"1. {city_results['combined_percentage']:.2f}% of participants are from Huntsville and Madison.")
    print("2. Half marathon times fixed based on place ranges.")
    if drop_lap:
        print(f"3. Dr. H. Chen was dropped by the 3-hour pacer at lap {drop_lap}.")
    if dizzy_lap:
        print(f"4. Dr. C. Chen likely got dizzy around lap {dizzy_lap}.")
    print(f"5. The correlation between age and finishing time is {correlation_results['correlation']:.4f}, "
          f"indicating a {correlation_results['interpretation']} {correlation_results['direction']} correlation.")
    print(f"6. Approximately {skipped_loop_results['total_skipped_estimate']} runners "
          f"({skipped_loop_results['skipped_percentage']:.2f}%) skipped the second short loop.")
    print(f"7. On average, runners tend to {pace_results['overall_trend']} as they run further, "
          f"with {pace_results['slowing_down_count']} runners ({pace_results['slowing_down_count']/(pace_results['slowing_down_count']+pace_results['speeding_up_count'])*100:.2f}%) "
          f"showing a slowing trend.")
    print(f"8. Negative split analysis: "
          f"Fast runners (top 25%): {negative_split_results['fast_negative_split_percentage']:.2f}% achieved a negative split, "
          f"Slow runners (bottom 25%): {negative_split_results['slow_negative_split_percentage']:.2f}% achieved a negative split.")
    print(f"9. Evidence for 1:2 penalty rule: {penalty_rule_results['percentage_following_rule']:.2f}% of runners who ran too fast in the first half "
          f"followed the rule (average penalty ratio: {penalty_rule_results['avg_penalty_ratio']:.2f}).")
    if fatigue_results['fatigue_lap']:
        print(f"10. Fatigue sets in around lap {fatigue_results['fatigue_lap']}. "
              "This was determined by analyzing the average split times across all runners to identify a significant slowdown, "
              "and examining individual runners' splits to find where their pace increased by a notable margi")
  
    data.to_csv('project_data_fixed.csv', index=False)
    print("Analysis complete!")

if __name__ == "__main__":
    main()
