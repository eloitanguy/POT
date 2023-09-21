"""Tests for module mapping"""
# Author: Eloi Tanguy <eloi.tanguy@u-paris.fr>
#
# License: MIT License

import numpy as np
import ot
import pytest
from ot.backend import to_numpy


try:  # test if cvxpy is installed
    import cvxpy  # noqa: F401
    nocvxpy = False
except ImportError:
    nocvxpy = True


@pytest.mark.skipif(nocvxpy, reason="No CVXPY available")
def test_ssnb_qcqp_constants():
    c1, c2, c3 = ot.mapping.ssnb_qcqp_constants(.5, 1)
    np.testing.assert_almost_equal(c1, 1)
    np.testing.assert_almost_equal(c2, .5)
    np.testing.assert_almost_equal(c3, 1)


@pytest.mark.skipif(nocvxpy, reason="No CVXPY available")
def test_nearest_brenier_potential_fit(nx):
    X = nx.ones((2, 2))
    phi, G, log = ot.nearest_brenier_potential_fit(X, X, its=3, log=True)
    np.testing.assert_almost_equal(to_numpy(G), to_numpy(X))  # image of source should be close to target
    # test without log but with X_classes and seed
    ot.nearest_brenier_potential_fit(X, X, X_classes=nx.ones(2), its=1, seed=0)
    # test with seed being a np.random.RandomState
    ot.nearest_brenier_potential_fit(X, X, its=1, seed=np.random.RandomState(seed=0))


@pytest.mark.skipif(nocvxpy, reason="No CVXPY available")
def test_brenier_potential_predict_bounds(nx):
    X = nx.ones((2, 2))
    phi, G = ot.nearest_brenier_potential_fit(X, X, its=3)
    phi_lu, G_lu, log = ot.nearest_brenier_potential_predict_bounds(X, phi, G, X, log=True)
    # 'new' input isn't new, so should be equal to target
    np.testing.assert_almost_equal(to_numpy(G_lu[0]), to_numpy(X))
    np.testing.assert_almost_equal(to_numpy(G_lu[1]), to_numpy(X))
    # test with no log but classes
    ot.nearest_brenier_potential_predict_bounds(X, phi, G, X, X_classes=nx.ones(2), Y_classes=nx.ones(2))


def test_joint_OT_mapping_verbose():
    xs = np.zeros((2, 1))
    ot.mapping.joint_OT_mapping_kernel(xs, xs, verbose=True)
    ot.mapping.joint_OT_mapping_linear(xs, xs, verbose=True)
