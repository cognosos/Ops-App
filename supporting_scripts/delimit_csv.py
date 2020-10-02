def extract_ids(my_csv):
    import pandas as pd
    my_df = pd.read_csv(my_csv)
    my_ids = list(my_df.iloc[:,0])
    if str(my_ids[0])[0] not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
        my_ids = my_ids[1:]

    return my_ids