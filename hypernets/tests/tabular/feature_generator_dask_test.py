# -*- coding:utf-8 -*-
"""

"""
import math
from datetime import datetime

import dask.dataframe as dd
import pandas as pd
import pytest
from sklearn.pipeline import Pipeline

from hypernets.tabular import dask_ex as dex
from hypernets.tabular.column_selector import column_object_category_bool, column_number_exclude_timedelta
from hypernets.tabular.dataframe_mapper import DataFrameMapper
from hypernets.tabular.datasets import dsutils
from hypernets.tabular.feature_generators import FeatureGenerationTransformer
from hypernets.tests.tabular.dask_transofromer_test import setup_dask
from hypernets.utils import logging

logger = logging.getLogger(__name__)


def general_preprocessor():
    cat_transformer = Pipeline(
        steps=[('imputer_cat', dex.SimpleImputer(strategy='constant', fill_value='')),
               ('encoder', dex.OrdinalEncoder())])
    num_transformer = Pipeline(
        steps=[('imputer_num', dex.SimpleImputer(strategy='mean')),
               ('scaler', dex.StandardScaler())])

    preprocessor = DataFrameMapper(features=[(column_object_category_bool, cat_transformer),
                                             (column_number_exclude_timedelta, num_transformer)],
                                   input_df=True,
                                   df_out=True)
    return preprocessor


class Test_FeatureGeneratorWithDask:
    @classmethod
    def setup_class(cls):
        setup_dask(cls)

    def test_pipeline(self):
        df = dsutils.load_bank()
        df.drop(['id'], axis=1, inplace=True)
        ddf = dex.dd.from_pandas(df.head(100), npartitions=2)
        X_train, X_test = dex.train_test_split(ddf, test_size=0.2, random_state=42)
        ftt = FeatureGenerationTransformer(task='binary', trans_primitives=['cross_categorical'],
                                           categories_cols=column_object_category_bool(X_train))
        preprocessor = general_preprocessor()
        pipe = Pipeline(steps=[('feature_gen', ftt), ('processor', preprocessor)])
        X_t = pipe.fit_transform(X_train)
        X_t = X_t.compute()
        assert X_t.shape[1] == 62

    def test_in_dataframe_mapper(self):
        df = dsutils.load_bank()
        df.drop(['id'], axis=1, inplace=True)
        ddf = dex.dd.from_pandas(df.head(100), npartitions=2)
        X_train, X_test = dex.train_test_split(ddf, test_size=0.2, random_state=42)
        ftt = FeatureGenerationTransformer(task='binary', trans_primitives=['cross_categorical'],
                                           categories_cols=column_object_category_bool(X_train))
        dfm = DataFrameMapper(features=[(X_train.columns.to_list(), ftt)],
                              input_df=True,
                              df_out=True)
        X_t = dfm.fit_transform(X_train)
        X_t = X_t.compute()
        assert X_t.shape[1] == 62

    def test_feature_tools_categorical_cross(self):
        df = dsutils.load_bank()
        df.drop(['id'], axis=1, inplace=True)
        ddf = dex.dd.from_pandas(df.head(100), npartitions=2)
        X_train, X_test = dex.train_test_split(ddf, test_size=0.2, random_state=42)
        cat_cols = column_object_category_bool(X_train)
        ftt = FeatureGenerationTransformer(task='binary', trans_primitives=['cross_categorical'],
                                           categories_cols=cat_cols)
        ftt.fit(X_train)
        x_t = ftt.transform(X_train)
        columns = set(x_t.columns.to_list())
        for i_left in range(len(cat_cols) - 1):
            for i_right in range(i_left + 1, len(cat_cols)):
                assert f'CROSS_CATEGORICAL_{cat_cols[i_left]}__{cat_cols[i_right]}' in columns \
                       or f'CROSS_CATEGORICAL_{cat_cols[i_right]}__{cat_cols[i_left]}' in columns

    def test_feature_tools_transformer(self):
        df = dsutils.load_bank()
        df.drop(['id'], axis=1, inplace=True)
        y = df.pop('y')
        ddf = dex.dd.from_pandas(df.head(100), npartitions=2)
        X_train, X_test = dex.train_test_split(ddf, test_size=0.2, random_state=42)
        ftt = FeatureGenerationTransformer(task='binary', trans_primitives=['add_numeric', 'divide_numeric'])
        ftt.fit(X_train)
        x_t = ftt.transform(X_train)
        assert x_t is not None

    # def test_feature_selection(self):
    #     df = dsutils.load_bank().head(1000)
    #     df.drop(['id'], axis=1, inplace=True)
    #     y = df.pop('y')
    #     ftt = FeatureGenerationTransformer(task='binary',
    #                                        trans_primitives=['add_numeric', 'divide_numeric', 'cross_categorical'],
    #                                        categories_cols=column_object_category_bool(df))
    #     ftt.fit(df)
    #     x_t = ftt.transform(df)
    #
    #     fst = FeatureSelectionTransformer('binary', ratio_select_cols=0.2, reserved_cols=ftt.original_cols)
    #     fst.fit(x_t, y)
    #     assert len(fst.scores_.items()) == 99
    #     assert len(fst.columns_) == 35
    #     x_t2 = fst.transform(x_t)
    #     assert x_t2.shape[1] == 35

    def test_category_datetime_text(self):
        df = dsutils.load_movielens()
        df['genres'] = df['genres'].apply(lambda s: s.replace('|', ' '))
        df['timestamp'] = df['timestamp'].apply(datetime.fromtimestamp)
        ddf = dd.from_pandas(df, npartitions=2)
        ftt = FeatureGenerationTransformer(task='binary', text_cols=['title'], categories_cols=['gender', 'genres'])
        x_t = ftt.fit_transform(ddf)
        xt_columns = x_t.columns.to_list()
        assert 'CROSS_CATEGORICAL_gender__genres' in xt_columns
        assert 'TFIDF__title____0__' in xt_columns
        assert 'DAY__timestamp__' in xt_columns

    def test_latlong(self):
        df = pd.DataFrame()
        df['latitude'] = [51.52, 9.93, 37.38]
        df['longitude'] = [-0.17, 76.25, -122.08]
        df['latlong'] = df[['latitude', 'longitude']].apply(tuple, axis=1)
        df['latitude2'] = [51.22, 9.22, 37.22]
        df['longitude2'] = [-0.22, 76.22, -122.22]
        df['latlong2'] = df[['latitude2', 'longitude2']].apply(tuple, axis=1)
        df = dd.from_pandas(df, npartitions=1)
        ftt = FeatureGenerationTransformer(latlong_cols=['latlong', 'latlong2'])
        x_t = ftt.fit_transform(df)
        print(x_t.head(3))
        assert 'GEOHASH__latlong__' in x_t.columns.to_list()

    # def test_feature_generation_with_selection(self):
    #     df = dsutils.load_bank().head(1000)
    #     df.drop(['id'], axis=1, inplace=True)
    #     y = df.pop('y')
    #     ftt = FeatureGenerationTransformer(task='binary',
    #                                        trans_primitives=['add_numeric', 'divide_numeric', 'cross_categorical'],
    #                                        categories_cols=column_object_category_bool(df),
    #                                        feature_selection_args={'ratio_select_cols': 0.2})
    #     with pytest.raises(AssertionError) as err:
    #         ftt.fit(df)
    #         assert err.value == '`y` must be provided for feature selection.'
    #     ftt.fit(df, y)
    #     x_t = ftt.transform(df)
    #     assert x_t.shape[1] == 35

    @pytest.mark.parametrize('fix_input', [True, False])
    def test_fix_input(self, fix_input: bool):
        df = pd.DataFrame(data={"x1": [None, 2, 3], 'x2': [4, 5, 6]})
        df = dex.dd.from_pandas(df, npartitions=1)
        ftt = FeatureGenerationTransformer(task='binary', trans_primitives=['add_numeric', 'divide_numeric'],
                                           fix_input=fix_input)
        ftt.fit(df)
        x_t = ftt.transform(df)
        x_t = x_t.compute()
        assert "x1__+__x2" in x_t
        assert "x1__/__x2" in x_t

        if fix_input is True:
            # should no NaN value not only input nor output
            assert not math.isnan(x_t["x1"][0])
            assert not math.isnan(x_t["x1__/__x2"][0])
        else:
            # x1 is NaN, it's children is NaN too.
            assert math.isnan(x_t["x1"][0])
            assert math.isnan(x_t["x1__/__x2"][0])

    def test_datetime_derivation(self):

        df = pd.DataFrame(data={"x1": [datetime.now()]})
        ftt = FeatureGenerationTransformer(task='binary', trans_primitives=["year", "month", "week"])
        ftt.fit(df)

        x_t = ftt.transform(df)
        assert "YEAR__x1__" in x_t
        assert "MONTH__x1__" in x_t
        assert "WEEK__x1__" in x_t

    def test_persist(self, tmp_path: str):
        from os import path as P
        tmp_path = P.join(tmp_path, 'fft.pkl')

        df = pd.DataFrame(data={"x1": [datetime.now()]})
        ftt = FeatureGenerationTransformer(task='binary', trans_primitives=["year", "month", "week"])
        ftt.fit(df)
        import pickle

        with open(tmp_path, 'wb') as f:
            pickle.dump(ftt, f)

        with open(tmp_path, 'rb') as f:
            ftt1 = pickle.load(f)

        x_t = ftt1.transform(df)
        assert "YEAR__x1__" in x_t
        assert "MONTH__x1__" in x_t
        assert "WEEK__x1__" in x_t
