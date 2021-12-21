# -*- coding:utf-8 -*-
"""

"""
import cudf
import cupy
import numpy as np
import pandas as pd
from cuml.common.array import CumlArray
from cuml.decomposition import TruncatedSVD
from cuml.pipeline import Pipeline
from cuml.preprocessing import SimpleImputer, LabelEncoder, OneHotEncoder, TargetEncoder, \
    StandardScaler, MaxAbsScaler, MinMaxScaler, RobustScaler
from sklearn import preprocessing as sk_pre, impute as sk_imp, decomposition as sk_dec
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_is_fitted

from hypernets.tabular import sklearn_ex as sk_ex
from .. import tb_transformer


class Localizable:
    def as_local(self):
        """
        convert the fitted transformer to accept pandas/numpy data, and remove cuml dependencies.
        """
        return self  # default: do nothing


def copy_attrs_as_local(tf, target, *attrs):
    from .. import CumlToolBox

    def to_local(x):
        if x is None:
            pass
        elif isinstance(x, list):
            x = list(map(to_local, x))
        elif isinstance(x, tuple):
            x = tuple(map(to_local, x))
        elif isinstance(x, dict):
            x = {ki: to_local(xi) for ki, xi in x.items()}
        elif hasattr(x, 'as_local'):
            x = x.as_local()
        else:
            x = CumlToolBox.to_local(x)[0]
        return x

    for a in attrs:
        v = getattr(tf, a)
        setattr(target, a, to_local(v))
    return target


def as_local_if_possible(tf):
    return tf.as_local() if hasattr(tf, 'as_local') else tf


@tb_transformer(cudf.DataFrame, name='Pipeline')
class LocalizablePipeline(Pipeline, Localizable):
    def as_local(self):
        from sklearn.pipeline import Pipeline as SkPipeline
        steps = [(name, as_local_if_possible(tf)) for name, tf in self.steps]
        target = SkPipeline(steps, verbose=self.verbose)
        return target


@tb_transformer(cudf.DataFrame, name='StandardScaler')
class LocalizableStandardScaler(StandardScaler, Localizable):
    def as_local(self):
        target = sk_pre.StandardScaler(copy=self.copy, with_mean=self.with_mean, with_std=self.with_std)
        copy_attrs_as_local(self, target, 'scale_', 'mean_', 'var_', 'n_samples_seen_')
        return target


@tb_transformer(cudf.DataFrame, name='MinMaxScaler')
class LocalizableMinMaxScaler(MinMaxScaler, Localizable):
    def as_local(self):
        target = sk_pre.MinMaxScaler(self.feature_range, copy=self.copy)
        copy_attrs_as_local(self, target, 'min_', 'scale_', 'data_min_', 'data_max_', 'data_range_', 'n_samples_seen_')
        return target


@tb_transformer(cudf.DataFrame, name='MaxAbsScaler')
class LocalizableMaxAbsScaler(MaxAbsScaler, Localizable):
    def as_local(self):
        target = sk_pre.MaxAbsScaler(copy=self.copy)
        copy_attrs_as_local(self, target, 'scale_', 'max_abs_', 'n_samples_seen_')
        return target


@tb_transformer(cudf.DataFrame, name='RobustScaler')
class LocalizableRobustScaler(RobustScaler, Localizable):
    def as_local(self):
        target = sk_pre.RobustScaler(with_centering=self.with_centering, with_scaling=self.with_scaling,
                                     quantile_range=self.quantile_range, copy=self.copy)
        copy_attrs_as_local(self, target, 'scale_', 'center_', )
        return target


@tb_transformer(cudf.DataFrame, name='TruncatedSVD')
class LocalizableTruncatedSVD(TruncatedSVD, Localizable):
    def as_local(self):
        target = sk_dec.TruncatedSVD(self.n_components, algorithm=self.algorithm, n_iter=self.n_iter,
                                     random_state=self.random_state, tol=self.tol)
        copy_attrs_as_local(self, target, 'components_', 'explained_variance_',
                            'explained_variance_ratio_', 'singular_values_')
        return target


@tb_transformer(cudf.DataFrame, name='SimpleImputer')
class LocalizableSimpleImputer(SimpleImputer, Localizable):
    def fit(self, X, y=None):
        self.feature_names_in_ = X.columns.tolist() if isinstance(X, (cudf.DataFrame, pd.DataFrame)) else None
        return super().fit(X, y)

    def as_local(self):
        target = sk_imp.SimpleImputer(missing_values=self.missing_values, strategy=self.strategy,
                                      fill_value=self.fill_value, copy=self.copy, add_indicator=self.add_indicator)
        copy_attrs_as_local(self, target, 'statistics_', 'feature_names_in_')  # 'indicator_', )

        ss = target.statistics_
        if isinstance(ss, (list, tuple)) and isinstance(ss[0], np.ndarray):
            target.statistics_ = ss[0]
        return target

    # override to fix cuml
    def _check_n_features(self, X, reset):
        """Set the `n_features_in_` attribute, or check against it.

        Parameters
        ----------
        X : {ndarray, sparse matrix} of shape (n_samples, n_features)
            The input samples.
        reset : bool
            If True, the `n_features_in_` attribute is set to `X.shape[1]`.
            Else, the attribute must already exist and the function checks
            that it is equal to `X.shape[1]`.
        """
        n_features = X.shape[1]

        if reset:
            self.n_features_in_ = n_features
        else:
            if not hasattr(self, 'n_features_in_'):
                raise RuntimeError(
                    "The reset parameter is False but there is no "
                    "n_features_in_ attribute. Is this estimator fitted?"
                )
            if n_features != self.n_features_in_:
                raise ValueError(
                    'X has {} features, but this {} is expecting {} features '
                    'as input.'.format(n_features, self.__class__.__name__,
                                       self.n_features_in_)
                )

    def transform(self, X):
        Xt = super().transform(X)
        if isinstance(Xt, cudf.Series):
            Xt = Xt.to_frame()
        elif isinstance(Xt, CumlArray):
            Xt = cupy.array(Xt)
        return Xt


@tb_transformer(cudf.DataFrame)
class ConstantImputer(BaseEstimator, TransformerMixin, Localizable):
    def __init__(self, missing_values=np.nan, fill_value=None, copy=True) -> None:
        super().__init__()

        self.missing_values = missing_values
        self.fill_value = fill_value
        self.copy = copy

    def fit(self, X, y=None, ):
        return self

    def transform(self, X, y=None):
        if self.copy:
            X = X.copy()

        X.replace(self.missing_values, self.fill_value, inplace=True)
        return X


@tb_transformer(cudf.DataFrame, name='OneHotEncoder')
class LocalizableOneHotEncoder(OneHotEncoder, Localizable):
    def as_local(self):
        from .. import CumlToolBox
        target = sk_pre.OneHotEncoder(categories=CumlToolBox.to_local(self.categories)[0],
                                      drop=self.drop, sparse=self.sparse,
                                      dtype=self.dtype, handle_unknown=self.handle_unknown)
        copy_attrs_as_local(self, target, 'categories_', 'drop_idx_')
        return target


@tb_transformer(cudf.DataFrame)
class SlimTargetEncoder(TargetEncoder, BaseEstimator):
    """
    The slimmed TargetEncoder with 'train' and 'train_encode' attribute were set to None.
    """

    def __init__(self, n_folds=4, smooth=0, seed=42, split_method='interleaved', dtype=None, output_2d=False):
        super().__init__(n_folds=n_folds, smooth=smooth, seed=seed, split_method=split_method)

        self.dtype = dtype
        self.output_2d = output_2d

    def fit(self, X, y):
        super().fit(X, y)
        self.train = None
        self.train_encode = None
        return self

    def fit_transform(self, X, y):
        Xt, _ = self._fit_transform(X, y)
        self.train = None
        self.train_encode = None
        self._fitted = True
        if self.dtype is not None:
            Xt = Xt.astype(self.dtype)
        if self.output_2d:
            Xt = Xt.reshape(-1, 1)
        return Xt

    def transform(self, X):
        Xt = super().transform(X)
        if self.dtype is not None:
            Xt = Xt.astype(self.dtype)
        if self.output_2d:
            Xt = Xt.reshape(-1, 1)
        return Xt

    def _check_is_fitted(self):
        check_is_fitted(self, '_fitted')

    def _is_train_df(self, df):
        return False

    @property
    def split_method(self):
        return self.split

    def as_local(self):
        target = sk_ex.SlimTargetEncoder(n_folds=self.n_folds, smooth=self.smooth, seed=self.seed,
                                         split_method=self.split, dtype=self.dtype, output_2d=self.output_2d)
        copy_attrs_as_local(self, target, '_fitted', 'train', 'train_encode', 'encode_all', 'mean', 'output_2d')
        return target


@tb_transformer(cudf.DataFrame)
class MultiTargetEncoder(sk_ex.MultiTargetEncoder):
    target_encoder_cls = SlimTargetEncoder
    label_encoder_cls = LabelEncoder

    def as_local(self):
        target = sk_ex.MultiTargetEncoder(n_folds=self.n_folds, smooth=self.smooth, seed=self.seed,
                                          split_method=self.split_method)
        target.encoders_ = {k: le.as_local() for k, le in self.encoders_.items()}
        return target


@tb_transformer(cudf.DataFrame, name='LabelEncoder')
class LocalizableLabelEncoder(LabelEncoder, Localizable):
    def as_local(self):
        target = sk_pre.LabelEncoder()
        copy_attrs_as_local(self, target, 'classes_', )
        return target

    # override to accept pd.Series and ndarray
    def inverse_transform(self, y) -> cudf.Series:
        if isinstance(y, pd.Series):
            y = cudf.from_pandas(y)
        elif isinstance(y, np.ndarray):
            y = cudf.from_pandas(pd.Series(y))
        elif isinstance(y, cupy.ndarray):
            y = cudf.Series(y)

        return super().inverse_transform(y)


@tb_transformer(cudf.DataFrame)
class SafeLabelEncoder(LabelEncoder):
    def __init__(self, *, verbose=False, output_type=None):
        super().__init__(handle_unknown='ignore', verbose=verbose, output_type=output_type)

    def fit_transform(self, y: cudf.Series, z=None) -> cudf.Series:
        t = super().fit_transform(y, z=z)
        return t

    def transform(self, y: cudf.Series) -> cudf.Series:
        t = super().transform(y)
        t.fillna(len(self.classes_), inplace=True)
        return t

    def as_local(self):
        target = sk_ex.SafeLabelEncoder()
        copy_attrs_as_local(self, target, 'classes_', )
        return target


@tb_transformer(cudf.DataFrame)
class MultiLabelEncoder(BaseEstimator, Localizable):
    def __init__(self, columns=None, dtype=None):
        super().__init__()

        self.columns = columns
        self.dtype = dtype

        # fitted
        self.encoders = {}

    def fit(self, X: cudf.DataFrame, y=None):
        assert isinstance(X, cudf.DataFrame)

        if self.columns is None:
            self.columns = X.columns.tolist()

        for col in self.columns:
            data = X.loc[:, col]
            if data.dtype == 'object':
                data = data.astype('str')
            le = SafeLabelEncoder()
            le.fit(data)
            self.encoders[col] = le

        return self

    def transform(self, X: cudf.DataFrame):
        assert isinstance(X, cudf.DataFrame) and self.columns is not None
        others = [c for c in X.columns.tolist() if c not in self.columns]

        dfs = []
        if len(others) > 0:
            dfs.append(X[others])

        for col in self.columns:
            data = X.loc[:, col]
            if data.dtype == 'object':
                data = data.astype('str')
            t = self.encoders[col].transform(data)
            if self.dtype is not None:
                t = t.astype(self.dtype)
            dfs.append(t)

        df = cudf.concat(dfs, axis=1, ignore_index=True) if len(dfs) > 1 else dfs[0]
        df.index = X.index
        df.columns = others + self.columns
        if len(others) > 0:
            df = df[X.columns]

        return df

    def fit_transform(self, X: cudf.DataFrame, *args):
        if self.columns is None:
            self.columns = X.columns.tolist()
            others = []
        else:
            others = [c for c in X.columns.tolist() if c not in self.columns]

        dfs = []
        if len(others) > 0:
            dfs.append(X[others])

        for col in self.columns:
            data = X.loc[:, col]
            if data.dtype == 'object':
                data = data.astype('str')
            le = SafeLabelEncoder()
            t = le.fit_transform(data)  # .to_frame(name=col)
            if self.dtype is not None:
                t = t.astype(self.dtype)
            dfs.append(t)
            self.encoders[col] = le
        df = cudf.concat(dfs, axis=1, ignore_index=True) if len(dfs) > 1 else dfs[0]
        df.index = X.index
        df.columns = others + self.columns
        if len(others) > 0:
            df = df[X.columns]

        return df

    def as_local(self):
        target = sk_ex.MultiLabelEncoder()
        target.columns = self.columns
        target.dtype = self.dtype
        target.encoders = {k: e.as_local() for k, e in self.encoders.items()}
        return target
