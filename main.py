import os

import pandas as pd
import numpy as np

# SET TO TRUE TO SAVE CSV TO PROJECT FOLDER
SAVE_SCHEMA = False


def read_schema():
    try:
        schema_df = pd.read_csv('data/user_activity.csv')
    except Exception:
        schema_df = create_schema_from_scratch()

    schema_df.replace('NA', np.nan, inplace=True)
    schema_df.sort_values(by=(['user_id', 'action']), inplace=True)
    schema_df.reset_index(inplace=True)
    schema_df[['timestamp']] = schema_df[['timestamp']].apply(pd.to_datetime)

    return schema_df


def create_schema_from_scratch():
    users = {
        'user_id': ['2234', '2244', '2234', '2244', '2235', '2236', '2236'],
        'timestamp': ['2023-10-06 08:00:00', '2023-10-06 08:30:00', '2023-10-06 09:00:00', '2023-10-06 10:00:00',
                      '2023-10-06 10:30:00', '2023-10-06 10:30:00', '2023-10-06 11:30:00'],
        'action': ['login', 'login', 'logout', 'logout', 'login', 'login', 'logout'],
    }

    schema_df = pd.DataFrame(users)

    if SAVE_SCHEMA:
        csv_name = 'user_activity.csv'

        outdir = './data'
        if not os.path.exists(outdir):
            os.mkdir(outdir)

        full_path = os.path.join(outdir, csv_name)

        schema_df.to_csv(full_path)

    return schema_df


def get_total_login_time(df, input_id):
    single_user_list = []
    for x in df.itertuples(index=False):
        if x.user_id == input_id:
            single_user_list.append(x.timestamp)

    if not single_user_list:
        return print(f"Sorry, no user found under id: {input_id}")

    if len(single_user_list) < 2:
        # get last recorded timestamp to use for missing logout
        single_user_list.append(df['timestamp'].max())

    td = np.ptp(single_user_list)
    td = td / np.timedelta64(1, 'h')

    return_single_response(td, input_id)


def get_total_all(df):
    df_filtered = df.groupby('user_id').apply(login_logout_df_filter).reset_index(level=1, drop=True)
    # add new 'elapsed' column to df for total for each user
    df_filtered['elapsed'] = (df_filtered.logout - df_filtered.login) / pd.Timedelta(hours=1)

    df_no_logouts = handle_no_logouts(df_filtered)

    elapsed_filt = (df_filtered['elapsed'] == 0.0)
    # remove 0.0 hour people from initial df
    df_filtered = df_filtered.drop(index=df_filtered[elapsed_filt].index)
    # append new 'no logout' people back to df
    df_filtered = df_filtered.append(df_no_logouts)
    df_filtered = df_filtered.sort_values(by=['elapsed'], ascending=False)

    return df_filtered


def handle_no_logouts(df):
    """ Create a new dataframe with user_id's having no logout.
        Change their logout to last time recorded and determine new elapsed time """
    elapsed_filt = (df['elapsed'] == 0.0)

    result = df[elapsed_filt]
    max_time = df['logout'].max()
    result['logout'] = max_time
    result['elapsed'] = (result.logout - result.login) / pd.Timedelta(hours=1)

    return result


def return_single_response(total_time, user_id=None):
    return print(f"User ID: {user_id} Total Time Spent (hours): {total_time}")


def return_multiple_response(df):
    for user in df.itertuples():
        print(f"User ID: {user.Index} Total Time Spent (hours): {user.elapsed}")


def login_logout_df_filter(df):
    """ Create new dataframe with login and logout columns for matching user_ids """
    return df.sort_values('timestamp').groupby(df.action.isin(['login']).cumsum()).agg(**{
        'login': ('timestamp', 'first'),
        'logout': ('timestamp', 'last')})


if __name__ == '__main__':
    schema_df = read_schema()
    print("Enter user_id, or type \"ALL\" for all records, to find login time:")
    input_id = str(input())

    if input_id in ["ALL", "all"]:
        return_multiple_response(get_total_all(schema_df))
    else:
        get_total_login_time(schema_df, input_id)
