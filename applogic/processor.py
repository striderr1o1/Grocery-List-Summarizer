import pandas as pd

def process_grocery_data(json_list, selected_month):
    """
    Processes the raw MongoDB cursor data into a unified DataFrame and calculates the total cost.
    
    Args:
        fetched_cursor: The cursor returned from MongoDB find().
        selected_month: The month to filter by (e.g., "January") or "all".
        
    Returns:
        tuple: (processed_dataframe, total_cost)
               - processed_dataframe: A pandas DataFrame containing the relevant data.
                                      Returns None if no data is found.
               - total_cost: The sum of costs matching the filter.
    """
    dataframes = []
    total = 0
    
    for doc in json_list:
        # Convert single document to DataFrame
        frame = pd.DataFrame.from_dict(doc)
        
        # Cleanup
        #if '_id' in frame.columns:
        #    frame = frame.drop('_id', axis=1)
            
        # Date processing
        frame["date"] = pd.to_datetime(frame["date"], format='%Y-%m-%d')
        frame.sort_values(by="date", inplace=True)
        frame["month"] = frame["date"].dt.month_name()
        
        # Calculate Total based on filter
        # We check the first row's month since a single list belongs to one month
        if selected_month == "all":
            total += doc.get("total", 0)
        elif not frame.empty and frame["month"].iloc[0] == selected_month:
            total += doc.get("total", 0)
            
        dataframes.append(frame)
    
    if not dataframes:
        return None, 0

    # Combine all frames
    combined_frame = pd.concat(dataframes, ignore_index=True)
    
    # Filter DataFrame based on selection
    if selected_month != "all":
        combined_frame = combined_frame[combined_frame["month"] == selected_month]
        
    return combined_frame, total
