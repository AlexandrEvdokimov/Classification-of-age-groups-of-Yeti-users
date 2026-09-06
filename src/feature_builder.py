import pandas as pd


def aggregate_visits(visits):
    df = visits.copy()

    df['daytime'] = df['daytime'].replace({'утро':'morn', 'день':'sun', 'вечер':'evening', 'ночь':'night'})

    result = pd.crosstab(df['user_id'], df['daytime'], normalize='index').add_prefix('share_daytime_')

    categories = pd.crosstab(df['user_id'], df['website_category'], normalize='index').add_prefix('share_')

    category_counts = pd.crosstab(df['user_id'], df['website_category'])

    category_stats = pd.DataFrame({ 'most_freq_cat': category_counts.idxmax(axis=1),
                                   'least_freq_cat': category_counts.idxmin(axis=1)
                                  })

    result = result.merge(categories, on='user_id', how='left')
    result = result.merge(category_stats, on='user_id', how='left')
    result.columns = result.columns.str.lower().str.replace(" ", "_")
    return result


def build_features(users, visits, ads_activity, surf_depth, primary_device, cloud_usage):
    users = users.drop(columns=['age_category'], errors='ignore')
    features = users.drop_duplicates(subset=['user_id'],ignore_index=True)

    visits = visits.drop_duplicates(subset=['session_id'],ignore_index=True)
    ads_activity = ads_activity.drop_duplicates(subset=['user_id'],ignore_index=True)
    surf_depth = surf_depth.drop_duplicates(subset=['user_id'],ignore_index=True)
    primary_device = primary_device.drop_duplicates(subset=['user_id'],ignore_index=True)
    cloud_usage = cloud_usage.drop_duplicates(subset=['user_id'],ignore_index=True)

    visits = aggregate_visits(visits)

    features = features.merge(visits, on="user_id", how="left")
    features = features.merge(ads_activity, on="user_id", how="left")
    features = features.merge(surf_depth, on="user_id", how="left")
    features = features.merge(primary_device, on="user_id", how="left")
    features = features.merge(cloud_usage, on="user_id", how="left")

    return features
